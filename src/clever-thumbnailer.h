/*

*/

#include "config.h"

#include <stdarg.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/time.h>

#include <sndfile.h>


#ifndef CLEVER_THUMBNAILER_H
#define CLEVER_THUMBNAILER_H

#define DEFAULT_CROP_IN   (7.0)
#define DEFAULT_CROP_OUT  (7.0)
#define DEFAULT_FADE_IN   (0.5)
#define DEFAULT_FADE_OUT  (3.0)
#define DEFAULT_LENGTH    (30.0)
#define DEFAULT_PRELUDE   (10.0)

// Minimum segment time in seconds
#define SEGMENTER_MIN_SEGMENT_SIZE  (4.0f)
#define SEGMENTER_MAX_SEGMENTS      (10)

#define LOUDNESS_WINDOW_SIZE        (1024)



#ifndef FALSE
#define FALSE (0)
#endif

#ifndef TRUE
#define TRUE  (1)
#endif


#define MM_SS(sec)   (sec / 60), (sec % 60)
#define LIN2DB(val)  (20.0f * log10(val))


#ifdef __cplusplus
extern "C" {
#endif

extern int verbose;
extern int quiet;
extern int use_dynamic;

typedef enum {
    LOGLEVEL_DEBUG=1,   // Only display debug if verbose
    LOGLEVEL_INFO,      // Don't show info when quiet
    LOGLEVEL_WARNING,   // Always display warnings
    LOGLEVEL_ERROR      // Quit after errors
} LogLevel;


#define ct_debug( ... )    ct_log( LOGLEVEL_DEBUG, __VA_ARGS__ )
#define ct_info( ... )     ct_log( LOGLEVEL_INFO, __VA_ARGS__ )
#define ct_warning( ... )  ct_log( LOGLEVEL_WARNING, __VA_ARGS__ )
#define ct_error( ... )    ct_log( LOGLEVEL_ERROR, __VA_ARGS__ )


void ct_log( LogLevel level, const char* fmt, ... );

float calculate_clever_thumbnail(SNDFILE *input, SF_INFO *input_info, float length);
float calculate_middle_thumbnail(SNDFILE *input, SF_INFO *input_info, float length);

int trim_audio_file(
    SNDFILE *input,
    SF_INFO *input_info,
    const char* output_filename,
    float offset,
    float length,
    float fade_in,
    float fade_out);

int calculate_segment_loudness(
    SNDFILE *input, SF_INFO *sfinfo,
    sf_count_t start, sf_count_t end,
    double *mean, double *min, double *max);

#ifdef __cplusplus
}
#endif


#endif
