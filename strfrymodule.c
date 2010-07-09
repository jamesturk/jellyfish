#include <Python.h>
#include "jaro.h"

static PyObject * strfry_jaro_winkler(PyObject *self, PyObject *args,
    PyObject *keywds)
{
    const char *s1, *s2;
    double result;
    bool ignore_case = true;

    static char *kwlist[] = {"string1", "string2", "ignore_case", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "ss|B", kwlist, &s1, &s2,
                                     &ignore_case)) {
        return NULL;
    }

    result = jaro_winkler(s1, s2, ignore_case, true);

    return Py_BuildValue("d", result);
}

static PyMethodDef StrfryMethods[] = {
    {"jaro_winkler", strfry_jaro_winkler, METH_VARARGS | METH_KEYWORDS,
     "jaro_winkler(string1, string2, ignore_case=True)\n\n"
     "Do a Jaro-Winkler string comparison between string1 and string2."},

    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initstrfry(void)
{
    (void)Py_InitModule("strfry", StrfryMethods);
}
