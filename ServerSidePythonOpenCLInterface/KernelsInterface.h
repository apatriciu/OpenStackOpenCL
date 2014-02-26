#ifndef __KERNELSINTERFACE_H__
#define __KERNELSINTERFACE_H__
#include <Python.h>

PyObject* _CL_CreateKernel(PyObject* args);
PyObject* _CL_GetKernelProperties(PyObject* args);
PyObject* _CL_RetainKernel(PyObject* args);
PyObject* _CL_ReleaseKernel(PyObject* args);
PyObject* _CL_ListKernels(PyObject* args);
PyObject* _CL_KernelSetArgument(PyObject* args);

#endif

  

