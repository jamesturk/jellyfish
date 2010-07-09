#include <Python.h>
#include "jaro.h"

static PyObject * strfry_jaro_winkler(PyObject *self, PyObject *args)
{
    const char *s1, *s2;
    double result;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        return NULL;
    }

    result = jaro_winkler(s1, s2, 0, 1);

    return Py_BuildValue("d", result);
}

static PyMethodDef StrfryMethods[] = {
    {"jaro_winkler", strfry_jaro_winkler, METH_VARARGS,
     "Do a Jaro-Winkler string comparison."},

    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initstrfry(void)
{
    (void)Py_InitModule("strfry", StrfryMethods);
}
