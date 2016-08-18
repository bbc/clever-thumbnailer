/*

*/

#include "config.h"

#include <stdarg.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/time.h>


#ifndef CLEVER_THUMBNAILER_H
#define CLEVER_THUMBNAILER_H

#define DEFAULT_CROP_IN   (7.0)
#define DEFAULT_CROP_OUT  (7.0)
#define DEFAULT_FADE_IN   (0.5)
#define DEFAULT_FADE_OUT  (2.0)
#define DEFAULT_LENGTH    (30.0)
#define DEFAULT_PRELUDE   (10.0)

// Minimum segment time in seconds
#define SEGMENTER_MIN_SEGMENT_SIZE  (4.0f)
#define SEGMENTER_MAX_SEGMENTS      (10)


#ifndef FALSE
#define FALSE (0)
#endif

#ifndef TRUE
#define TRUE  (1)
#endif

#ifdef __cplusplus
extern "C" {
#endif

float calculate_clever_thumbnail(SNDFILE *input, SF_INFO *input_info, float length);

float calculate_middle_thumbnail(SNDFILE *input, SF_INFO *input_info, float length);
int trim_audio_file(SNDFILE *input, SF_INFO *input_info, const char* output_filename, float offset, float length);

#ifdef __cplusplus
}
#endif


#endif
