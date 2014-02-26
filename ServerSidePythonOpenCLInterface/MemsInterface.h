#ifndef __BUFFERSINTERFACE_H__
#define __BUFFERSINTERFACE_H__
#include <Python.h>

PyObject* _CL_CreateBuffer(PyObject* args);
PyObject* _CL_GetBufferProperties(PyObject* args);
PyObject* _CL_RetainBuffer(PyObject* args);
PyObject* _CL_ReleaseBuffer(PyObject* args);
PyObject* _CL_ListBuffers(PyObject* args);

#endif

  

