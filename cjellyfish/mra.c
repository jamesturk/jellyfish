#include "jellyfish.h"
#include <string.h>
#include <ctype.h>

int match_rating_comparison(const char *s1, const char *s2) {
    size_t s1c_len, s2c_len;
    size_t i, j;
    int diff;
    char *longer;

    char *s1_codex = match_rating_codex(s1);
    if (!s1_codex) {
        return -1;
    }

    char *s2_codex = match_rating_codex(s2);
    if (!s2_codex) {
        free(s1_codex);
        return -1;
    }

    s1c_len = strlen(s1_codex);
    s2c_len = strlen(s2_codex);

    if (abs(s1c_len - s2c_len) >= 3) {
        free(s1_codex);
        free(s2_codex);
        return -1;
    }

    for (i = 0; i < s1c_len && i < s2c_len; i++) {
        if (s1_codex[i] == s2_codex[i]) {
            s1_codex[i] = ' ';
            s2_codex[i] = ' ';
        }
    }

    i = s1c_len - 1;
    j = s2c_len - 1;

    while (i != 0 && j != 0) {
        if (s1_codex[i] == ' ') {
            i--;
            continue;
        }

        if (s2_codex[j] == ' ') {
            j--;
            continue;
        }

        if (s1_codex[i] == s2_codex[j]) {
            s1_codex[i] = ' ';
            s2_codex[j] = ' ';
        }

        i--;
        j--;
    }

    if (s1c_len > s2c_len) {
        longer = s1_codex;
    } else {
        longer = s2_codex;
    }

    for (diff = 0; *longer; longer++) {
        if (*longer != ' ') {
            diff++;
        }
    }

    free(s1_codex);
    free(s2_codex);

    diff = 6 - diff;
    i = s1c_len + s2c_len;

    if (i <= 4) {
        return diff >= 5;
    } else if (i <= 7) {
        return diff >= 4;
    } else if (i <= 11) {
        return diff >= 3;
    } else {
        return diff >= 2;
    }
}

char* match_rating_codex(const char *str) {
    size_t len = strlen(str);
    size_t i, j;
    char c, prev;

    char *codex = malloc(7 * sizeof(char));
    if (!codex) {
        return NULL;
    }

    prev = '\0';
    for(i = 0, j = 0; i < len && j < 7; i++) {
        c = toupper(str[i]);

        if (c == ' ' || (i != 0 && (c == 'A' || c == 'E' || c == 'I' ||
                                    c == 'O' || c == 'U'))) {
            continue;
        }

        if (c == prev) {
            continue;
        }

        if (j == 6) {
            codex[3] = codex[4];
            codex[4] = codex[5];
            j = 5;
        }

        codex[j++] = c;
    }

    codex[j] = '\0';

    return codex;
}
