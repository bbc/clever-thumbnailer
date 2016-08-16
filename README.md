CleverThumbnailer
=================

Cleverthumbnailer is a command line tool that analyses songs and creates short audio thumbnails of them.

Algorithm
---------

Given a full length piece of music in WAVE format (`*.bwf` and `*.wav`), cleverthumbnailer attempts to generate a short extract most representative of the track in general. It bases this decision on three factors:

1. **Segment Detection**. Using the [QMUL Segmenter](http://dx.doi.org/10.1109/TASL.2007.910781) algorithm, distinct musical sections of a piece are found. In western pop music, this algorithm detects transitions between verses, choruses, and bridges. In western classical music, segment boundaries are often found at key changes/modulations.
2. **RMS Energy profiling**. The varying dynamics of a piece of music are
calculated by tracking the RMS energy over the course of a piece. Sections of a piece that are loud (by default) or have a high amount of dynamic variation (`--dynamic` flag) are preferred for inclusion in the audio snippet generated.
3. **Applause detection**. An algorithm that determines [spectral centroid](https://dx.doi.org/10.1121%2F1.381843) over time is used to detect applause within a recording. Periods of applause are avoided in the resulting audio thumbnail. 

Installation
------------



Usage
-----

```
clever-thumbnailer version 0.1.0

Usage: clever-thumbnailer [options] <inputfile> <outputfile>
   -a             Enable applause detection
   -c <cropin>    Crop time from start in seconds (default 7.0)
   -C <cropout>   Crop time from end in seconds (default 7.0)
   -d             Rate sections by dynamic range rather than max loudness
   -f <fadein>    Fade-in duration in seconds (default 0.5)
   -F <fadeout>   Fade-out duration in seconds (default 2.0)
   -h             Display this help message
   -l <length>    Thumbnail length in seconds (default 30.0)
   -p <prelude>   Seconds of additional lead-in (default 10.0)
   -q             Enable quiet mode
   -v             Enable verbose mode
```


Credits
-------

The code in this repository was created by Jon Tutcher in 2015 for [BBC Research & Development](http://www.bbc.co.uk/rd).

[QM-DSP](https://code.soundsoftware.ac.uk/projects/qm-dsp) was created by Queen Mary University of London; the segmenter module used here was developed by Mark Levy and Chris Cannam.


License
-------

This project is licensed under the GNU GPLv2 license. For terms and conditions, see [LICENSE](LICENSE).
