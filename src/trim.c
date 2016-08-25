/*

*/

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <sndfile.h>

#include "clever-thumbnailer.h"


static void apply_fade(
    int buffer[],
    sf_count_t frames,
    int channels,
    double gain,
    double gain_per_frame
)
{
    for(sf_count_t f=0; f < frames; f++) {
        for (int c=0; c < channels; c++) {
            buffer[f*channels + c] *= gain;
        }
        gain += gain_per_frame;
    }
}

static int copy_and_fade(
    SNDFILE *input,
    SF_INFO *input_info,
    SNDFILE *output,
    float length,
    float start_gain,
    float end_gain
)
{
    int buffer[4096];
    sf_count_t frames = ceilf(length * input_info->samplerate);
    sf_count_t remaining = frames;
    sf_count_t buffer_size = sizeof(buffer) / sizeof(int) / input_info->channels;
    double gain_per_frame = (end_gain - start_gain) / frames;
    
    if (start_gain != end_gain) {
        ct_debug("Applying %1.1f second fade with gain %1.1f -> %1.1f", length, start_gain, end_gain);
        ct_debug("Per-frame fade gain: %f", gain_per_frame);
    }

    while(remaining > 0) {
        // 1: Read samples from input file
        sf_count_t readcount = sf_readf_int(input, buffer, buffer_size);

        if (readcount > 0) {
            // 2: Apply the fade
            if (start_gain != end_gain) {
                double gain = start_gain + ((frames - remaining) * gain_per_frame);
                apply_fade(
                    buffer, readcount,
                    input_info->channels,
                    gain,
                    gain_per_frame
                );
            }

            // 3: Write back to disk
            sf_count_t writecount = sf_writef_int(output, buffer, readcount);
            if (writecount < 1) {
                ct_warning("sf_writef_int error: %s", sf_strerror(output));
                return -1;
            }
            remaining -= readcount;
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
    float length,
    float fade_in,
    float fade_out)
{
    SNDFILE *output;
    SF_INFO output_info;

    ct_info("Creating %1.1f second thumbnail from %1.1f seconds into the file.", length, offset);

    // Seek to the offset in the input file
    sf_count_t result = sf_seek(input, ceilf(offset * input_info->samplerate), SEEK_SET);
    if (result < 0) {
        ct_warning("Failed to seek to offset: %1.1f", offset);
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
        ct_warning("Failed to open output file: %s", sf_strerror(NULL));
        return -1;
    }

    // Copy frames from in to out, applying a fade if required
    float body_length = length - fade_in - fade_out;
    copy_and_fade(input, input_info, output, fade_in, 0.0, 1.0);
    copy_and_fade(input, input_info, output, body_length, 1.0, 1.0);
    copy_and_fade(input, input_info, output, fade_out, 1.0, 0.0);

    sf_close(output);

    // Success
    return 0;
}
