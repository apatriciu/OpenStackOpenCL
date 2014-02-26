// ServerSide Python -> OpenCL interface
// Plain translation of python calls into C calls
#include <Python.h>
#include <CL/cl.h>
#include "ContextsInterface.h"
#include "DevicesInterface.h"
#include "KernelsInterface.h"
#include "MemsInterface.h"
#include "ProgramsInterface.h"
#include "QueuesInterface.h"

int InitializePlatformAndDevices(int device_type);

static PyObject* PyOpenCLInterfaceError;

// we asssume that we have a single OpenCL platform
// the platforms are kept in an array

static PyObject*
CL_Initialize(PyObject* self, PyObject* args){
  // sets up the initial platform
  // builds the array of devices
  
  char* deviceOptions;
  int device_type = 0; // 0 -> GPU; 1 -> CPU; 2 -> ALL
  if(PyArg_ParseTuple(args, "s", &deviceOptions)){
    if( !strcmp("GPU", deviceOptions) ) device_type = 0;
    if( !strcmp("CPU", deviceOptions) ) device_type = 1;
    if( !strcmp("ALL", deviceOptions) ) device_type = 2;
  }
  int nErr = InitializePlatformAndDevices(device_type);
  return Py_BuildValue("i", nErr);
}

static PyObject*
CL_ListDevices(PyObject* self, PyObject* args){
  return _CL_GetListDevices(args);
}

static PyObject*
CL_GetDeviceProperties(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_GetDeviceProperties(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_CreateContext(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_CreateContext(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_GetContextProperties(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_GetContextProperties(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_RetainContext(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_RetainContext(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_ReleaseContext(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ReleaseContext(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_ListContexts(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ListContexts(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

// Queue commands

static PyObject*
CL_ListQueues(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ListQueues(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_CreateQueue(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_CreateQueue(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_GetQueueProperties(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_GetQueueProperties(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_RetainQueue(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_RetainQueue(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_ReleaseQueue(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ReleaseQueue(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_EnqueueReadBuffer(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_EnqueueReadBuffer(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_EnqueueWriteBuffer(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_EnqueueWriteBuffer(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_EnqueueCopyBuffer(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_EnqueueCopyBuffer(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_EnqueueNDRangeKernel(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_EnqueueNDRangeKernel(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_EnqueueTask(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_EnqueueTask(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_EnqueueBarrier(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_EnqueueBarrier(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_Finish(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_Finish(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

// program interface
static PyObject*
CL_ListPrograms(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ListPrograms(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_CreateProgram(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_CreateProgram(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_GetProgramProperties(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_GetProgramProperties(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_RetainProgram(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_RetainProgram(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_ReleaseProgram(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ReleaseProgram(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_BuildProgram(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_BuildProgram(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_GetProgramBuildInfo(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_GetProgramBuildInfo(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

// kernels interface
static PyObject*
CL_ListKernels(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ListKernels(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_CreateKernel(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_CreateKernel(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_GetKernelProperties(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_GetKernelProperties(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_RetainKernel(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_RetainKernel(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_ReleaseKernel(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ReleaseKernel(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_KernelSetArgument(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_KernelSetArgument(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

// buffer interface
static PyObject*
CL_ListBuffers(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ListBuffers(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_CreateBuffer(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_CreateBuffer(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_GetBufferProperties(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_GetBufferProperties(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_RetainBuffer(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_RetainBuffer(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyObject*
CL_ReleaseBuffer(PyObject* self, PyObject* args){
  PyObject* retObj = _CL_ReleaseBuffer(args);
  if(retObj == NULL)
    PyErr_SetString(PyOpenCLInterfaceError, "OpenCLInterface Error");
  return retObj;
}

static PyMethodDef PythonOpenCLInterfaceMethods[] = {
  {"Initialize", CL_Initialize , METH_VARARGS, "Initialize the GPU"},
  {"ListDevices", CL_ListDevices, METH_VARARGS, "Retrieves all the devices"},
  {"GetDeviceProperties", CL_GetDeviceProperties, METH_VARARGS, "Retrieves the device properties"},
  {"CreateContext", CL_CreateContext, METH_VARARGS, "Creates a new OpenCL context"},
  {"GetContextProperties", CL_GetContextProperties, METH_VARARGS, "Retrieves the context properties"},
  {"RetainContext", CL_RetainContext, METH_VARARGS, "Retains a context"},
  {"ReleaseContext", CL_ReleaseContext, METH_VARARGS, "Releases a context"},
  {"ListContexts", CL_ListContexts, METH_VARARGS, "Lists all the contexts in the system"},
  {"ListQueues", CL_ListQueues, METH_VARARGS, "Lists all the queues in the system"},
  {"CreateQueue", CL_CreateQueue, METH_VARARGS, "Create a new command queue"},
  {"GetQueueProperties", CL_GetQueueProperties, METH_VARARGS, "Retrieves the command queue properties"},
  {"RetainQueue", CL_RetainQueue, METH_VARARGS, "Retains a queue"},
  {"ReleaseQueue", CL_ReleaseQueue, METH_VARARGS, "Releases a queue"},
  {"EnqueueReadBuffer", CL_EnqueueReadBuffer, METH_VARARGS, "Enqueues a read buffer operation"},
  {"EnqueueWriteBuffer", CL_EnqueueWriteBuffer, METH_VARARGS, "Enqueues a write buffer operation"},
  {"EnqueueCopyBuffer", CL_EnqueueCopyBuffer, METH_VARARGS, "Enqueues a copy buffer operation"},
  {"EnqueueNDRangeKernel", CL_EnqueueNDRangeKernel, METH_VARARGS, "Enqueues an NDRange kernel"},
  {"EnqueueTask", CL_EnqueueTask, METH_VARARGS, "Enqueues a task"},
  {"EnqueueBarrier", CL_EnqueueBarrier, METH_VARARGS, "Enqueues a barrier"},
  {"Finish", CL_Finish, METH_VARARGS, "Wait for all the operations submitted to the queue to finish"},
  {"ListPrograms", CL_ListPrograms, METH_VARARGS, "Lists all the programs on the system"},
  {"CreateProgram", CL_CreateProgram, METH_VARARGS, "Creates a new program"},
  {"GetProgramProperties", CL_GetProgramProperties, METH_VARARGS, "Retrieves the program properties"},
  {"RetainProgram", CL_RetainProgram, METH_VARARGS, "Retains a program"},
  {"ReleaseProgram", CL_ReleaseProgram, METH_VARARGS, "Releases a program"},
  {"BuildProgram", CL_BuildProgram, METH_VARARGS, "Builds a program"},
  {"GetProgramBuildInfo", CL_GetProgramBuildInfo, METH_VARARGS, "Retrieves program build info"},
  {"ListKernels", CL_ListKernels, METH_VARARGS, "Lists all the kernels on the system"},
  {"CreateKernel", CL_CreateKernel, METH_VARARGS, "Creates a new kernel"},
  {"GetKernelProperties", CL_GetKernelProperties, METH_VARARGS, "Retrieves the  kernel properties"},
  {"RetainKernel", CL_RetainKernel, METH_VARARGS, "Retains a kernel"},
  {"ReleaseKernel", CL_ReleaseKernel, METH_VARARGS, "Releases a kernel"},
  {"KernelSetArgument", CL_KernelSetArgument, METH_VARARGS, "Sets a kernel parameter"},
  {"ListBuffers", CL_ListBuffers, METH_VARARGS, "Lists all the memory buffers in the system"},
  {"CreateBuffer", CL_CreateBuffer, METH_VARARGS, "Creates a new memory buffer"},
  {"GetBufferProperties", CL_GetBufferProperties, METH_VARARGS, "Retrieves memory buffer properties"},
  {"RetainBuffer", CL_RetainBuffer, METH_VARARGS, "Retains a memory buffer"},
  {"ReleaseBuffer", CL_ReleaseBuffer, METH_VARARGS, "Releases a memory buffer"},
  {NULL, NULL, 0, NULL} /* sentinel */
};

PyMODINIT_FUNC
initPyOpenCLInterface(void)
{
    PyObject *m;
    m = Py_InitModule("PyOpenCLInterface", PythonOpenCLInterfaceMethods);
    if (m == NULL)
        return;
    PyOpenCLInterfaceError = PyErr_NewException("PyOpenCLInterface.error", NULL, NULL);
    Py_INCREF(PyOpenCLInterfaceError);
    PyModule_AddObject(m, "error", PyOpenCLInterfaceError);
}

