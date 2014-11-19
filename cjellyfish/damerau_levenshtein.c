#include "jellyfish.h"
#include <string.h>
#include <stdio.h>

int damerau_levenshtein_distance(const char *s1, const char *s2)
{
    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);
    size_t infinite = len1 + len2;
    size_t cols = len2 + 2;

    size_t i, j, i1, j1;
    size_t db;
    size_t d1, d2, d3, d4, result;
    unsigned short cost;

    size_t *da = malloc(256 * sizeof(size_t));
    if (!da) {
        return -1;
    }
    for(i = 0; i < 256; i++) {
        da[i] = 0;
    }

    size_t *dist = malloc((len1 + 2) * cols * sizeof(size_t));
    if (!dist) {
        return -1;
    }

    dist[0] = infinite;

    for (i = 0; i <= len1; i++) {
        dist[((i + 1) * cols) + 0] = infinite;
        dist[((i + 1) * cols) + 1] = i;
    }

    for (i = 0; i <= len2; i++) {
        dist[i + 1] = infinite;       // 0*cols + row
        dist[cols + i + 1] = i;       // 1*cols + row
    }

    for (i = 1; i <= len1; i++) {
        db = 0;
        for (j = 1; j <= len2; j++) {
            i1 = da[(size_t)(s2[j-1])];
            j1 = db;

            if (s1[i - 1] == s2[j - 1]) {
                cost = 0;
                db = j;
            } else {
                cost = 1;
            }

            d1 = dist[(i * cols) + j] + cost;
            d2 = dist[((i + 1) * cols) + j] + 1;
            d3 = dist[(i * cols) + j + 1] + 1;
            d4 = dist[(i1 * cols) + j1] + (i - i1 - 1) + 1 + (j - j1 - 1);

            dist[((i+1)*cols) + j + 1] = MIN(MIN(d1, d2), MIN(d3, d4));
        }

        da[s1[i-1]] = i;
    }

    result = dist[((len1+1) * cols) + len2 + 1];

    free(dist);
    free(da);

    return result;
}
