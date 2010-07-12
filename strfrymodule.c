#include <Python.h>
#include "strfry.h"

struct strfry_state {
    PyObject *unicodedata_normalize;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct strfry_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct strfry_state _state;
#endif

#if PY_MAJOR_VERSION >= 3
#define UTF8_BYTES(s) (PyBytes_AsString(s))
#else
#define UTF8_BYTES(s) (PyString_AS_STRING(s))
#endif

/* Returns a new reference to a PyString (python < 3) or
 * PyBytes (python >= 3.0).
 *
 * If passed a PyUnicode, the returned object will be NFKD UTF-8.
 * If passed a PyString or PyBytes no conversion is done.
 */
static inline PyObject* normalize(PyObject *mod, PyObject *pystr) {
    PyObject *unicodedata_normalize;
    PyObject *normalized;
    PyObject *utf8;

#if PY_MAJOR_VERSION < 3
    if (PyString_Check(pystr)) {
        Py_INCREF(pystr);
        return pystr;
    }
#else
    if (PyBytes_Check(pystr)) {
        Py_INCREF(pystr);
        return pystr;
    }
#endif

    if (PyUnicode_Check(pystr)) {
        unicodedata_normalize = GETSTATE(mod)->unicodedata_normalize;
        normalized = PyObject_CallFunction(unicodedata_normalize,
                                           "sO", "NFKD", pystr);
        if (!normalized) {
            return NULL;
        }
        utf8 = PyUnicode_AsUTF8String(normalized);
        Py_DECREF(normalized);
        return utf8;
    }

    PyErr_SetString(PyExc_TypeError, "expected str or unicode");
    return NULL;
}

static PyObject * strfry_jaro_winkler(PyObject *self, PyObject *args,
    PyObject *keywds)
{
    const char *s1, *s2;
    double result;

    static char *kwlist[] = {"string1", "string2", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "ss", kwlist, &s1, &s2)) {
        return NULL;
    }

    result = jaro_winkler(s1, s2, false);

    return Py_BuildValue("d", result);
}

static PyObject * strfry_jaro_distance(PyObject *self, PyObject *args,
    PyObject *keywds)
{
    const char *s1, *s2;
    double result;

    static char *kwlist[] = {"string1", "string2", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "ss|B", kwlist, &s1, &s2)) {
        return NULL;
    }

    result = jaro_distance(s1, s2);

    return Py_BuildValue("d", result);
}

static PyObject * strfry_hamming_distance(PyObject *self, PyObject *args,
                                          PyObject *keywds)
{
    const char *s1, *s2;
    unsigned result;
    bool ignore_case = true;

    static char *kwlist[] = {"string1", "string2", "ignore_case", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "ss|B", kwlist, &s1, &s2,
                                     &ignore_case)) {
        return NULL;
    }

    result = hamming_distance(s1, s2, ignore_case);

    return Py_BuildValue("I", result);
}

static PyObject* strfry_levenshtein_distance(PyObject *self, PyObject *args)
{
    const char *s1, *s2;
    unsigned result;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        return NULL;
    }

    result = levenshtein_distance(s1, s2);

    return Py_BuildValue("I", result);
}

static PyObject* strfry_soundex(PyObject *self, PyObject *args)
{
    PyObject *pystr;
    PyObject *normalized;
    PyObject* ret;
    char *result;

    if (!PyArg_ParseTuple(args, "O", &pystr)) {
        return NULL;
    }

    normalized = normalize(self, pystr);
    result = soundex(UTF8_BYTES(normalized));
    ret = Py_BuildValue("s", result);
    free(result);
    Py_DECREF(normalized);

    return ret;
}

static PyObject* strfry_metaphone(PyObject *self, PyObject *args)
{
    PyObject *pystr;
    PyObject *normalized;
    PyObject *ret;
    char *result;

    if (!PyArg_ParseTuple(args, "O", &pystr)) {
        return NULL;
    }

    normalized = normalize(self, pystr);
    result = metaphone((const char*)UTF8_BYTES(normalized));
    ret = Py_BuildValue("s", result);
    free(result);
    Py_DECREF(normalized);

    return ret;
}

static PyMethodDef strfry_methods[] = {
    {"jaro_winkler", strfry_jaro_winkler, METH_VARARGS | METH_KEYWORDS,
     "jaro_winkler(string1, string2, ignore_case=True)\n\n"
     "Do a Jaro-Winkler string comparison between string1 and string2."},

    {"jaro_distance", strfry_jaro_distance, METH_VARARGS | METH_KEYWORDS,
     "jaro_distance(string1, string2, ignore_case=True)\n\n"
     "Get a Jaro string distance metric for string1 and string2."},

    {"hamming_distance", strfry_hamming_distance, METH_VARARGS | METH_KEYWORDS,
     "hamming_distance(string1, string2, ignore_case=True)\n\n"
     "Compute the Hamming distance between string1 and string2."},

    {"levenshtein_distance", strfry_levenshtein_distance, METH_VARARGS,
     "levenshtein_distance(string1, string2)\n\n"
     "Compute the Levenshtein distance between string1 and string2."},

    {"soundex", strfry_soundex, METH_VARARGS,
     "soundex(string)\n\n"
     "Calculate the soundex code for a given name."},

    {"metaphone", strfry_metaphone, METH_VARARGS,
     "metaphone(string)\n\n"
     "Calculate the metaphone representation of a given string."},

    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
#define INITERROR return NULL

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "strfry",
    NULL,
    sizeof(struct strfry_state),
    strfry_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyObject* PyInit_strfry(void)
#else

#define INITERROR return

PyMODINIT_FUNC initstrfry(void)
#endif
{
    PyObject *unicodedata;

#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("strfry", strfry_methods);
#endif

    if (module == NULL) {
        INITERROR;
    }

    unicodedata = PyImport_ImportModule("unicodedata");
    if (!unicodedata) {
        INITERROR;
    }

    GETSTATE(module)->unicodedata_normalize =
        PyObject_GetAttrString(unicodedata, "normalize");
    Py_DECREF(unicodedata);

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
