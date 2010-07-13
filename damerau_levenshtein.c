#include "jellyfish.h"
#include <string.h>

int damerau_levenshtein_distance(const char *s1, const char *s2)
{
    size_t s1_len = strlen(s1);
    size_t s2_len = strlen(s2);
    size_t rows = s1_len + 1;
    size_t cols = s2_len + 1;

    size_t i, j;
    size_t d1, d2, d3, d_now;;
    unsigned short cost;

    size_t *dist = malloc(rows * cols * sizeof(size_t));
    if (!dist) {
        return -1;
    }

    for (i = 0; i < rows; i++) {
        dist[i * cols] = i;
    }

    for (j = 0; j < cols; j++) {
        dist[j] = j;
    }

    for (i = 1; i < rows; i++) {
        for (j = 1; j < cols; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                cost = 0;
            } else {
                cost = 1;
            }

            d1 = dist[((i - 1) * cols) + j] + 1;
            d2 = dist[(i * cols) + (j - 1)] + 1;
            d3 = dist[((i - 1) * cols) + (j - 1)] + cost;

            d_now = MIN(d1, MIN(d2, d3));

            if (i > 2 && j > 2 && s1[i - 1] == s2[j - 2] &&
                s1[i - 2] == s2[j - 1]) {
                d1 = dist[((i - 2) * cols) + (j - 2)] + cost;
                d_now = MIN(d_now, d1);
            }

            dist[(i * cols) + j] = d_now;
        }
    }

    d_now = dist[(cols * rows) - 1];
    free(dist);

    return d_now;
}
