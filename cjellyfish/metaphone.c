#include "jellyfish.h"
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define ISVOWEL(a) ((a) == 'a' || (a) == 'e' || (a) == 'i' || \
                    (a) == 'o' || (a) == 'u')

char* metaphone(const char *str)
{
    const char *s;
    char c, next, nextnext, temp = '\0';

    // Worst case (a string of all x's) will result in a
    // metaphone twice as large as the original string
    char *result = calloc(strlen(str) * 2 + 1, sizeof(char));
    char *r;

    if (!result) {
        return NULL;
    }

    c = tolower(*str);
    if (c) {
        next = tolower(*(str + 1));

        if ((c == 'k' && next == 'n') ||
            (c == 'g' && next == 'n') ||
            (c == 'p' && next == 'n') ||
            (c == 'a' && next == 'c') ||
            (c == 'w' && next == 'r') ||
            (c == 'a' && next == 'e')) {
            str++;
        }
    }


    next = tolower(*str);
    for (s = str, r = result; next; s++) {
        c = next;
        next = tolower(*(s + 1));
        nextnext = tolower(*(s + 2));

        if (c == next && c != 'c') {
            continue;
        }

        switch(c) {
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
            if (s == str || *(s - 1) == ' ') {
                *r++ = toupper(c);
            }
            break;
        case 'b':
            if (!(s > str && tolower(*(s - 1)) == 'm') || next) {
                *r++ = 'B';
            }
            break;
        case 'c':
            if ((next == 'i' && nextnext == 'a') || next == 'h') {
                *r++ = 'X';
                next = tolower(*(++s + 1));
            } else if (next == 'i' || next == 'e' || next == 'y') {
                *r++ = 'S';
                next = tolower(*(++s + 1));
            } else {
                *r++ = 'K';
            }
            break;
        case 'd':
            if (next == 'g' && (nextnext == 'e' || nextnext == 'y' ||
                                nextnext == 'i')) {
                *r++ = 'J';
                s += 2;
                next = tolower(*(s + 1));
            } else {
                *r++ = 'T';
            }
            break;
        case 'f':
            *r++ = 'F';
            break;
        case 'g':
            if (next == 'i' || next == 'e' || next == 'y') {
                *r++ = 'J';
            } else if(next != 'h' && next != 'n') {
                *r++ = 'K';
            } else if(next == 'h' && !(ISVOWEL(nextnext))) {
                s++;
                next = tolower(*(s + 1));
            }
            break;
        case 'h':
            if (s == str || ISVOWEL(next) || (temp = tolower(*(s - 1)) &&
                                              ISVOWEL(temp))) {
                *r++ = 'H';
            }
            break;
        case 'j':
            *r++ = 'J';
            break;
        case 'k':
            if (s == str || tolower(*(s - 1)) != 'c') {
                *r++ = 'K';
            }
            break;
        case 'l':
            *r++ = 'L';
            break;
        case 'm':
            *r++ = 'M';
            break;
        case 'n':
            *r++ = 'N';
            break;
        case 'p':
            if (next == 'h') {
                *r++ = 'F';
                next = tolower(*(++s + 1));
            } else {
                *r++ = 'P';
            }
            break;
        case 'q':
            *r++ = 'K';
            break;
        case 'r':
            *r++ = 'R';
            break;
        case 's':
            if (next == 'h') {
                *r++ = 'X';
                next = tolower(*(++s + 1));
            } else if (next == 'i' && (nextnext == 'o' || nextnext == 'a')) {
                *r++ = 'X';
                s += 2;
                next = tolower(*(s + 1));
            } else {
                *r++ = 'S';
            }
            break;
        case 't':
            if (next == 'i' && (nextnext == 'a' || nextnext == 'o')) {
                *r++ = 'X';
            } else if(next == 'h') {
                *r++ = '0';
                next = tolower(*(++s + 1));
            } else if(next != 'c' || nextnext != 'h') {
                *r++ = 'T';
            }
            break;
        case 'v':
            *r++ = 'F';
            break;
        case 'w':
            if (s == str && next == 'h') {
                next = tolower(*(++s + 1));
            }
            if (ISVOWEL(next)) {
                *r++ = 'W';
            }
            break;
        case 'x':
            if (s == str) {
                if (next == 'h' || (next == 'i' && (nextnext == 'o' || nextnext == 'a'))) {
                    *r++ = 'X';
                } else {
                    *r++ = 'S';
                }
            } else {
                *r++ = 'K';
                *r++ = 'S';
            }
            break;
        case 'y':
            if (ISVOWEL(next)) {
                *r++ = 'Y';
            }
            break;
        case 'z':
            *r++ = 'S';
            break;
        case ' ':
            if (*r != ' ') {
                *r++ = ' ';
            }
            break;
        }
    }

    return result;
}
