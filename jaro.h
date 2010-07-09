#ifndef _JARO_H_
#define _JARO_H_

#include <stdbool.h>

double jaro_winkler(const char *str1, const char *str2, bool ignore_case,
                    bool long_tolerance);

#endif
