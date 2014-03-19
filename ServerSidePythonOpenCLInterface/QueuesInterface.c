#include <Python.h>
#include <CL/cl.h>
#include "OpenCLObjectsMaps.h"
#include <stdio.h>

PyObject* _CL_CreateQueue(PyObject* args){
  // creates a new OpenCL queue; 
  // the arguments are: (ContextID, DeviceID, [strProperty1, strProperty2, ])
  long contextID;
  cl_context ctx;
  long deviceID;
  cl_device_id dev;
  PyObject* propertiesList;
  cl_command_queue_properties props = 0;
  cl_int ErrCode;
  cl_command_queue newQueue;
  long newQueueID;

  if(!PyArg_ParseTuple(args, "llO", &contextID, &deviceID, &propertiesList) )
    return NULL;
  // retrieve context
  ctx = GetContext( contextID );
  // retrieve device
  dev = GetCLDevice( deviceID );
  if(ctx == NULL || dev == NULL) return NULL;
  // unpack the properties; skip for now
  // create the new command queue
  newQueue = clCreateCommandQueue(ctx, dev, props, &ErrCode);
  if(ErrCode != CL_SUCCESS)
    return Py_BuildValue("li", 0, ErrCode);
  if( !InsertCommandQueue(newQueue, &newQueueID) ){
    clReleaseCommandQueue(newQueue);
    return NULL;
  }
  return Py_BuildValue("li", newQueueID, ErrCode);
}

PyObject* _CL_GetQueueProperties(PyObject* args){
  // retrieves the properties of a queue
  // returns a map with properties and the errcode
  cl_int retErr;
  long QueueID;
  cl_command_queue localQueue;
  long DeviceID;
  cl_device_id dev;
  long ContextID;
  cl_context ctx;

  if(!PyArg_ParseTuple(args, "l", &QueueID)) return NULL;
  // retrieve the context and the device
  localQueue = GetCommandQueue( QueueID );
  if(localQueue == NULL) return NULL;
  retErr = clGetCommandQueueInfo(localQueue, CL_QUEUE_CONTEXT, sizeof(cl_context), &ctx, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  retErr = clGetCommandQueueInfo(localQueue, CL_QUEUE_DEVICE, sizeof(cl_device_id), &dev, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  // retrieve the IDs
  DeviceID = GetDeviceID( dev );
  ContextID = GetContextID( ctx );
  // return the queue properties
  return Py_BuildValue("{sisisi}i","id", QueueID, "Device", DeviceID, "Context", ContextID, retErr);
  retMinimalInfo:
    return Py_BuildValue("{si}i","id", QueueID, retErr);
}

PyObject* _CL_RetainQueue(PyObject* args){
  cl_int nErr = CL_SUCCESS;
  long QueueID;
  if(!PyArg_ParseTuple(args, "l", &QueueID)) return NULL;
  if( !RetainCommandQueue( QueueID ) ) return NULL;
  return Py_BuildValue("i", nErr);
}

PyObject* _CL_ReleaseQueue(PyObject* args){
  long count;
  long QueueID;
  if(!PyArg_ParseTuple(args, "l", &QueueID)) return NULL;
  count = ReleaseCommandQueue( QueueID );
  return Py_BuildValue("i", count);
}

PyObject* 
_CL_ListQueues(PyObject* args){
  long nQueues;
  long* Queues = NULL;
  long ii;
  PyObject* QueueList;
  PyObject* QueueID;
  nQueues = GetNumberOfCommandQueues();
  Queues = (long*)malloc(nQueues * sizeof(long));
  if(Queues == NULL) goto returnNULL;
  GetCommandQueuesIDs(Queues);
  QueueList = PyList_New(nQueues);
  if(QueueList == NULL) goto returnNULL;
  for(ii = 0; ii < nQueues; ii++){
    QueueID = PyInt_FromLong(Queues[ii]);
    if(QueueID == NULL){
      Py_DECREF(QueueList);
      goto returnNULL;
      }
    PyList_SET_ITEM(QueueList, ii, QueueID);
  }
  free(Queues);
  return QueueList;
returnNULL:
  free(Queues);
  return NULL;
}

PyObject*
_CL_EnqueueReadBuffer(PyObject* args){
  // enqueue a readbuffer operation
  // parameters (QueueID, BufferID, nBytes, offset)
  // this is a blocking operation on the server side.
  long QueueID, BufferID;
  cl_command_queue queue;
  cl_mem buffer;
  char* data = NULL;
  Py_ssize_t nBytes, offset;
  PyObject* retData;
  cl_int retErr;

  if(!PyArg_ParseTuple(args, "llnn", &QueueID, &BufferID, &nBytes, &offset)) return NULL;
  // retrieve buffer and queue
  queue = GetCommandQueue(QueueID);
  buffer = GetMem(BufferID);
  if(queue == NULL || buffer == NULL) return NULL;
  data = (char*)malloc(nBytes);
  if(data == NULL) return NULL;
  retErr = clEnqueueReadBuffer(queue, buffer, CL_TRUE, offset, nBytes, data, 0, NULL, NULL);
  retData = retErr == CL_SUCCESS ? PyByteArray_FromStringAndSize(data, nBytes) : 
                                   PyByteArray_FromStringAndSize(data, 1);
  free(data);
  return Py_BuildValue("Oi", retData, retErr);
}

PyObject*
_CL_EnqueueWriteBuffer(PyObject* args){
  // enqueue a writebuffer operation
  // parameters (QueueID, BufferID, nBytes, offset, Data)
  // this is a blocking operation on the server side.
  long QueueID, BufferID;
  cl_command_queue queue;
  cl_mem buffer;
  char* data = NULL;
  Py_ssize_t nBytes, offset;
  PyObject* pObjData;
  cl_int retErr;

  if(!PyArg_ParseTuple(args, "llnnO", &QueueID, &BufferID, &nBytes, &offset, &pObjData)) return NULL;
  // retrieve buffer and queue
  queue = GetCommandQueue(QueueID);
  buffer = GetMem(BufferID);
  if(queue == NULL || buffer == NULL) return NULL;
  if( !PyByteArray_Check(pObjData) ) return NULL;
  data = PyByteArray_AsString(pObjData);
  if(data == NULL) return NULL;
  retErr = clEnqueueWriteBuffer(queue, buffer, CL_TRUE, offset, nBytes, data, 0, NULL, NULL);
  return Py_BuildValue("i", retErr);
}

PyObject*
_CL_EnqueueCopyBuffer(PyObject* args){
  // enqueue a writebuffer operation
  // parameters (QueueID, SourceBufferID, DestinationBufferID, nBytes, SourceOffset, DestinationOffset)
  // this is a non-blocking operation on the server side.
  long QueueID, SourceBufferID, DestinationBufferID;
  cl_command_queue queue;
  cl_mem sbuffer;
  cl_mem dbuffer;
  Py_ssize_t nBytes, SourceOffset, DestinationOffset;
  cl_int retErr;

  if(!PyArg_ParseTuple(args, "lllnnn", &QueueID, &SourceBufferID, &DestinationBufferID, &nBytes, &SourceOffset, 
                       &DestinationOffset)) return NULL;
  // retrieve buffer and queue
  queue = GetCommandQueue(QueueID);
  sbuffer = GetMem(SourceBufferID);
  dbuffer = GetMem(DestinationBufferID);
  if(queue == NULL || sbuffer == NULL || dbuffer == NULL) return NULL;
  retErr = clEnqueueCopyBuffer(queue, sbuffer, dbuffer, SourceOffset, DestinationOffset, nBytes, 0, NULL, NULL);
  return Py_BuildValue("i", retErr);
}

PyObject*
_CL_EnqueueNDRangeKernel(PyObject* args){
  // enqueue an NDRange kernel
  // parameters (QueueID, KernelID, WorkOffsets, GlobalWorkSize, LocalWorkSize)
  long QueueID, KernelID;
  PyObject *pObjWorkOffsets, *pObjGlobalWorkSize, *pObjLocalWorkSize;
  PyObject *listItem; 
  size_t work_offset[3] = {0, 0, 0}, 
         global_work_size[3] = {0, 0, 0}, 
         local_work_size[3] = {0, 0, 0};
  cl_uint work_dim;
  cl_int retErr;
  cl_kernel kernel;
  cl_command_queue queue;
  cl_uint ii;

  if(!PyArg_ParseTuple(args, "llOOO", &QueueID, &KernelID, &pObjWorkOffsets, &pObjGlobalWorkSize, &pObjLocalWorkSize))
    return NULL;
  // retrieve the queue and kernel
  kernel = GetKernel(KernelID);
  queue = GetCommandQueue(QueueID);
  if(queue == NULL || kernel == NULL) return NULL;
  if(!PyList_Check(pObjWorkOffsets) || !PyList_Check(pObjGlobalWorkSize) || !PyList_Check(pObjLocalWorkSize)) return NULL;
  work_dim = (cl_uint)PyList_Size(pObjGlobalWorkSize);
  if(PyList_Size(pObjWorkOffsets) != 0 && PyList_Size(pObjWorkOffsets) != PyList_Size(pObjGlobalWorkSize)) return NULL;
  if(PyList_Size(pObjGlobalWorkSize) != PyList_Size(pObjLocalWorkSize)) return NULL;
  for(ii = 0; ii < work_dim; ii++){
    listItem = PyList_GetItem(pObjGlobalWorkSize, ii);
    if(!PyInt_Check(listItem)) return NULL;
    global_work_size[ii] = PyInt_AsSsize_t(listItem);
    listItem = PyList_GetItem(pObjLocalWorkSize, ii);
    if(!PyInt_Check(listItem)) return NULL;
    local_work_size[ii] = PyInt_AsSsize_t(listItem);
    if(PyList_Size(pObjWorkOffsets) != 0){
      listItem = PyList_GetItem(pObjWorkOffsets, ii);
      if(!PyInt_Check(listItem)) return NULL;
      work_offset[ii] = PyInt_AsSsize_t(listItem);
    }
  }
  /*
  printf("WorkDim = %u\n", work_dim);
  printf("WorkOffset = [%lu, %lu, %lu]\n", work_offset[0], work_offset[1], work_offset[2]);
  printf("LocalWorkSize = [%lu, %lu, %lu]\n", local_work_size[0], local_work_size[1], local_work_size[2]);
  printf("GlobalWorkSize = [%lu, %lu, %lu]\n", global_work_size[0], global_work_size[1], global_work_size[2]);
  */
  retErr = clEnqueueNDRangeKernel(queue, kernel, work_dim, work_offset, global_work_size, local_work_size, 0, NULL, NULL);
  return Py_BuildValue("i", retErr);
}

PyObject*
_CL_EnqueueTask(PyObject* args){
  // enqueue a task 
  // parameters (QueueID, KernelID)
  long QueueID, KernelID;
  cl_int retErr;
  cl_kernel kernel;
  cl_command_queue queue;

  if(!PyArg_ParseTuple(args, "ll", &QueueID, &KernelID))
    return NULL;
  // retrieve the queue and kernel
  kernel = GetKernel(KernelID);
  queue = GetCommandQueue(QueueID);
  if(queue == NULL || kernel == NULL) return NULL;
  retErr = clEnqueueTask(queue, kernel, 0, NULL, NULL);
  return Py_BuildValue("i", retErr);
}

PyObject*
_CL_EnqueueBarrier(PyObject* args){
  // enqueue a Barrier
  // parameters (QueueID)
  long QueueID;
  cl_int retErr;
  cl_command_queue queue;

  if(!PyArg_ParseTuple(args, "l", &QueueID))
    return NULL;
  // retrieve the queue and kernel
  queue = GetCommandQueue(QueueID);
  if(queue == NULL) return NULL;
  retErr = clEnqueueBarrier(queue);
  return Py_BuildValue("i", retErr);
}

PyObject*
_CL_Finish(PyObject* args){
  // waits for all the enqueued operations to finish
  // parameters (QueueID)
  long QueueID;
  cl_int retErr;
  cl_command_queue queue;

  if(!PyArg_ParseTuple(args, "l", &QueueID))
    return NULL;
  // retrieve the queue and kernel
  queue = GetCommandQueue(QueueID);
  if(queue == NULL) return NULL;
  retErr = clFinish(queue);
  return Py_BuildValue("i", retErr);
 return NULL;
}

