#ifndef _STRFRY_H_
#define _STRFRY_H_

#include <stdbool.h>

double jaro_winkler(const char *str1, const char *str2, bool ignore_case,
                    bool long_tolerance);
double jaro_distance(const char *str1, const char *str2, bool ignore_case);

unsigned hamming_distance(const char *str1, const char *str2, bool ignore_case);

unsigned levenshtein_distance(const char *str1, const char *str2);

#endif
