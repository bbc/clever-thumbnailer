#include <ClusterMeltSegmenter.h>
#include <sndfile.h>

#include <stdio.h>

#include "clever-thumbnailer.h"


static const Segmentation& perform_segmentation(SNDFILE *input, SF_INFO *sfinfo)
{
    ClusterMeltSegmenterParams params;
    
    // We want constant Q (hybrid) segmentation
    params.featureType = FEATURE_TYPE_CONSTQ;
    
    // Calculate neighbourhood limit in seconds
    params.neighbourhoodLimit = (SEGMENTER_MIN_SEGMENT_SIZE / params.hopSize) + 0.0001;

    ClusterMeltSegmenter segmenter = ClusterMeltSegmenter(params);
    segmenter.initialise(sfinfo->samplerate);

    // get preferred window(block) size
    int window = segmenter.getWindowsize();
    printf("Window Size: %d samples\n", window);
    
    // get preferred hop(step) size
    int hop = segmenter.getHopsize();
    printf("Hop Size: %d samples\n", hop);

    double* buffer = (double*)malloc(window * sizeof(double));
    if (buffer == NULL) {
        fprintf(stderr, "Error: failed to allocate memory for buffer\n");
        exit(-1);
    }

    for(sf_count_t i=0; i<sfinfo->frames; i += hop) {
        sf_seek(input, i, SEEK_SET);
        sf_count_t readcount = sf_read_double(input, buffer, window);

        if (readcount < window)
            break;
        segmenter.extractFeatures(buffer, readcount);
    }

    free(buffer);
    sf_close(input);

    printf("Performing segmentation...\n");
    segmenter.segment(SEGMENTER_MAX_SEGMENTS);

    // get results
    return segmenter.getSegmentation();
}


float calculate_middle_thumbnail(SNDFILE *input, SF_INFO *input_info, float thumb_length)
{
    float total_length = ((float)input_info->frames / input_info->samplerate);

    if (thumb_length >= total_length) {
        fprintf(stderr, "Warning: requested thumbnail duration is longer than original audio\n");
        return 0.0;
    } else {
        return (total_length / 2) - (thumb_length / 2);
    }
}


float calculate_clever_thumbnail(SNDFILE *input, SF_INFO *sfinfo, float thumb_length)
{
    // Step 1: segment the audio
    const Segmentation& seginfo = perform_segmentation(input, sfinfo);
    printf(
        "Audio segmented into %d types, with %d total sections, at %dHz sample rate.\n",
        (int)seginfo.nsegtypes,
        (int)seginfo.segments.size(),
        seginfo.samplerate
    );

    // Step 2: ignore segments with applause

    // Step 3: calculate loudness of each segment

    // Step 4: pick the loudest segment

    return 0.0f;
}
