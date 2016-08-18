#include <stdio.h>
#include <stdlib.h>

#include "clever-thumbnailer.h"

void ct_log( LogLevel level, const char* fmt, ... )
{
    va_list args;

    if (level == LOGLEVEL_DEBUG ) {
        if (!verbose) return;
        fprintf(stderr, "[DEBUG]  " );
    } else if (level == LOGLEVEL_INFO ) {
        if (quiet) return;
        fprintf(stderr, "[INFO]   " );
    } else if (level == LOGLEVEL_WARNING ) {
        fprintf(stderr, "[WARN]   " );
    } else if (level == LOGLEVEL_ERROR ) {
        fprintf(stderr, "[ERROR]  " );
    } else {
        fprintf(stderr, "[UNKNOWN]" );
    }

    // Display the error message
    va_start( args, fmt );
    vfprintf( stderr, fmt, args );
    fprintf( stderr, "\n" );
    va_end( args );

    // If fatal then stop
    if (level == LOGLEVEL_ERROR) {
        exit(-1);
    }
}
