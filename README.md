#CleverThumbnailer

Cleverthumbnailer is a Python2 application that analyses songs and creates short audio thumbnails of them based. Given a full length piece of music in WAVE format (`*.bwf` and `*.wav`), cleverthumbnailer attempts to generate a short extract most representative of the track in general. It bases this decision on three factors:

1. **Segment Detection**. Using the [QMUL Segmenter](http://dx.doi.org/10.1109/TASL.2007.910781) algorithm, distinct musical sections of a piece are found. In western pop music, this algorithm detects transitions between verses, choruses, and bridges. In western classical music, segment boundaries are often found at key changes/modulations.
2. **RMS Enegy profiling**. The varying dynamics of a piece of music are calculated by tracking the RMS energy over the course of a piece. Sections of a piece that are loud (by default) or have a high amount of dynamic variation (`--difference` flag) are preferred for inclusion in the audio snippet generated.
3. **Applause detection**. An algorithm that determines [spectral centroid](https://dx.doi.org/10.1121%2F1.381843) over time is used to detect applause within a recording. Periods of applause are avoided in the resulting audio thumbnail. 

It is available under the GNU GPLv2 license, as detailed below and in [LICENSE](LICENSE)

##Installation

Cleverthumbnailer can be installed using Python setuptools:

1. Install dependencies
    - *Note: cleverthumbnailer requires the QM-DSP library, which (currently) must be built from source—see [Dependencies](#Dependencies)*
2. Open a terminal, and cd to this repository
3. Run `python setup.py install`
4. Check that Cleverthumbnailer runs by typing (from this or any other directory) `cleverthumbnailer -h`

##Usage

Cleverthumbnauiler is a command-line python application, and will create an audio thumbnail file in the same format and directory as some input file, using sensible defaults, by typing `cleverthumbnailer inputfile.wav`. Optional command-line arguments can be provided to override these defaults, and a brief overview of these is given by typing 'cleverthumbnailer -h'.

###Command Line arguments

A more detailed explanation of the application's command line arguments is given as follows:

####Required arguments:

Name    | Description
----    | -----------
`input` | Input wav file to be processed (one only). Cleverthumbnailer supports uncompressed 8 or 16-bit WAVE/BWF files using the Python2 [`wave`](https://docs.python.org/2/library/wave.html) library. |

####Optional parameters:

Name    | Default | Description
----    | ------- | -----------
`h, --help` || Show help message on command line
`v, --verbose` || Increase logging verbosity level
`q, --quiet` || Only log errors
`f in out, --fade in out` | `0.5` `0.5` | Fade in and out times (seconds)
`c in out, --crop in out` | `7` `7` | Crop time (seconds) — the amount of time at the beginning and end of a track to ignore when choosing thumbnails
`l seconds, --length seconds` | `30` | Thumbnail length (seconds)
`d, --dynamic` || Rate sections by dynamic range rather than max loudness when choosing thumbnails
`n, --noapplause` || Skip applause detection
`o wavfile, --output wavfile` || Output file path

##Dependencies

Cleverthumbnailer depends on the following:

* [Python2.7](https://www.python.org/download/releases/2.7/)
    - Included in many operating systems by default, or can be downloaded from the above site.
* [SoX - Sound eXchange](http://sox.sourceforge.net/), which is called upon to create audio thumbnails themselves.
    - Available through the above site, or in many operating system package managers:
        + MacOS (homebrew): `brew install sox`
        + Ubuntu/Debian (apt): `apt-get install sox`
    - On windows, you will have to add SoX to your shell `%PATH%` manually, so that it can be called by Cleverthumbnailer
        + `setx PATH=%PATH%;C:\Program Files (x86)\sox-14-4-2`
* [qm-segmenter-python](https://github.com/bbc/qm-segmenter-python), a python wrapper around the [QM-DSP](https://code.soundsoftware.ac.uk/projects/qm-dsp) audio segmenter. This (currently) in turn requires building QM-DSP from source—please check the README file in the qm-segmenter-python repository for more information.

##Credits

The code in this repository was created by Jon Tutcher in 2015 for [BBC Research & Development](http://www.bbc.co.uk/rd).

##License

This project is licensed under the GNU GPLv2 license. For terms and conditions, see [LICENSE](LICENSE).