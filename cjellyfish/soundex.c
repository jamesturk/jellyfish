#include "jellyfish.h"
#include <ctype.h>
#include <stdlib.h>

char* soundex(const char *str)
{
    const char *s;
    char c, prev;
    int i;
    char *result = calloc(5, sizeof(char));

    if (!result) {
        return NULL;
    }

    if (!*str) {
        return result;
    }

    prev = '\0';
    for(s = str, i = 1; *s && i < 4; s++) {
        switch(tolower(*s)) {
        case 'b':
        case 'f':
        case 'p':
        case 'v':
            c = '1';
            break;
        case 'c':
        case 'g':
        case 'j':
        case 'k':
        case 'q':
        case 's':
        case 'x':
        case 'z':
            c = '2';
            break;
        case 'd':
        case 't':
            c = '3';
            break;
        case 'l':
            c = '4';
            break;
        case 'm':
        case 'n':
            c = '5';
            break;
        case 'r':
            c = '6';
            break;
        default:
            c = '\0';
        }

        if (c && c != prev && s != str) {
            result[i++] = c;
        }
        prev = c;
    }

    for ( ; i < 4; i++) {
        result[i] = '0';
    }

    result[0] = toupper(*str);

    return result;
}
