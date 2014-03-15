#include "jellyfish.h"
#include <ctype.h>

size_t hamming_distance(const char *s1, const char *s2) {
    unsigned distance = 0;

    for (; *s1 && *s2; s1++, s2++) {
        if (*s1 != *s2) {
            distance++;
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
