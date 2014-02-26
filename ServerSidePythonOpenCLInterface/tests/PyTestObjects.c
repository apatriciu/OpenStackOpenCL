// ServerSide Python -> OpenCL interface
// Plain translation of python calls into C calls
#include <Python.h>

static PyObject* PyTestObjectsError;

static PyObject*
LongAsByteArray(PyObject* self, PyObject* args){
  long lValue;
  PyObject* pObjByteArray;
  if( !PyArg_ParseTuple(args, "l", &lValue) ) return NULL;
  pObjByteArray = PyByteArray_FromStringAndSize((const char*)&lValue, sizeof(long));
  if(pObjByteArray == NULL) return NULL;
  return pObjByteArray;
}

static PyObject*
ByteArrayAsLong(PyObject* self, PyObject* args){
  long lValue;
  PyObject* pObjByteArray;
  if( !PyArg_ParseTuple(args, "O", &pObjByteArray) ) return NULL;
  if( !PyByteArray_Check( pObjByteArray ) ){
    PyErr_SetString(PyTestObjectsError, "TestObjects Error");
    return NULL;
  }
  memcpy((void*)&lValue, PyByteArray_AsString(pObjByteArray), sizeof(long));
  return Py_BuildValue("l", lValue);
}

static PyObject*
ByteArrayAsVar(PyObject* self, PyObject* args){
  // converts a bytearray into a variable
  // parameters (bytearray, format_string)
  // returns the variable
  PyObject* pObjInput;
  char *strFormat;
  
  if(!PyArg_ParseTuple(args, "Os", &pObjInput, &strFormat)){
    PyErr_SetString(PyTestObjectsError, "Parameter Error");
    return NULL;
  }
  if(!PyByteArray_Check(pObjInput)){
    PyErr_SetString(PyTestObjectsError, "Parameter Error");
    return NULL;
  }
  PyObject* retValue = NULL;
  switch(strFormat[0]){
    case 'i' :{
      int lValue = 0;
      memcpy((void*)&lValue, PyByteArray_AsString(pObjInput), sizeof(int));
      retValue = Py_BuildValue("i", lValue);
      break;
    }
    case 'l' :{
      long lValue = 0;
      memcpy((void*)&lValue, PyByteArray_AsString(pObjInput), sizeof(long));
      retValue = Py_BuildValue("l", lValue);
      break;
    }
    case 'I' :{
      unsigned int lValue = 0;
      memcpy((void*)&lValue, PyByteArray_AsString(pObjInput), sizeof(unsigned int));
      retValue = Py_BuildValue("I", lValue);
      break;
    }
    case 'k' :{
      unsigned long lValue = 0;
      memcpy((void*)&lValue, PyByteArray_AsString(pObjInput), sizeof(unsigned long));
      retValue = Py_BuildValue("k", lValue);
      break;
    }
    case 'f' :{
      float lValue = 0;
      memcpy((void*)&lValue, PyByteArray_AsString(pObjInput), sizeof(float));
      retValue = Py_BuildValue("f", lValue);
      break;
    }
    case 'd' :{
      double lValue = 0;
      memcpy((void*)&lValue, PyByteArray_AsString(pObjInput), sizeof(double));
      retValue = Py_BuildValue("d", lValue);
      break;
    }
  }
  if(retValue == NULL)
    PyErr_SetString(PyTestObjectsError, "Parameter Error");
  return retValue;
}

static PyObject*
VarAsByteArray(PyObject* self, PyObject* args){
  // converts a variable into a bytearray
  // parameters (var, format_string)
  // returns the bytearray

  PyObject* pObjVar;
  char* strFormat;
  if( !PyArg_ParseTuple(args, "Os", &pObjVar, &strFormat) ){
    PyErr_SetString(PyTestObjectsError, "Parameter Error");
    return NULL;
  }

  PyObject* retValue = NULL;
  switch(strFormat[0]){
    case 'i' :{
      int lValue = 0;
      if( !PyInt_Check(pObjVar) ) break;
      lValue = (int)PyInt_AsLong( pObjVar );
      retValue = PyByteArray_FromStringAndSize((const char*)&lValue, sizeof(int));
      break;
    }
    case 'l' :{
      long lValue = 0;
      if( !PyInt_Check(pObjVar) ) break;
      lValue = PyInt_AsLong( pObjVar );
      retValue = PyByteArray_FromStringAndSize((const char*)&lValue, sizeof(long));
      break;
    }
    case 'I' :{
      unsigned int lValue = 0;
      if( !PyInt_Check(pObjVar) ) break;
      lValue = (unsigned int)PyInt_AsUnsignedLongMask( pObjVar );
      retValue = PyByteArray_FromStringAndSize((const char*)&lValue, sizeof(unsigned int));
      break;
    }
    case 'k' :{
      unsigned long lValue = 0;
      if( !PyInt_Check(pObjVar) ) break;
      lValue = PyInt_AsUnsignedLongMask( pObjVar );
      retValue = PyByteArray_FromStringAndSize((const char*)&lValue, sizeof(unsigned long));
      break;
    }
    case 'f' :{
      float lValue = 0;
      if( !PyFloat_Check(pObjVar) ) break;
      lValue = (float)PyFloat_AsDouble( pObjVar );
      retValue = PyByteArray_FromStringAndSize((const char*)&lValue, sizeof(float));
      break;
    }
    case 'd' :{
      double lValue = 0;
      if( !PyFloat_Check(pObjVar) ) break;
      lValue = PyFloat_AsDouble( pObjVar );
      retValue = PyByteArray_FromStringAndSize((const char*)&lValue, sizeof(double));
      break;
    }
  }
  if(retValue == NULL)
    PyErr_SetString(PyTestObjectsError, "Parameter Error");
  return retValue;
}

static PyMethodDef TestObjectsMethods[] = {
  {"LongAsByteArray", LongAsByteArray, METH_VARARGS, "Converts a long into a bytearray"},
  {"ByteArrayAsLong", ByteArrayAsLong, METH_VARARGS, "converts a bytearray into a long"},
  {"VarAsByteArray", VarAsByteArray, METH_VARARGS, "Converts a variable into a bytearray"},
  {"ByteArrayAsVar", ByteArrayAsVar, METH_VARARGS, "converts a bytearray into a variable"},
  {NULL, NULL, 0, NULL} /* sentinel */
};

PyMODINIT_FUNC
initPyTestObjects(void)
{
    PyObject *m;
    m = Py_InitModule("PyTestObjects", TestObjectsMethods);
    if (m == NULL)
        return;
    PyTestObjectsError = PyErr_NewException("PyTestObjects.error", NULL, NULL);
    Py_INCREF(PyTestObjectsError);
    PyModule_AddObject(m, "error", PyTestObjectsError);
}

