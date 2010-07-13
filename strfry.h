#ifndef _STRFRY_H_
#define _STRFRY_H_

#include <stdbool.h>
#include <stdlib.h>

#ifndef MIN
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#endif

double jaro_winkler(const char *str1, const char *str2, bool long_tolerance);
double jaro_distance(const char *str1, const char *str2);

size_t hamming_distance(const char *str1, const char *str2);

int levenshtein_distance(const char *str1, const char *str2);

int damerau_levenshtein_distance(const char *str1, const char *str2);

char* soundex(const char *str);

char* metaphone(const char *str);

#endif
