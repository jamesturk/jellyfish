/* Date of Release:  Jan. 26, 1994
   Modified: April 24, 1994  Corrected the processing of the single length
             character strings.
   Authors:  This function was written using the logic from code written by
             Bill Winkler, George McLaughlin and Matt Jaro with modifications
             by Maureen Lynch. 
   Comment:  This is the official string comparator to be used for matching 
             during the 1995 Test Census.
*/

#include <ctype.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "jaro.h"

#define NOTNUM(c)   ((c>57) || (c<48))
#define INRANGE(c)  ((c>0)  && (c<91))

/* The jaro_winkler function returns a double precision value from 0.0 (total
   disagreement) to 1.0 (character-by-character agreement).  The returned 
   value is a measure of the similarity of the two strings.
*/
double jaro_winkler(const char *ying, const char *yang, bool ignore_case,
    bool long_tolerance)
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
       
       ignore_case
         ignore case in comparison
    */
    char *ying_cpy=0, *yang_cpy=0, *ying_flag=0, *yang_flag=0;

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
    
    ying_cpy = (char*) malloc(sizeof(char) * (ying_length+1));
    yang_cpy = (char*) malloc(sizeof(char) * (yang_length+1));
    
    strncpy(ying_cpy, ying, ying_length+1);
    strncpy(yang_cpy, yang, yang_length+1);
    
    if (ying_length > yang_length) {
        search_range = ying_length;
        min_len = yang_length;
    } else {
        search_range = yang_length;
        min_len = ying_length;
    }
    
    // Blank out the flags
    ying_flag = (char*) malloc(sizeof(char) * (ying_length+1));
    yang_flag = (char*) malloc(sizeof(char) * (yang_length+1));
    memset(ying_flag, ' ', ying_length);
    memset(yang_flag, ' ', yang_length);
    
    // Convert all lower case characters to upper case.
    if (ignore_case) {
        for (i = 0;i < ying_length;i++) {
            if (islower(ying_cpy[i])) {
                ying_cpy[i] -= 32;
            }
        }
        for (j = 0;j < yang_length;j++) {
            if (islower(yang_cpy[j])) {
                yang_cpy[j] -= 32;
            }
        }
    }
    
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
            if (yang_flag[j] != '1' && yang_cpy[j] == ying_cpy[i]) {
                yang_flag[j] = '1';
                ying_flag[i] = '1';
                common_chars++;
                break;
            }
        }
    }
    
    // If no characters in common - return
    if (!common_chars) {
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
            if (ying_cpy[i] != yang_cpy[j]) {
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
    if (weight > 0.7) {
        
        // Adjust for having up to the first 4 characters in common
        j = (min_len >= 4) ? 4 : min_len;
        for (i=0;((i<j)&&(ying_cpy[i]==yang_cpy[i])&&(NOTNUM(ying_cpy[i])));i++); 
        if (i) {
            weight += i * 0.1 * (1.0 - weight);
        }
        
        /* Optionally adjust for long strings. */
        /* After agreeing beginning chars, at least two more must agree and 
           the agreeing characters must be > .5 of remaining characters.
        */
        if ((long_tolerance) && (min_len>4) && (common_chars>i+1) && (2*common_chars>=min_len+i)) {
            if (NOTNUM(ying_cpy[0])) {
                weight += (double) (1.0-weight) *
                    ((double) (common_chars-i-1) / ((double) (ying_length+yang_length-i*2+2)));
            }
        }
    }
    
    return weight ;
}
