/*
  This script displays the loudness of an audio file in 10 second chunks

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <math.h>
#include <unistd.h>
#include <getopt.h>
#include <sndfile.h>

#include "clever-thumbnailer.h"


// ------- Globals -------
int quiet = TRUE;
int verbose = FALSE;



int main(int argc, const char *argv[])
{
    SNDFILE *input = NULL;
    SF_INFO sfinfo;

    if (argc != 2) {
        fprintf(stderr, "Missing input filename.\n");
        return -1;
    }

    memset(&sfinfo, 0, sizeof(SF_INFO));
    input = sf_open(argv[1], SFM_READ, &sfinfo);
    if (input == NULL) {
        fprintf(stderr, "Failed to open input file: %s", sf_strerror(NULL));
        return -1;
    }

    printf("| Start | End   | Mean     | Min      | Max      | Range    |\n");
    printf("|-------|-------|----------|----------|----------|----------|\n");
    const int segment_size = 10 * sfinfo.samplerate;
    for(int i=0; i < sfinfo.frames; i += segment_size) {
        double mean, min, max;
        int end = i + segment_size;
        int result = calculate_segment_loudness(input, &sfinfo, i, end, &mean, &min, &max);

        printf(
          "| %2.2d:%2.2d | %2.2d:%2.2d | %1.1f dB | %1.1f dB | %1.1f dB | %1.1f dB |\n",
          MM_SS(i / sfinfo.samplerate),
          MM_SS(end / sfinfo.samplerate),
          LIN2DB(mean),
          LIN2DB(min),
          LIN2DB(max),
          LIN2DB(max - min)
        );
    }

    sf_close(input);

    // Success
    return 0;
}
