noinst_LIBRARIES = libqmsegmenter.a

libqmsegmenter_a_CXXFLAGS = -I../kissfft -Dkiss_fft_scalar=double
libqmsegmenter_a_LIBADD = ../kissfft/libkissfft.a
libqmsegmenter_a_SOURCES = \
    cblas.h \
    Chromagram.cpp \
    Chromagram.h \
    clapack.h \
    cluster_melt.c \
    cluster_melt.h \
    cluster_segmenter.c \
    cluster_segmenter.h \
    ClusterMeltSegmenter.cpp \
    ClusterMeltSegmenter.h \
    ConstantQ.cpp \
    ConstantQ.h \
    Decimator.cpp \
    Decimator.h \
    FFT.cpp \
    FFT.h \
    hmm.c \
    hmm.h \
    MathAliases.h \
    MathUtilities.h \
    MFCC.cpp \
    MFCC.h \
    nan-inf.h \
    pca.c \
    pca.h \
    Segmenter.cpp \
    Segmenter.h \
    Window.h

noinst_PROGRAMS = segmenter-test
segmenter_test_SOURCES = segmenter_test.cpp
segmenter_test_CXXFLAGS = $(SNDFILE_CFLAGS) $(WARNING_CFLAGS)
segmenter_test_LDADD = libqmsegmenter.a ../kissfft/libkissfft.a $(SNDFILE_LIBS)
