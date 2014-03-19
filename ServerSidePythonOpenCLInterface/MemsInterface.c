#include <Python.h>
#include <CL/cl.h>
#include "OpenCLObjectsMaps.h"

PyObject* _CL_CreateBuffer(PyObject* args){
  // creates a new OpenCL context; 
  // the argument are: BufferProperties dict and device id list
  long ContextID;
  cl_context ctx;
  Py_ssize_t bufferSize;
  PyObject* pObjFlags;
  cl_mem buf;
  long bufID;
  cl_int ErrCode;

  if(!PyArg_ParseTuple(args, "lnO", &ContextID, &bufferSize, &pObjFlags) )
    return NULL;
  ctx = GetContext(ContextID);
  if(ctx == NULL) return NULL;
  // create the buffer
  buf = clCreateBuffer(ctx, 0, bufferSize, NULL, &ErrCode);
  if(ErrCode != CL_SUCCESS) return Py_BuildValue("li", 0l, ErrCode);
  if( !InsertMem(buf, &bufID) ){
    clReleaseMemObject(buf);
    return NULL;
  }
  return Py_BuildValue("li", bufID, ErrCode);
}

PyObject* _CL_GetBufferProperties(PyObject* args){
  // retrieves the properties of context
  // returns a map with properties and the errcode
  cl_int retErr;
  long BufferID;
  cl_mem localBuffer;
  long ContextID;
  cl_context ctx;
  size_t bufferSize;

  if(!PyArg_ParseTuple(args, "l", &BufferID)) return NULL;
  // retrieve the cl_context
  localBuffer = GetMem( BufferID );
  if(localBuffer == NULL) return NULL;
  retErr = clGetMemObjectInfo(localBuffer, CL_MEM_CONTEXT, sizeof(cl_context), &ctx, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  retErr = clGetMemObjectInfo(localBuffer, CL_MEM_SIZE, sizeof(size_t), &bufferSize, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  // retrieve the context ID
  ContextID = GetContextID(ctx);
  return Py_BuildValue("{slslsn}i","id", BufferID, "Context", ContextID, "Size", bufferSize, retErr);
  retMinimalInfo:
    return Py_BuildValue("{sl}i","id", BufferID, retErr);
}

PyObject* _CL_RetainBuffer(PyObject* args){
  long BufferID;
  if(!PyArg_ParseTuple(args, "l", &BufferID)) return NULL;
  // retain the cl_context
  if( !RetainMem( BufferID ) ) return NULL;
  return Py_BuildValue("i", CL_SUCCESS);
}

PyObject* _CL_ReleaseBuffer(PyObject* args){
  long BufferID;
  long count;

  if(!PyArg_ParseTuple(args, "l", &BufferID)) return NULL;
  // retain the cl_context
  count = ReleaseMem( BufferID );
  return Py_BuildValue("i", count);
}

PyObject* 
_CL_ListBuffers(PyObject* args){
  long nBuffers;
  long* Buffers = NULL;
  long ii;
  PyObject* BufferList;
  PyObject* BufferID;
  nBuffers = GetNumberOfMems();
  Buffers = (long*)malloc(nBuffers * sizeof(long));
  if(Buffers == NULL) goto returnNULL;
  GetMemsIDs(Buffers);
  BufferList = PyList_New(nBuffers);
  if(BufferList == NULL) goto returnNULL;
  for(ii = 0; ii < nBuffers; ii++){
    BufferID = PyInt_FromLong(Buffers[ii]);
    if(BufferID == NULL){
      Py_DECREF(BufferList);
      goto returnNULL;
      }
    PyList_SET_ITEM(BufferList, ii, BufferID);
  }
  free(Buffers);
  return BufferList;
returnNULL:
  free(Buffers);
  return NULL;
}

