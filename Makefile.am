ACLOCAL_AMFLAGS = -I build-scripts
SUBDIRS = kissfft qmsegmenter src .

# Copy README.md to README when building distribution
README:
	[ -f README.md ] && fgrep -v "Build Status]" $(top_srcdir)/README.md > $@ || true

test: check
