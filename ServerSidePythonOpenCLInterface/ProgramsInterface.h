#ifndef __PROGRAMSINTERFACE_H__
#define __PROGRAMSINTERFACE_H__
#include <Python.h>

PyObject* _CL_CreateProgram(PyObject* args);
PyObject* _CL_GetProgramProperties(PyObject* args);
PyObject* _CL_RetainProgram(PyObject* args);
PyObject* _CL_ReleaseProgram(PyObject* args);
PyObject* _CL_ListPrograms(PyObject* args);
PyObject* _CL_BuildProgram(PyObject* args);
PyObject* _CL_GetProgramBuildInfo(PyObject* args);

#endif

  

