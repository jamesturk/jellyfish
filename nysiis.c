#include "jellyfish.h"
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define ISVOWEL(a) ((a) == 'A' || (a) == 'E' || (a) == 'I' || \
                    (a) == 'O' || (a) == 'U')

char *nysiis(const char *str) {
    size_t len = strlen(str);

    char c1, c2, c3;
    char *copy = strdup(str);
    if (!copy) {
        return NULL;
    }

    if (!*copy) {
        return copy;
    }

    char *code = malloc(len + 1 * sizeof(char));
    if (!code) {
        free(copy);
        return NULL;
    }

    char *p, *cp;

    // Step 1
    if (!strncmp(copy, "MAC", 3)) {
        copy[1] = 'C';
    } else if (!strncmp(copy, "KN", 3)) {
        copy[0] = 'N';
    } else if (copy[0] == 'K') {
        copy[0] = 'C';
    } else if (!strncmp(copy, "PH", 2)) {
        copy[0] = 'F';
        copy[1] = 'F';
    } else if (!strncmp(copy, "SCH", 3)) {
        copy[1] = 'S';
        copy[2] = 'S';
    }

    // Step 2
    c1 = copy[len - 1];
    if (c1 == 'E') {
        c2 = copy[len - 2];
        if (c2 == 'E' || c2 == 'I') {
            copy[len - 1] = ' ';
            copy[len - 2] = 'Y';
        }
    } else if (c1 == 'T') {
        c2 = copy[len - 2];
        if (c2 == 'D' || c2 == 'R' || c2 == 'N') {
            copy[len - 1] = ' ';
            copy[len - 2] = 'D';
        }
    } else if (c1 == 'D') {
        c2 = copy[len - 2];
        if (c2 == 'R' || c2 == 'N') {
            copy[len - 1] = ' ';
            copy[len - 2] = 'D';
        }
    }

    cp = code;
    p = copy;

    // Step 3
    *(cp++) = toupper(*(p++));

    while ((c1 = toupper(*p))) {
        if (c1 == ' ') {
            break;
        }

        // Step 5
        switch(c1) {
        case 'E':
            if (toupper(*(p + 1)) == 'V') {
                *cp = 'A';
                *(++cp) = 'F';
                break;
            }
        case 'A':
        case 'I':
        case 'O':
        case 'U':
            *cp = 'A';
            break;
        case 'Q':
            *cp = 'G';
            break;
        case 'Z':
            *cp = 'S';
            break;
        case 'M':
            *cp = 'N';
            break;
        case 'K':
            if (toupper(*(p + 1)) == 'N') {
                *cp = 'N';
            } else {
                *cp = 'C';
            }
            break;
        case 'S':
            if (toupper(*(p + 1)) == 'C' && toupper(*(p + 2)) == 'H') {
                *(cp++) = 'S';
                *(cp++) = 'S';
                *cp = 'S';
                //p += 2;
            } else {
                *cp = 'S';
            }
            break;
        case 'P':
            if (toupper(*(p + 1)) == 'H') {
                *cp = 'F';
                *(++cp) = 'F';
                // p++;
            } else {
                *cp = 'P';
            }
            break;
        case 'H':
            c2 = toupper(*(p + 1));
            c3 = toupper(*(p - 1));
            if (!ISVOWEL(c2) || !ISVOWEL(c3)) {
                *cp = c3;
            } else {
                *cp = 'H';
            }
            break;
        case 'W':
            c2 = toupper(*(p - 1));
            if (ISVOWEL(c2)) {
                *cp = c2;
            } else {
                *cp = 'W';
            }
            break;
        default:
            *cp = toupper(c1);
        }

        // Step 6
        if (*cp != *(cp - 1) || cp == code + 1) {
            cp++;
        }

        p++;
    }

    *cp = '\0';

    // Step 7
    c1 = *(cp - 1);
    if (c1 == 'S') {
        *(--cp) = '\0';
    } else if (c1 == 'Y') {
        if (*(cp - 2) == 'A') {
            *(--cp) = '\0';
            *(--cp) = 'Y';
        }
    }

    // There is no step 8!

    // Step 9
    if (*(cp - 1) == 'A') {
        *(cp - 1) = '\0';
    }

    free(copy);

    return code;
}
