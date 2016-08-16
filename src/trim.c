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
                fprintf(stderr, "sf_writef_int error: %s\n", sf_strerror(output));
                return -1;
            }
            frames -= readcount;
        } else {
            fprintf(stderr, "sf_readf_int error: %s\n", sf_strerror(input));
            return -1;
        }
    }

    // Success
    return 0;
}

int trim_audio_file(
    const char* input_filename,
    const char* output_filename,
    float offset,
    float length)
{
    SNDFILE *input, *output;
    SF_INFO input_info, output_info;

    // Open the input file
    memset(&input_info, 0, sizeof(SF_INFO));
    input = sf_open(input_filename, SFM_READ, &input_info);
    if (input == NULL) {
        fprintf(stderr, "Failed to open input file: %s\n", sf_strerror(NULL));
        return -1;
    }

    // Seek to the start offset
    sf_count_t result = sf_seek(input, ceilf(offset * input_info.samplerate), SEEK_SET);
    if (result < 1) {
        fprintf(stderr, "Failed to seek to offset: %1.1f\n", offset);
        sf_close(input);
        return -1;
    }

    // Open the output file
    memset(&output_info, 0, sizeof(SF_INFO));
    output_info.samplerate = input_info.samplerate;
    output_info.channels = input_info.channels;
    // FIXME: choose output format based on the output filename
    output_info.format = input_info.format;
    output = sf_open(output_filename, SFM_WRITE, &output_info);
    if (output == NULL) {
        fprintf(stderr, "Failed to open output file: %s\n", sf_strerror(NULL));
        sf_close(input);
        return -1;
    }

    // Now copy frames from in to out
    copy_frames(input, output, input_info.channels, ceilf(length * input_info.samplerate));

    sf_close(input);
    sf_close(output);

    // Success
    return 0;

}
