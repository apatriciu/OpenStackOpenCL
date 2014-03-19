#include <Python.h>
#include <CL/cl.h>
#include "OpenCLObjectsMaps.h"

PyObject* _CL_CreateKernel(PyObject* args){
  // creates a new OpenCL program; 
  // the arguments are: (programID, kernelName)
  long programID;
  cl_program program;
  char* pKernelName = NULL;
  cl_kernel newKernel;
  long newKernelID;
  cl_int retErr = CL_SUCCESS;

  if(!PyArg_ParseTuple(args, "ls", &programID, &pKernelName) )
    return NULL;
  // retrieve programID
  program = GetProgram(programID);
  if(program == NULL) return NULL;
  // create the new kernel
  newKernel = clCreateKernel(program, pKernelName, &retErr);
  if(retErr != CL_SUCCESS) goto labelRetErr1;
  // insert the new kernel in the map
  if(!InsertKernel(newKernel, &newKernelID)){
    clReleaseKernel(newKernel);
    goto labelRetErr;
  }
  return Py_BuildValue("ii", newKernelID, retErr);
  labelRetErr:
    return NULL;
  labelRetErr1:
    return Py_BuildValue("ii", 0, retErr);
}

PyObject* _CL_GetKernelProperties(PyObject* args){
  // retrieves the properties of context
  // returns a map with properties and the errcode
  cl_int retErr;
  long KernelID;
  cl_kernel localKernel;
  long ContextID;
  long ProgramID;
  cl_context ctx;
  cl_program prog;
  cl_uint nArguments;
  char KernelName[128];

  if(!PyArg_ParseTuple(args, "l", &KernelID)) return NULL;
  // retrieve the cl_program
  localKernel = GetKernel( KernelID );
  if(localKernel == NULL) return NULL;
  retErr = clGetKernelInfo(localKernel, CL_KERNEL_CONTEXT, sizeof(cl_context), &ctx, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  ContextID = GetContextID(ctx);
  retErr = clGetKernelInfo(localKernel, CL_KERNEL_PROGRAM, sizeof(cl_program), &prog, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  ProgramID = GetProgramID(prog);
  retErr = clGetKernelInfo(localKernel, CL_KERNEL_NUM_ARGS, sizeof(cl_uint), &nArguments, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  retErr = clGetKernelInfo(localKernel, CL_KERNEL_FUNCTION_NAME, 128, KernelName, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  return Py_BuildValue("{sisisiss}i","id", KernelID, "Context", ContextID, "Program", ProgramID, "KernelFunctionName", KernelName, retErr);
  retMinimalInfo:
    return Py_BuildValue("{si}i","id", KernelID, retErr);
}

PyObject* _CL_RetainKernel(PyObject* args){
  long KernelID;
  if(!PyArg_ParseTuple(args, "l", &KernelID)) return NULL;
  // retain the cl_context
  if( !RetainKernel( KernelID ) ) return NULL;
  return Py_BuildValue("i", CL_SUCCESS);
}

PyObject* _CL_ReleaseKernel(PyObject* args){
  long KernelID;
  long count;
  if(!PyArg_ParseTuple(args, "l", &KernelID)) return NULL;
  // release the kernel
  count = ReleaseKernel( KernelID );
  return Py_BuildValue("i", count);
}

PyObject* 
_CL_ListKernels(PyObject* args){
  long nKernels;
  long* Kernels = NULL;
  long ii;
  PyObject* KernelList;
  PyObject* KernelID;
  nKernels = GetNumberOfKernels();
  Kernels = (long*)malloc(nKernels * sizeof(long));
  if(Kernels == NULL) goto returnNULL;
  GetKernelsIDs(Kernels);
  KernelList = PyList_New(nKernels);
  if(KernelList == NULL) goto returnNULL;
  for(ii = 0; ii < nKernels; ii++){
    KernelID = PyInt_FromLong(Kernels[ii]);
    if(KernelID == NULL){
      Py_DECREF(KernelList);
      goto returnNULL;
      }
    PyList_SET_ITEM(KernelList, ii, KernelID);
  }
  free(Kernels);
  return KernelList;
returnNULL:
  free(Kernels);
  return NULL;
}

PyObject* _CL_KernelSetArgument(PyObject* args){
  long kernelID;
  cl_uint kernelArgumentIndex;
  cl_kernel Kernel;
  PyObject* pDictParamsObject;
  PyObject* key;
  PyObject* value;
  Py_ssize_t pos = 0;
  cl_int retErr;

  if(!PyArg_ParseTuple(args, "lIO", &kernelID, &kernelArgumentIndex, &pDictParamsObject)) return NULL;
  if(!PyDict_Check(pDictParamsObject)) return NULL;
  // retrieve cl kernel object
  Kernel = GetKernel(kernelID);
  if(Kernel == NULL) return NULL;
  // scan the params dictionary
  while(PyDict_Next(pDictParamsObject, &pos, &key, &value)){
    if(!PyString_Check(key)) return NULL;
    if( !strcmp(PyString_AsString(key), "DeviceMemoryObject") ){
      long memID;
      cl_mem memObj;
      if(!PyInt_Check(value)) return NULL;
      memID = PyInt_AsLong(value);
      memObj = GetMem( memID );
      if(memObj == NULL) return NULL;
      retErr = clSetKernelArg(Kernel, kernelArgumentIndex, sizeof(cl_mem), &memObj);
    } else if( !strcmp(PyString_AsString(key), "LocalMemory") ){
      size_t SharedMemorySize;
      if( !PyInt_Check(value) ) return NULL;
      SharedMemorySize = PyInt_AsSsize_t( value );
      retErr = clSetKernelArg(Kernel, kernelArgumentIndex, SharedMemorySize, NULL);
    } else if( !strcmp(PyString_AsString(key), "HostValue") ){
      char* hostBuffer;
      Py_ssize_t length;
      if( !PyByteArray_Check(value) ) return NULL;
      length = PyByteArray_Size( value );
      hostBuffer = PyByteArray_AsString( value );
      retErr = clSetKernelArg(Kernel, kernelArgumentIndex, length, hostBuffer);
    }
    if(retErr != CL_SUCCESS) return Py_BuildValue("i", retErr);
  }
  return Py_BuildValue("i", CL_SUCCESS);
}

