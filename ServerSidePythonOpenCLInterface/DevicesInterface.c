#include <Python.h>
#include <CL/cl.h>
#include "OpenCLObjectsMaps.h"

PyObject* _CL_GetListDevices(PyObject* args){
  // returns all the GPU devices on the system
  cl_int nErr = 0;
  PyObject* listDevices;
  PyObject* item;
  int nDev;
  long arrDev[128];

  nDev = GetNumberOfDevices();
  GetDevicesIds(arrDev);
  listDevices = PyList_New( nDev );
  int ii;
  for(ii = 0; ii < nDev; ii++){
    item = Py_BuildValue("l", arrDev[ii]);
    PyList_SET_ITEM(listDevices, ii, item);
  }
  return Py_BuildValue("Oi", listDevices, nErr);
}

PyObject* _CL_GetDeviceProperties(PyObject* args){
  cl_int nErr = 0;
  long DeviceID;

  if( !PyArg_ParseTuple(args, "l", &DeviceID) )
    return NULL;

  char szDeviceName[256];
  szDeviceName[0] = 0;
  size_t szRetValue;
  cl_device_id dev;
  dev = GetCLDevice(DeviceID);
  if(dev == NULL) return NULL;
  if( clGetDeviceInfo(dev, CL_DEVICE_NAME,
	256, szDeviceName, &szRetValue) != CL_SUCCESS ) goto retMinInfo;
   
  cl_uint nComputeUnits;
  if( clGetDeviceInfo(dev, CL_DEVICE_MAX_COMPUTE_UNITS,
			 sizeof(cl_uint), &nComputeUnits, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  size_t nMaxWorkGroupSize;
  if( clGetDeviceInfo(dev, CL_DEVICE_MAX_WORK_GROUP_SIZE,
			 sizeof(size_t), &nMaxWorkGroupSize, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  cl_ulong nMaxMemAllocationSize;
  if( clGetDeviceInfo(dev, CL_DEVICE_MAX_MEM_ALLOC_SIZE, sizeof(cl_ulong),
		  &nMaxMemAllocationSize, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  cl_ulong nGlobalMemorySize;
  if( clGetDeviceInfo(dev, CL_DEVICE_GLOBAL_MEM_SIZE, sizeof(cl_ulong),
			&nGlobalMemorySize, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  cl_device_local_mem_type LocalMemoryType;
  if( clGetDeviceInfo(dev, CL_DEVICE_LOCAL_MEM_TYPE, sizeof(cl_device_local_mem_type),
			&LocalMemoryType, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  char szLocalMemoryType[16];
  strcpy(szLocalMemoryType, "CL_NONE");
  switch(LocalMemoryType){
    case CL_LOCAL:
      strcpy(szLocalMemoryType, "CL_LOCAL");
      break;
    case CL_GLOBAL:
      strcpy(szLocalMemoryType, "CL_GLOBAL");
      break;
  }
  cl_ulong nLocalMemorySize;
  if( clGetDeviceInfo(dev, CL_DEVICE_LOCAL_MEM_SIZE, sizeof(cl_ulong),
			&nLocalMemorySize, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  cl_bool bDeviceAvailable;
  if( clGetDeviceInfo(dev, CL_DEVICE_AVAILABLE, sizeof(cl_bool),
			&bDeviceAvailable, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  cl_bool bEndianLittle;
  if( clGetDeviceInfo(dev, CL_DEVICE_ENDIAN_LITTLE, sizeof(cl_bool),
                        &bEndianLittle, &szRetValue) != CL_SUCCESS )
    goto retMinInfo;
  retMinInfo:
  return Py_BuildValue("({sisssIsnsksksssksIsI}i)", "id", DeviceID, "CL_DEVICE_NAME", szDeviceName,
                                    "CL_DEVICE_MAX_COMPUTE_UNITS", nComputeUnits,
                                    "CL_DEVICE_MAX_WORK_GROUP_SIZE", nMaxWorkGroupSize,
                                    "CL_DEVICE_MAX_MEM_ALLOC_SIZE", nMaxMemAllocationSize,
                                    "CL_DEVICE_GLOBAL_MEM_SIZE", nGlobalMemorySize,
                                    "CL_DEVICE_LOCAL_MEM_TYPE", szLocalMemoryType,
                                    "CL_DEVICE_LOCAL_MEM_SIZE", nLocalMemorySize,
                                    "CL_DEVICE_AVAILABLE", bDeviceAvailable,
                                    "CL_DEVICE_ENDIAN_LITTLE", bEndianLittle,
                                    nErr);
}

