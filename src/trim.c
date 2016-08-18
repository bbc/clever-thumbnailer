/*

*/

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <sndfile.h>

#include "clever-thumbnailer.h"


static int copy_frames(
    SNDFILE *input,
    SNDFILE *output,
    int channels,
    sf_count_t frames
)
{
    int buffer[4096];
    sf_count_t buffer_size = sizeof(buffer) / sizeof(int) / channels;

    while(frames > 0) {
        sf_count_t readcount = sf_readf_int(input, buffer, buffer_size);
        if (readcount > 0) {
            sf_count_t writecount = sf_writef_int(output, buffer, readcount);
            if (writecount < 1) {
                ct_warning("sf_writef_int error: %s", sf_strerror(output));
                return -1;
            }
            frames -= readcount;
        } else {
            ct_warning("sf_readf_int error: %s", sf_strerror(output));
            return -1;
        }
    }

    // Success
    return 0;
}

int trim_audio_file(
    SNDFILE *input,
    SF_INFO *input_info,
    const char* output_filename,
    float offset,
    float length)
{
    SNDFILE *output;
    SF_INFO output_info;

    // Seek to the offset in the input file
    sf_count_t result = sf_seek(input, ceilf(offset * input_info->samplerate), SEEK_SET);
    if (result < 1) {
        ct_warning("Failed to seek to offset: %1.1f\n", offset);
        return -1;
    }

    // Open the output file
    memset(&output_info, 0, sizeof(SF_INFO));
    output_info.samplerate = input_info->samplerate;
    output_info.channels = input_info->channels;
    // FIXME: choose output format based on the output filename
    output_info.format = input_info->format;
    output = sf_open(output_filename, SFM_WRITE, &output_info);
    if (output == NULL) {
        ct_warning("Failed to open output file: %s\n", sf_strerror(NULL));
        return -1;
    }

    // Now copy frames from in to out
    copy_frames(input, output, input_info->channels, ceilf(length * input_info->samplerate));

    sf_close(output);

    // Success
    return 0;
}
