#ifndef __QUEUESINTERFACE_H__
#define __QUEUESINTERFACE_H__
#include <Python.h>

PyObject* _CL_CreateQueue(PyObject* args);
PyObject* _CL_GetQueueProperties(PyObject* args);
PyObject* _CL_RetainQueue(PyObject* args);
PyObject* _CL_ReleaseQueue(PyObject* args);
PyObject* _CL_ListQueues(PyObject* args);
PyObject* _CL_ListQueues(PyObject* args);
PyObject* _CL_EnqueueReadBuffer(PyObject* args);
PyObject* _CL_EnqueueWriteBuffer(PyObject* args);
PyObject* _CL_EnqueueCopyBuffer(PyObject* args);
PyObject* _CL_EnqueueNDRangeKernel(PyObject* args);
PyObject* _CL_EnqueueTask(PyObject* args);
PyObject* _CL_EnqueueBarrier(PyObject* args);
PyObject* _CL_Finish(PyObject* args);

#endif

