#CleverThumbnailer

Cleverthumbnailer is a Python2 application that analyses songs and creates short audio thumbnails of them based.

## Algorithm

Given a full length piece of music in WAVE format (`*.bwf` and `*.wav`), cleverthumbnailer attempts to generate a short extract most representative of the track in general. It bases this decision on three factors:

1. **Segment Detection**. Using the [QMUL Segmenter](http://dx.doi.org/10.1109/TASL.2007.910781) algorithm, distinct musical sections of a piece are found. In western pop music, this algorithm detects transitions between verses, choruses, and bridges. In western classical music, segment boundaries are often found at key changes/modulations.
2. **RMS Energy profiling**. The varying dynamics of a piece of music are
calculated by tracking the RMS energy over the course of a piece. Sections of a piece that are loud (by default) or have a high amount of dynamic variation (`--difference` flag) are preferred for inclusion in the audio snippet generated.
3. **Applause detection**. An algorithm that determines [spectral centroid](https://dx.doi.org/10.1121%2F1.381843) over time is used to detect applause within a recording. Periods of applause are avoided in the resulting audio thumbnail. 

##Installation

1. Install dependencies
  * MacOS (homebrew): `brew install python sox`
  * Ubuntu/Debian (apt): `apt-get install python2.7 python-numpy python-setuptools sox`
  * CentOS (yum): `yum install python-devel numpy python-setuptools python-enum sox`
2. Install [qm-segmenter-python](https://github.com/bbc/qm-segmenter-python)
3. Run `python2 setup.py install`

##Usage

Cleverthumbnailer is a command-line python application, and will create an audio thumbnail file in the same format and directory as some input file, using sensible defaults, by typing `cleverthumbnailer inputfile.wav`. Optional command-line arguments can be provided to override these defaults, and a brief overview of these is given by typing 'cleverthumbnailer -h'.

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
`p seconds, --prelude seconds` | `10` | Length of additional lead-in audio
to include prior to calculated thumbnail start
`d, --dynamic` || Rate sections by dynamic range rather than max loudness when choosing thumbnails
`a, --applause` || Use applause detection
`o wavfile, --output wavfile` || Output file path

##Credits

The code in this repository was created by Jon Tutcher in 2015 for [BBC Research & Development](http://www.bbc.co.uk/rd).

[QM-DSP](https://code.soundsoftware.ac.uk/projects/qm-dsp) was created by Queen Mary University of London; the segmenter module used here was developed by Mark Levy and Chris Cannam.

Cleverthumbnailer also includes and makes use of the Python [appdirs](https://github.com/ActiveState/appdirs) module, credits for which are included in appdirs.py. 

##License

This project is licensed under the GNU GPLv2 license. For terms and conditions, see [LICENSE](LICENSE).
