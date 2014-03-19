#include <Python.h>
#include <CL/cl.h>
#include "OpenCLObjectsMaps.h"

PyObject* _CL_CreateProgram(PyObject* args){
  // creates a new OpenCL program; 
  // the arguments are: (contextID, [codestring1, codestring2, ...])
  long contextID;
  cl_context ctx;
  PyObject* pObjListCodeStrings;
  cl_uint nStrings;
  char** programStrings = NULL;
  long ii;
  cl_program newProgram;
  long newProgramID;
  cl_int retErr = CL_SUCCESS;

  if(!PyArg_ParseTuple(args, "lO", &contextID, &pObjListCodeStrings) )
    return NULL;
  // retrieve contextID
  if(!PyList_Check(pObjListCodeStrings)) return NULL;
  ctx = GetContext(contextID);
  if(ctx == NULL) return NULL;
  // retrieve list strings
  nStrings = (cl_uint)PyList_Size(pObjListCodeStrings);
  programStrings = (char**)malloc(nStrings * sizeof(char*));
  if(programStrings == NULL) return NULL;
  for(ii = 0; ii < nStrings; ii++){
    PyObject* listItem;
    listItem = PyList_GetItem(pObjListCodeStrings, ii);
    if(!PyString_Check( listItem )) goto labelRetErr;
    programStrings[ii] = PyString_AsString(listItem);
  }
  // create the new program
  newProgram = clCreateProgramWithSource(ctx, nStrings,(const char**)programStrings, NULL, &retErr);
  if(retErr != CL_SUCCESS) goto labelRetErr1;
  // insert the new program in the map
  if(!InsertProgram(newProgram, &newProgramID)){
    clReleaseProgram(newProgram);
    goto labelRetErr;
  }
  free(programStrings);
  return Py_BuildValue("li", newProgramID, retErr);
  labelRetErr:
    free(programStrings);
    return NULL;
  labelRetErr1:
    free(programStrings);
    return Py_BuildValue("ii", 0, retErr);
}

PyObject* _CL_GetProgramProperties(PyObject* args){
  // retrieves the properties of context
  // returns a map with properties and the errcode
  cl_int retErr;
  long ProgramID;
  cl_program localProgram;
  long *DeviceIDs = NULL;
  cl_uint numDevices;
  cl_device_id* Devices = NULL;
  long contextID;
  cl_context ctx;
  long ii;
  PyObject* deviceList;
  PyObject* deviceID;

  if(!PyArg_ParseTuple(args, "l", &ProgramID)) return NULL;
  // retrieve the cl_program
  localProgram = GetProgram( ProgramID );
  if(localProgram == NULL) return NULL;
  retErr = clGetProgramInfo(localProgram, CL_PROGRAM_CONTEXT, sizeof(cl_context), &ctx, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  contextID = GetContextID(ctx);
  retErr = clGetProgramInfo(localProgram, CL_PROGRAM_NUM_DEVICES, sizeof(cl_uint), &numDevices, NULL);
  if(retErr != CL_SUCCESS) goto retMinimalInfo;
  Devices = (cl_device_id*)malloc(numDevices * sizeof(cl_device_id));
  if(Devices == NULL) goto retMinimalInfo;
  retErr = clGetProgramInfo(localProgram, CL_PROGRAM_DEVICES, numDevices*sizeof(cl_device_id), Devices, NULL);
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
  return Py_BuildValue("{slsOsl}i","id", ProgramID, "Devices", deviceList, "Context", contextID, retErr);
  retMinimalInfo:
    free(DeviceIDs);
    free(Devices);
    return Py_BuildValue("{sl}i","id", ProgramID, retErr);
}

PyObject* _CL_RetainProgram(PyObject* args){
  long ProgramID;
  if(!PyArg_ParseTuple(args, "l", &ProgramID)) return NULL;
  // retain the program
  if( !RetainProgram( ProgramID ) ) return NULL;
  return Py_BuildValue("i", CL_SUCCESS);
}

PyObject* _CL_ReleaseProgram(PyObject* args){
  long ProgramID;
  long count;
  if(!PyArg_ParseTuple(args, "l", &ProgramID)) return NULL;
  // release the program
  count = ReleaseProgram( ProgramID );
  return Py_BuildValue("i", count);
}

PyObject* 
_CL_ListPrograms(PyObject* args){
  long nPrograms;
  long* Programs = NULL;
  long ii;
  PyObject* ProgramList;
  PyObject* ProgramID;
  nPrograms = GetNumberOfPrograms();
  Programs = (long*)malloc(nPrograms * sizeof(long));
  if(Programs == NULL) goto returnNULL;
  GetProgramsIDs(Programs);
  ProgramList = PyList_New(nPrograms);
  if(ProgramList == NULL) goto returnNULL;
  for(ii = 0; ii < nPrograms; ii++){
    ProgramID = PyInt_FromLong(Programs[ii]);
    if(ProgramID == NULL){
      Py_DECREF(ProgramList);
      goto returnNULL;
      }
    PyList_SET_ITEM(ProgramList, ii, ProgramID);
  }
  free(Programs);
  return ProgramList;
returnNULL:
  free(Programs);
  return NULL;
}

PyObject* _CL_BuildProgram(PyObject* args){
  // builds a program; the arguments are as follows
  // (ProgramID, [device0, device1, ...], options)
  long ProgramID;
  cl_program prog;
  PyObject* listDevices;
  char* strOptions;
  Py_ssize_t nDevices;
  Py_ssize_t ii;
  cl_device_id arrayDevices[10];
  long deviceID;
  PyObject* listItem;
  cl_int retErr;

  if(!PyArg_ParseTuple(args, "lOs", &ProgramID, &listDevices, &strOptions)) return NULL;
  if(!PyList_Check(listDevices)) return NULL;
  prog = GetProgram(ProgramID); if(prog == NULL) return NULL;
  // retrieve the list with devices
  nDevices = PyList_Size( listDevices );
  for(ii = 0; ii < nDevices; ii++){
    listItem = PyList_GetItem(listDevices, ii);
    if( !PyInt_Check(listItem) ) return NULL;
    deviceID = PyInt_AsLong(listItem);
    arrayDevices[ii] = GetCLDevice(deviceID);
  }
  retErr = clBuildProgram(prog, nDevices, arrayDevices, strOptions, NULL, NULL);
  return Py_BuildValue("i", retErr);
}

PyObject* _CL_GetProgramBuildInfo(PyObject* args){
  // retrieves the build info for a program
  // the arguments are as follows (ProgramID, DeviceID, ParamName)
  long ProgramID;
  cl_program prog;
  long DeviceID;
  cl_device_id dev;
  char* ParamName;
  cl_int retErr = CL_SUCCESS;

  if( !PyArg_ParseTuple(args, "lls", &ProgramID, &DeviceID, &ParamName) ) return NULL;
  prog = GetProgram(ProgramID); if(prog == NULL) goto labelRetErr;
  dev = GetCLDevice(DeviceID); if(dev == NULL) goto labelRetErr;
  if(!strcmp(ParamName, "CL_PROGRAM_BUILD_STATUS")){
    cl_build_status build_status;
    char strBuildStatus[32];
    retErr = clGetProgramBuildInfo(prog, dev, CL_PROGRAM_BUILD_STATUS, sizeof(cl_build_status), &build_status, NULL);
    if(retErr != CL_SUCCESS) goto labelRetErrCL;
    switch(build_status){
      case CL_BUILD_NONE:
        strcpy(strBuildStatus, "CL_BUILD_NONE");
        break;
      case CL_BUILD_ERROR:
        strcpy(strBuildStatus, "CL_BUILD_ERROR");
        break;
      case CL_BUILD_SUCCESS:
        strcpy(strBuildStatus, "CL_BUILD_SUCCESS");
        break;
    }
    return Py_BuildValue("{ss}i", "CL_PROGRAM_BUILD_STATUS", strBuildStatus, retErr);
  }
  else if( !strcmp(ParamName, "CL_PROGRAM_BUILD_LOG") ){
    char *buildLog = NULL;
    size_t buildLogSize = 0;
    PyObject* retObject;
    retErr = clGetProgramBuildInfo(prog, dev, CL_PROGRAM_BUILD_LOG, buildLogSize, buildLog, &buildLogSize);
    if(retErr != CL_SUCCESS) goto labelRetErrCL;
    buildLog = (char*)malloc(buildLogSize + 1);
    if(buildLog == NULL)
      retObject = Py_BuildValue("{ss}i", "CL_PROGRAM_BUILD_LOG", "Could not build the log", retErr);
    else{
      retErr = clGetProgramBuildInfo(prog, dev, CL_PROGRAM_BUILD_LOG, buildLogSize, buildLog, NULL);
      retObject = Py_BuildValue("{ss}i", "CL_PROGRAM_BUILD_LOG", buildLog, retErr);
      }
    free(buildLog);
    return retObject;
  }
labelRetErrCL:
  return Py_BuildValue("ii", 0, retErr);  
labelRetErr:
  return NULL;
}

