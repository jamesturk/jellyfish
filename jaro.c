#include <ctype.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "jellyfish.h"

#define NOTNUM(c)   ((c>57) || (c<48))
#define INRANGE(c)  ((c>0)  && (c<91))

#ifndef NaN
#define NaN (0.0 / 0.0)
#endif

/* borrowed heavily from strcmp95.c
 *    http://www.census.gov/geo/msb/stand/strcmp.c
 */
double _jaro_winkler(const char *ying, const char *yang,
                     bool long_tolerance, bool winklerize)
{
    /* Arguments:

       ying
       yang
         pointers to the 2 strings to be compared.

       long_tolerance
         Increase the probability of a match when the number of matched
         characters is large.  This option allows for a little more
         tolerance when the strings are large.  It is not an appropriate
         test when comparing fixed length fields such as phone and
         social security numbers.
    */
    char *ying_flag=0, *yang_flag=0;

    double weight;

    long ying_length, yang_length, min_len;
    long search_range;
    long lowlim, hilim;
    long trans_count, common_chars;

    register int i, j, k;

    // ensure that neither string is blank
    ying_length = strlen(ying);
    yang_length = strlen(yang);

    if (!ying_length || !yang_length) {
        return 0;
    }

    if (ying_length > yang_length) {
        search_range = ying_length;
        min_len = yang_length;
    } else {
        search_range = yang_length;
        min_len = ying_length;
    }

    // Blank out the flags
    ying_flag = (char*)calloc(ying_length + 1, sizeof(char));
    if (!ying_flag) {
        return NaN;
    }

    yang_flag = (char*)calloc(yang_length + 1, sizeof(char));
    if (!yang_flag) {
        free(ying_flag);
        return NaN;
    }

    memset(ying_flag, ' ', ying_length);
    memset(yang_flag, ' ', yang_length);

    search_range = (search_range/2) - 1;
    if(search_range < 0) {
        search_range = 0;
    }

    // Looking only within the search range, count and flag the matched pairs.
    common_chars = 0;
    for (i = 0; i < ying_length; i++) {
        lowlim = (i >= search_range) ? i - search_range : 0;
        hilim = (i + search_range <= yang_length-1) ? (i + search_range) : yang_length-1;
        for (j = lowlim; j <= hilim; j++)  {
            if (yang_flag[j] != '1' && yang[j] == ying[i]) {
                yang_flag[j] = '1';
                ying_flag[i] = '1';
                common_chars++;
                break;
            }
        }
    }

    // If no characters in common - return
    if (!common_chars) {
        // free the flag memory
        free(ying_flag);
        free(yang_flag);
        return 0;
    }

    // Count the number of transpositions
    k = trans_count = 0;
    for (i = 0; i < ying_length; i++) {
        if (ying_flag[i] == '1') {
            for (j = k;j < yang_length;j++) {
                if (yang_flag[j] == '1') {
                    k = j + 1;
                    break;
                }
            }
            if (ying[i] != yang[j]) {
                trans_count++;
            }
        }
    }
    trans_count /= 2;

    // adjust for similarities in nonmatched characters

    // Main weight computation.
    weight= common_chars / ((double) ying_length) + common_chars / ((double) yang_length)
        + ((double) (common_chars - trans_count)) / ((double) common_chars);
    weight /=  3.0;

    // Continue to boost the weight if the strings are similar
    if (winklerize && weight > 0.7) {

        // Adjust for having up to the first 4 characters in common
        j = (min_len >= 4) ? 4 : min_len;
        for (i=0;((i<j)&&(ying[i]==yang[i])&&(NOTNUM(ying[i])));i++);
        if (i) {
            weight += i * 0.1 * (1.0 - weight);
        }

        /* Optionally adjust for long strings. */
        /* After agreeing beginning chars, at least two more must agree and
           the agreeing characters must be > .5 of remaining characters.
        */
        if ((long_tolerance) && (min_len>4) && (common_chars>i+1) && (2*common_chars>=min_len+i)) {
            if (NOTNUM(ying[0])) {
                weight += (double) (1.0-weight) *
                    ((double) (common_chars-i-1) / ((double) (ying_length+yang_length-i*2+2)));
            }
        }
    }

    // free the flag memory
    free(ying_flag);
    free(yang_flag);

    return weight;
}


double jaro_winkler(const char *ying, const char *yang, bool long_tolerance)
{
    return _jaro_winkler(ying, yang, long_tolerance, true);
}

double jaro_distance(const char *ying, const char *yang)
{
    return _jaro_winkler(ying, yang, false, false);
}
