/*
  This script displays the loudness of an audio file in 10 second chunks

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>
#include <sndfile.h>

#include "clever-thumbnailer.h"


// ------- Globals -------
int quiet = TRUE;
int verbose = FALSE;


#define MM_SS(sec)   (sec / 60), (sec % 60)


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

    printf("| Start | End   | Mean     |\n");
    printf("|-------|-------|----------|\n");
    const int segment_size = 10 * sfinfo.samplerate;
    for(int i=0; i < sfinfo.frames; i += segment_size) {
        int end = i + segment_size;
        double loudness = calculate_segment_loudness(input, &sfinfo, i, end);
        float db = 20.0f * log10f(loudness);
        printf(
          "| %2.2d:%2.2d | %2.2d:%2.2d | %1.1f dB |\n",
          MM_SS(i / sfinfo.samplerate),
          MM_SS(end / sfinfo.samplerate),
          db
        );
    }

    sf_close(input);

    // Success
    return 0;
}
