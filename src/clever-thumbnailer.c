/*

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>

#include "clever-thumbnailer.h"


// ------- Globals -------
int quiet = FALSE;
int verbose = FALSE;


static void usage()
{
    printf("%s version %s\n\n", PACKAGE_NAME, PACKAGE_VERSION);
    printf("Usage: %s [options] <inputfile> <outputfile>\n", PACKAGE_NAME);

    printf("   -a             Enable applause detection\n");
    printf("   -c <cropin>    Crop time from start in seconds (default %1.1f)\n", DEFAULT_CROP_IN);
    printf("   -C <cropout>   Crop time from end in seconds (default %1.1f)\n", DEFAULT_CROP_OUT);
    printf("   -d             Rate sections by dynamic range rather than max loudness\n");
    printf("   -f <fadein>    Fade-in duration in seconds (default %1.1f)\n", DEFAULT_FADE_IN);
    printf("   -F <fadeout>   Fade-out duration in seconds (default %1.1f)\n", DEFAULT_FADE_OUT);
    printf("   -h             Display this help message\n");
    printf("   -l <length>    Thumbnail length in seconds (default %1.1f)\n", DEFAULT_LENGTH);
    printf("   -p <prelude>   Seconds of additional lead-in (default %1.1f)\n", DEFAULT_PRELUDE);
    printf("   -q             Enable quiet mode\n");
    printf("   -v             Enable verbose mode\n");

    exit(1);
}


int main(int argc, char *argv[])
{
    const char* input_filename = NULL;
    const char* output_filename = NULL;
    int applause_detection = FALSE;
    int use_dynamic = FALSE;
    float crop_in = DEFAULT_CROP_IN;
    float crop_out = DEFAULT_CROP_OUT;
    float fade_in = DEFAULT_FADE_IN;
    float fade_out = DEFAULT_FADE_OUT;
    float length = DEFAULT_LENGTH;
    float prelude = DEFAULT_PRELUDE;
    int result = -1;
    int opt;

    // Make STDOUT unbuffered
    setbuf(stdout, NULL);

    // Parse Switches
    while ((opt = getopt(argc, argv, "ac:C:df:F:hl:p:qv")) != -1) {
        switch (opt) {
        case 'a':
            applause_detection = TRUE;
            break;
        case 'c':
            crop_in = atof(optarg);
            break;
        case 'C':
            crop_out = atof(optarg);
            break;
        case 'n':
            use_dynamic = TRUE;
            break;
        case 'f':
            fade_in = atof(optarg);
            break;
        case 'F':
            fade_out = atof(optarg);
            break;
        case 'l':
            length = atof(optarg);
            break;
        case 'p':
            prelude = atof(optarg);
            break;
        case 'v':
            verbose = TRUE;
            break;
        case 'q':
            quiet = TRUE;
            break;
        default:
            usage();
            break;
        }
    }

    // Validate parameters
    if (quiet && verbose) {
        fprintf(stderr, "Can't be quiet and verbose at the same time.");
        usage();
    }

    // Check remaining arguments
    argc -= optind;
    argv += optind;
    if (argc < 1) {
        fprintf(stderr, "Missing input filename.\n");
        usage();
    } else if (argc < 2) {
        fprintf(stderr, "Missing output filename.\n");
        usage();
    } else {
        input_filename = argv[0];
        output_filename = argv[1];
    }

    result = trim_audio_file(
        input_filename,
        output_filename,
        30.0,
        length
    );

    // Success
    return result;
}
