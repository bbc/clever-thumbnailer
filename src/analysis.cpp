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

    ct_debug("Starting Segmenter");
    static ClusterMeltSegmenter segmenter = ClusterMeltSegmenter(params);
    segmenter.initialise(sfinfo->samplerate);

    // get preferred window(block) size
    int window = segmenter.getWindowsize();
    ct_debug("  Window Size: %d samples", window);
    
    // get preferred hop(step) size
    int hop = segmenter.getHopsize();
    ct_debug("  Hop Size: %d samples", hop);

    double* buffer = (double*)malloc(window * sizeof(double));
    if (buffer == NULL) {
        ct_error("Failed to allocate memory for segmenter audio buffer.");
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

    ct_debug("Performing segmentation...");
    segmenter.segment(SEGMENTER_MAX_SEGMENTS);

    // get results
    return segmenter.getSegmentation();
}


float calculate_middle_thumbnail(SNDFILE *input, SF_INFO *input_info, float thumb_length)
{
    float total_length = ((float)input_info->frames / input_info->samplerate);

    if (thumb_length >= total_length) {
        ct_warning("Requested thumbnail duration is longer than original audio.");
        return 0.0;
    } else {
        return (total_length / 2) - (thumb_length / 2);
    }
}


float calculate_clever_thumbnail(SNDFILE *input, SF_INFO *sfinfo, float thumb_length)
{
    // Step 1: segment the audio
    const Segmentation& seginfo = perform_segmentation(input, sfinfo);
    ct_debug(
        "Audio segmented into %d types, with %d total sections, at %dHz sample rate.",
        (int)seginfo.nsegtypes,
        (int)seginfo.segments.size(),
        seginfo.samplerate
    );

    // Step 2: ignore segments with applause
    // FIXME: do this

    // Step 3: calculate loudness of each segment
    int best_segment = 0;
    double best_segment_value = -1.0;
    for (int i = 0; i < seginfo.segments.size(); i++)
    {
        const Segment &segment = seginfo.segments[i];
        double mean, min, max;

        ct_debug(
            " Section %d: Type %d. Start %2.2d:%2.2d, end %2.2d:%2.2d. ",
            i, segment.type,
            MM_SS(segment.start / sfinfo->samplerate),
            MM_SS(segment.end / sfinfo->samplerate)
        );

        
        int result = calculate_segment_loudness(
            input, sfinfo,
            segment.start, segment.end,
            &mean, &min, &max
        );
        
        if (result) {
            double current_value = use_dynamic ? max-min : mean;
        
            ct_debug(
                "   mean=%1.1f min=%1.1f max=%1.1f range=%1.1f",
                LIN2DB(mean), LIN2DB(min), LIN2DB(max), LIN2DB(max-min)
            );
            
            if (best_segment_value < current_value) {
                best_segment = i;
                best_segment_value = current_value;
            }
        }        
    }

    // Step 4: pick the best segment
    const Segment &segment = seginfo.segments[best_segment];

    if (use_dynamic) {
        ct_info("Segment with greatest dynamic range is %d and starts at %2.2d:%2.2d", best_segment, MM_SS(segment.start / sfinfo->samplerate));
    } else {
        ct_info("Loudest segment is %d and starts at %2.2d:%2.2d", best_segment, MM_SS(segment.start / sfinfo->samplerate));
    }

    return segment.start / sfinfo->samplerate;
}
