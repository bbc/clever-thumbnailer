#include <math.h>
#include <sndfile.h>

#include "clever-thumbnailer.h"


static double calculate_window_mean_loudness(SNDFILE *input, SF_INFO *sfinfo)
{
    double buffer[LOUDNESS_WINDOW_SIZE * 2];
    double total = 0.0;

    sf_count_t readcount = sf_read_double(input, buffer, LOUDNESS_WINDOW_SIZE * sfinfo->channels);
    if (readcount <= 0) {
        ct_warning("Read failed in calculate_window_mean_loudness: %s", sf_strerror(input));
        return 0;
    }
    
    for (sf_count_t i=0; i<readcount; i++) {
        total += fabs(buffer[i]);
    }

    return total / readcount;
}



float calculate_segment_loudness(SNDFILE *input, SF_INFO *sfinfo, sf_count_t start, sf_count_t end)
{
    sf_count_t remaining = 0;
    double total = 0.0;
    int window_count = 0;

    sf_count_t result = sf_seek(input, start, SEEK_SET);
    if (result < 0) {
        ct_warning("Failed to seek to offset: %d\n", start);
        return 0;
    }

    // Is the requested range longer than the file?
    if (end > sfinfo->frames) {
        end = sfinfo->frames;
    }

    for(remaining = end-start; remaining > 0; remaining -= LOUDNESS_WINDOW_SIZE) {
        double window_loudness = calculate_window_mean_loudness(input, sfinfo);
        total += window_loudness;
        window_count++;
    }

    return total / window_count;
}
