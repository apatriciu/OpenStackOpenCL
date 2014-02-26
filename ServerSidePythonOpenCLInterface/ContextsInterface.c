#include <Python.h>
#include <CL/cl.h>
#include "OpenCLObjectsMaps.h"

PyObject* _CL_CreateContext(PyObject* args){
  // creates a new OpenCL context; 
  // the argument are: ContextProperties dict and device id list
  PyObject* dictContextProperties = NULL;
  PyObject* listDevices = NULL;
  int ii;
  Py_ssize_t nDevices;
  cl_device_id *Devices = NULL;
  cl_device_id dev;
  cl_context_properties *properties = NULL;
  cl_context new_context;
  cl_int ErrCode;

  if(!PyArg_ParseTuple(args, "OO", &listDevices, &dictContextProperties) )
    return NULL;
  // test parameters
  if(!PyList_Check(listDevices)) return NULL;
  // unpack list devices
  nDevices = PyList_Size(listDevices);
  Devices = (cl_device_id*)malloc(nDevices * sizeof(cl_device_id));
  if(Devices == NULL) return NULL;
  for(ii = 0; ii < nDevices; ii++){
    dev = GetCLDevice( PyInt_AsLong( PyList_GET_ITEM(listDevices, ii) ) );
    if(dev == NULL) return NULL;
    Devices[ii] = dev; 
  }
  properties = (cl_context_properties*)malloc(3 * sizeof(cl_context_properties));
  if(properties == NULL) return NULL;
  properties[0] = CL_CONTEXT_PLATFORM;
  properties[1] = (cl_context_properties)GetCLPlatform(0);
  properties[2] = 0;
  // create the context
  new_context = clCreateContext(properties, nDevices, Devices, NULL, NULL, &ErrCode);
  if(ErrCode != CL_SUCCESS) goto returnErr;
  // insert context into the map and retrieve the integer index
  long idContext;
  if( !InsertContext(new_context, &idContext) ){
    clReleaseContext(new_context);
    goto returnErr;
  }
  free(Devices);
  free(properties);  
  return Py_BuildValue("ii", idContext, ErrCode);
  returnErr: 
    free(Devices);
    free(properties);
    return NULL;
}

PyObject* _CL_GetContextProperties(PyObject* args){
  // retrieves the properties of context
  // returns a map with properties and the errcode
  cl_int retErr;
  long ContextID;
  cl_context localContext;
  long *DeviceIDs = NULL;
  cl_uint numDevices;
  cl_device_id* Devices = NULL;
  long ii;
  PyObject* deviceList;
  PyObject* deviceID;

  if(!PyArg_ParseTuple(args, "l", &ContextID)) return NULL;
  // retrieve the cl_context
  localContext = GetContext( ContextID );
  if(localContext == NULL) return NULL;
  retErr = clGetContextInfo(localContext, CL_CONTEXT_NUM_DEVICES, sizeof(cl_uint), &numDevices, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  Devices = (cl_device_id*)malloc(numDevices * sizeof(cl_device_id));
  if(Devices == NULL) goto retMinimalInfo;
  retErr = clGetContextInfo(localContext, CL_CONTEXT_DEVICES, sizeof(cl_device_id), Devices, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  DeviceIDs = (long*)malloc(numDevices * sizeof(long));
  if(DeviceIDs == NULL) goto retMinimalInfo;
  for(ii = 0; ii < numDevices; ii++)
    DeviceIDs[ii] = GetDeviceID(Devices[ii]);
  // build the output
  deviceList = PyList_New(numDevices);
  for(ii = 0; ii < numDevices; ii++){
    deviceID = PyInt_FromLong(DeviceIDs[ii]);
    PyList_SetItem(deviceList, ii, deviceID);
  }
  free(DeviceIDs);
  free(Devices);
  return Py_BuildValue("{sisO}i","id", ContextID, "Devices", deviceList, retErr);
  retMinimalInfo:
    free(DeviceIDs);
    free(Devices);
    return Py_BuildValue("{si}i","id", ContextID, retErr);
}

PyObject* _CL_RetainContext(PyObject* args){
  long ContextID;
  if(!PyArg_ParseTuple(args, "l", &ContextID)) return NULL;
  // retain the cl_context
  if( !RetainContext( ContextID ) ) return NULL;
  return Py_BuildValue("i", CL_SUCCESS);
}

PyObject* _CL_ReleaseContext(PyObject* args){
  long ContextID;
  if(!PyArg_ParseTuple(args, "l", &ContextID)) return NULL;
  // retain the cl_context
  if( !ReleaseContext( ContextID ) ) return NULL;
  return Py_BuildValue("i", CL_SUCCESS);
}

PyObject* 
_CL_ListContexts(PyObject* args){
  long nContexts;
  long* Contexts;
  long ii;
  PyObject* ContextList;
  PyObject* ContextID;
  nContexts = GetNumberOfContexts();
  Contexts = (long*)malloc(nContexts * sizeof(long));
  if(Contexts == NULL) return NULL;
  GetContextsIDs(Contexts);
  ContextList = PyList_New(nContexts);
  if(ContextList == NULL) return NULL;
  for(ii = 0; ii < nContexts; ii++){
    ContextID = PyInt_FromLong(Contexts[ii]);
    if(ContextID == NULL){
      Py_DECREF(ContextList);
      return NULL;
      }
    PyList_SET_ITEM(ContextList, ii, ContextID);
  }
  return ContextList;
}


