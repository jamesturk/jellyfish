#include <Python.h>
#include <math.h>
#include "jellyfish.h"

struct jellyfish_state {
    PyObject *unicodedata_normalize;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct jellyfish_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct jellyfish_state _state;
#endif

#if PY_MAJOR_VERSION >= 3
#define UTF8_BYTES(s) (PyBytes_AS_STRING(s))
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

static PyObject * jellyfish_jaro_winkler(PyObject *self, PyObject *args,
    PyObject *keywds)
{
    const char *s1, *s2;
    double result;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        return NULL;
    }

    result = jaro_winkler(s1, s2, false);
    if (isnan(result)) {
        PyErr_NoMemory();
        return NULL;
    }

    return Py_BuildValue("d", result);
}

static PyObject * jellyfish_jaro_distance(PyObject *self, PyObject *args,
    PyObject *keywds)
{
    const char *s1, *s2;
    double result;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        return NULL;
    }

    result = jaro_distance(s1, s2);
    if (isnan(result)) {
        PyErr_NoMemory();
        return NULL;
    }

    return Py_BuildValue("d", result);
}

static PyObject * jellyfish_hamming_distance(PyObject *self, PyObject *args,
                                          PyObject *keywds)
{
    const char *s1, *s2;
    unsigned result;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        return NULL;
    }

    result = hamming_distance(s1, s2);

    return Py_BuildValue("I", result);
}

static PyObject* jellyfish_levenshtein_distance(PyObject *self, PyObject *args)
{
    const char *s1, *s2;
    int result;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        return NULL;
    }

    result = levenshtein_distance(s1, s2);
    if (result == -1) {
        // levenshtein_distance only returns failure code (-1) on
        // failed malloc
        PyErr_NoMemory();
        return NULL;
    }

    return Py_BuildValue("i", result);
}

static PyObject* jellyfish_damerau_levenshtein_distance(PyObject *self,
                                                     PyObject *args)
{
    const char *s1, *s2;
    int result;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        return NULL;
    }

    result = damerau_levenshtein_distance(s1, s2);
    if (result == -1) {
        PyErr_NoMemory();
        return NULL;
    }

    return Py_BuildValue("i", result);
}

static PyObject* jellyfish_soundex(PyObject *self, PyObject *args)
{
    PyObject *pystr;
    PyObject *normalized;
    PyObject* ret;
    char *result;

    if (!PyArg_ParseTuple(args, "O", &pystr)) {
        return NULL;
    }

    normalized = normalize(self, pystr);
    if (!normalized) {
        return NULL;
    }

    result = soundex(UTF8_BYTES(normalized));
    Py_DECREF(normalized);

    if (!result) {
        // soundex only fails on bad malloc
        PyErr_NoMemory();
        return NULL;
    }

    ret = Py_BuildValue("s", result);
    free(result);

    return ret;
}

static PyObject* jellyfish_metaphone(PyObject *self, PyObject *args)
{
    PyObject *pystr;
    PyObject *normalized;
    PyObject *ret;
    char *result;

    if (!PyArg_ParseTuple(args, "O", &pystr)) {
        return NULL;
    }

    normalized = normalize(self, pystr);
    if (!normalized) {
        return NULL;
    }

    result = metaphone((const char*)UTF8_BYTES(normalized));
    Py_DECREF(normalized);

    if (!result) {
        // metaphone only fails on bad malloc
        PyErr_NoMemory();
        return NULL;
    }

    ret = Py_BuildValue("s", result);
    free(result);

    return ret;
}

static PyObject* jellyfish_match_rating_codex(PyObject *self, PyObject *args)
{
    const char *str;
    char *result;
    PyObject *ret;

    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }

    result = match_rating_codex(str);
    if (!result) {
        PyErr_NoMemory();
        return NULL;
    }

    ret = Py_BuildValue("s", result);
    free(result);

    return ret;
}

static PyObject* jellyfish_match_rating_comparison(PyObject *self,
                                                   PyObject *args)
{
    const char *str1, *str2;
    int result;

    if (!PyArg_ParseTuple(args, "ss", &str1, &str2)) {
        return NULL;
    }

    result = match_rating_comparison(str1, str2);
    if (result == -1) {
        PyErr_NoMemory();
        return NULL;
    }

    if (result) {
        return Py_True;
    } else {
        return Py_False;
    }
}

static PyObject* jellyfish_nysiis(PyObject *self, PyObject *args)
{
    const char *str;
    char *result;
    PyObject *ret;

    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }

    result = nysiis(str);
    if (!result) {
        PyErr_NoMemory();
        return NULL;
    }

    ret = Py_BuildValue("s", result);
    free(result);

    return ret;
}

static PyObject* jellyfish_porter_stem(PyObject *self, PyObject *args)
{
    const char *str;
    char *result;
    PyObject *ret;
    struct stemmer *z;
    int end;

    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }

    z = create_stemmer();
    if (!z) {
        PyErr_NoMemory();
        return NULL;
    }

    result = strdup(str);
    if (!result) {
        free_stemmer(z);
        PyErr_NoMemory();
        return NULL;
    }

    end = stem(z, result, strlen(result) - 1);
    result[end + 1] = '\0';

    ret = Py_BuildValue("s", result);

    free(result);
    free_stemmer(z);

    return ret;
}

static PyMethodDef jellyfish_methods[] = {
    {"jaro_winkler", jellyfish_jaro_winkler, METH_VARARGS,
     "jaro_winkler(string1, string2, ignore_case=True)\n\n"
     "Do a Jaro-Winkler string comparison between string1 and string2."},

    {"jaro_distance", jellyfish_jaro_distance, METH_VARARGS,
     "jaro_distance(string1, string2, ignore_case=True)\n\n"
     "Get a Jaro string distance metric for string1 and string2."},

    {"hamming_distance", jellyfish_hamming_distance, METH_VARARGS,
     "hamming_distance(string1, string2, ignore_case=True)\n\n"
     "Compute the Hamming distance between string1 and string2."},

    {"levenshtein_distance", jellyfish_levenshtein_distance, METH_VARARGS,
     "levenshtein_distance(string1, string2)\n\n"
     "Compute the Levenshtein distance between string1 and string2."},

    {"damerau_levenshtein_distance", jellyfish_damerau_levenshtein_distance,
     METH_VARARGS,
     "damerau_levenshtein_distance(string1, string2)\n\n"
     "Compute the Damerau-Levenshtein distance between string1 and string2."},

    {"soundex", jellyfish_soundex, METH_VARARGS,
     "soundex(string)\n\n"
     "Calculate the soundex code for a given name."},

    {"metaphone", jellyfish_metaphone, METH_VARARGS,
     "metaphone(string)\n\n"
     "Calculate the metaphone representation of a given string."},

    {"match_rating_codex", jellyfish_match_rating_codex, METH_VARARGS,
     "match_rating_codex(string)\n\n"
     "Calculate the Match Rating Approach representation of a given string."},

    {"match_rating_comparison", jellyfish_match_rating_comparison, METH_VARARGS,
     "match_rating_comparison(string)\n\n"
     "Compute the Match Rating Approach similarity between string1 and"
     "string2."},

    {"nysiis", jellyfish_nysiis, METH_VARARGS,
     "nysiis(string)\n\n"
     "Compute the NYSIIS (New York State Identification and Intelligence\n"
     "System) code for a string."},

    {"porter_stem", jellyfish_porter_stem, METH_VARARGS,
     "porter_stem(string)\n\n"
     "Return the result of running the Porter stemming algorithm on "
     "a single-word string."},

    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
#define INITERROR return NULL

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "strfry",
    NULL,
    sizeof(struct jellyfish_state),
    jellyfish_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyObject* PyInit_jellyfish(void)
#else

#define INITERROR return

PyMODINIT_FUNC initjellyfish(void)
#endif
{
    PyObject *unicodedata;

#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("jellyfish", jellyfish_methods);
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
