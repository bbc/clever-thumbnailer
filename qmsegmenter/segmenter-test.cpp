
#include <ClusterMeltSegmenter.h>
#include <sndfile.h>

#include <stdio.h>

void format_duration(char buffer[16], float seconds)
{
    int minutes = seconds / 60;
    snprintf(buffer, 15, "%2.2d:%05.2f", minutes, seconds - (minutes * 60));
}

int main(int argc, const char* argv[])
{
    int nLimit = 4;          // minimum segment time in seconds
    int nComponents = 20;    // number of Principle Component Analysis components used in clustering (not currently implemented)
    int maxSegments = 10;    // *max* number of segment types (algorithm may return less)
    int sr = 48000;

    SNDFILE *input = NULL;
    SF_INFO sfinfo;

    if (argc != 2) {
        fprintf(stderr, "Usage: segmenter-test <filename>\n");
        exit(1);
    }

    // Open the input file
    memset(&sfinfo, 0, sizeof(SF_INFO));
    input = sf_open(argv[1], SFM_READ, &sfinfo);
    if (input == NULL) {
        fprintf(stderr, "Failed to open input file: %s\n", sf_strerror(NULL));
        return -1;
    }
    
    if (sfinfo.channels != 1) {
        fprintf(stderr, "Error: this test requires a mono audio file.\n");
        return -1;
    }
    
    char durationStr[16];
    format_duration(durationStr, (float)sfinfo.frames / sfinfo.samplerate);
    printf("File Duration: %s\n", durationStr);

    ClusterMeltSegmenterParams params;
    params.featureType = FEATURE_TYPE_CONSTQ;    // we want constant Q (hybrid) segmentation
    params.neighbourhoodLimit = ((float)nLimit / params.hopSize) + 0.0001;   // calculate neighbourhood limit in seconds
    params.ncomponents = nComponents;            // set number of PCA components

    ClusterMeltSegmenter segmenter = ClusterMeltSegmenter(params);
    segmenter.initialise(sfinfo.samplerate);

    // get preferred window(block) size
    int window = segmenter.getWindowsize();
    printf("Window Size: %d samples\n", window);
    
    // get preferred hop(step) size
    int hop = segmenter.getHopsize();
    printf("Hop Size: %d samples\n", hop);

    double* buffer = (double*)malloc(window * sizeof(double));
    if (buffer == NULL) {
        fprintf(stderr, "Error: failed to allocate memory for buffer\n");
        return -1;
    }

    for(sf_count_t i=0; i<sfinfo.frames; i += hop) {
        sf_seek(input, i, SEEK_SET);
        sf_count_t readcount = sf_read_double(input, buffer, window);

        if (readcount < window)
            break;
        segmenter.extractFeatures(buffer, readcount);
    }

    free(buffer);
    sf_close(input);

    printf("Performing segmentation...\n");
    segmenter.segment(maxSegments);

    // get results
    Segmentation segInfo = segmenter.getSegmentation();

    // print results
    printf(
        "Audio segmented into %d types, with %d total sections, at %dHz sample rate.\n",
        (int)segInfo.nsegtypes,
        (int)segInfo.segments.size(),
        segInfo.samplerate
    );


    for (int i = 0; i < segInfo.segments.size(); i++)
    {
        Segment &segment = segInfo.segments[i];
        
        char startstr[16], endstr[16];
        format_duration(startstr, (float)segment.start / segInfo.samplerate);
        format_duration(endstr, (float)segment.end / segInfo.samplerate);

        printf(
            "  Section %d: Type %d. Start %s, end %s (%d to %d samples)\n",
            i, segment.type,
            startstr, endstr,
            segment.start, segment.end
        );
    }

    return 0;
}

