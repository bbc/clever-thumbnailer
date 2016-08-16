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


#ifndef FALSE
#define FALSE (0)
#endif

#ifndef TRUE
#define TRUE  (1)
#endif


int trim_audio_file(const char* input_filename, const char* output_filename, float offset, float length);


#endif
