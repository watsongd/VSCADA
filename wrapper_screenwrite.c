#include <Python.h>
#include "screenwrite.h"

static PyObject* wrap_writeToScreen(PyObject* self, PyObject* args)
{
	//store the args
	int row;
	char *message;

	//get the args
	PyArg_ParseTuple(args, "is", &row, &message);

  	//run funct
  	writeToScreen(row, message);

  	return Py_BuildValue("s", "Success");
}

static PyMethodDef DashboardMethods[] = {
    {"writeToScreen", wrap_writeToScreen, METH_VARARGS},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef dashboardmodule = {
   PyModuleDef_HEAD_INIT,
   "screenwrite",   /* name of module */
   NULL,   /* module documentation, may be NULL */
   -1,     /* size of per-interpreter state of the module,
              or -1 if the module keeps state in global variables. */
   DashboardMethods
};

PyMODINIT_FUNC
PyInit_screenwrite(void)
{
    return PyModule_Create(&dashboardmodule);
}

// gcc -Isrc -fPIC $(pkg-config --cflags --libs python3) -c src/screenwrite.c wrapper_screenwrite.c
// gcc -shared -fPIC -o screenwrite.so screenwrite.o wrapper_screenwrite.o
