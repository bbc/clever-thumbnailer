AM_CFLAGS = $(SNDFILE_CFLAGS) $(WARNING_CFLAGS)
AM_CXXFLAGS = -I../qmsegmenter $(SNDFILE_CFLAGS) $(WARNING_CFLAGS)

bin_PROGRAMS = clever-thumbnailer
clever_thumbnailer_LDADD = ../qmsegmenter/libqmsegmenter.a ../kissfft/libkissfft.a $(SNDFILE_LIBS)
clever_thumbnailer_SOURCES = \
  clever-thumbnailer.c \
  analysis.cpp \
  utils.c \
  trim.c

noinst_PROGRAMS = loudness-test
loudness_test_CFLAGS = $(SNDFILE_CFLAGS) $(WARNING_CFLAGS)
loudness_test_LDADD = $(SNDFILE_LIBS)
loudness_test_SOURCES = loudness-test.c loudness.c utils.c
