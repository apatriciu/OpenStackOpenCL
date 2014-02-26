#ifndef __CONTEXTSINTERFACE_H__
#define __CONTEXTSINTERFACE_H__
#include <Python.h>

PyObject* _CL_CreateContext(PyObject* args);
PyObject* _CL_GetContextProperties(PyObject* args);
PyObject* _CL_RetainContext(PyObject* args);
PyObject* _CL_ReleaseContext(PyObject* args);
PyObject* _CL_ListContexts(PyObject* args);

#endif

