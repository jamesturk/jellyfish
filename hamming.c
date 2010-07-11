#include "strfry.h"
#include <ctype.h>

unsigned hamming_distance(const char *s1, const char *s2, bool ignore_case) {
    unsigned distance = 0;

    if (ignore_case) {
        for ( ; *s1 && *s2; s1++, s2++) {
            if (tolower(*s1) != tolower(*s2)) {
                distance++;
            }
        }
    } else {
        for (; *s1 && *s2; s1++, s2++) {
            if (*s1 != *s2) {
                distance++;
            }
        }
    }

    for ( ; *s1; s1++) {
        distance++;
    }

    for ( ; *s2; s2++) {
        distance++;
    }

    return distance;
}
