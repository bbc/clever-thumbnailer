#include <math.h>
#include <sndfile.h>

#include "clever-thumbnailer.h"


static double calculate_window_rms(SNDFILE *input, SF_INFO *sfinfo)
{
    double buffer[LOUDNESS_WINDOW_SIZE * 2];
    double total = 0.0;

    sf_count_t readcount = sf_read_double(input, buffer, LOUDNESS_WINDOW_SIZE * sfinfo->channels);
    if (readcount <= 0) {
        ct_warning("Read failed in calculate_window_mean_loudness: %s", sf_strerror(input));
        return 0;
    }
    
    for (sf_count_t i=0; i<readcount; i++) {
        total += (buffer[i] * buffer[i]);
    }

    return sqrt(total / readcount);
}



int calculate_segment_loudness(
    SNDFILE *input, SF_INFO *sfinfo,
    sf_count_t start, sf_count_t end,
    double *mean, double *min, double *max)
{
    sf_count_t remaining = 0;
    double total = 0.0;
    int window_count = 0;

    // Seek to the starting point
    sf_count_t result = sf_seek(input, start, SEEK_SET);
    if (result < 0) {
        ct_warning("Failed to seek to offset: %d\n", start);
        return FALSE;
    }

    // Is the requested range longer than the file?
    if (end > sfinfo->frames) {
        end = sfinfo->frames;
    }

    // All samples should be between 0 and 1, so these should be safe starting points
    *min = 10.0;
    *max = -10.0;

    for(remaining = start; remaining < end; remaining += LOUDNESS_WINDOW_SIZE) {
        double rms = calculate_window_rms(input, sfinfo);
        if (rms < *min)
            *min = rms;
        if (rms > *max)
            *max = rms;
        total += rms;
        window_count++;
    }
    
    *mean = total / window_count;

    // Success
    return TRUE;
}
