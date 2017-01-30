
dnl ############# Initialization

AC_PREREQ([2.62])
AC_INIT([clever-thumbnailer],[0.1.0])
AC_CONFIG_SRCDIR([src/clever-thumbnailer.c])
AC_CONFIG_HEADERS([src/config.h])
AC_CONFIG_AUX_DIR(build-scripts)
AC_CONFIG_MACRO_DIR(build-scripts)
AM_INIT_AUTOMAKE([1.11 foreign -Wobsolete -Wportability -Wsyntax -Wunsupported -Wextra-portability])

AM_MAINTAINER_MODE



dnl ############# Compiler and tools Checks

AM_SANITY_CHECK
AC_PROG_CC
AC_PROG_CC_C99
AC_PROG_CXX

AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_RANLIB

m4_ifdef([AM_PROG_AR], [AM_PROG_AR])

AC_C_CONST
AC_C_BIGENDIAN
AC_C_INLINE



dnl ############## Header and function checks

AC_HEADER_STDC
AC_CHECK_HEADERS([stdlib.h])
AC_FUNC_MALLOC
AC_FUNC_REALLOC



dnl ############## Check for packages we depend upon

AC_CHECK_LIB([cblas], [cblas_ddot],, [
    AC_MSG_ERROR([Couldn't find cblas_ddot in libcblas])
])
AC_CHECK_LIB([lapack], [dgetrf],, [
    AC_CHECK_LIB([lapack], [dgetrf_],, [
        AC_MSG_ERROR([Couldn't find dgetrf or dgetrf_ in liblapack])
    ])
])

PKG_CHECK_MODULES(SNDFILE, sndfile >= 1.0.18)


dnl ############## Compiler and Linker Flags

# If maintainer mode is enabled then make warnings errors
if test "$USE_MAINTAINER_MODE" = yes; then
  WARNING_CFLAGS="-Wall -Werror -pedantic -Wunused"
  WARNING_CFLAGS="$WARNING_CFLAGS -Wmissing-prototypes"
  AC_SUBST(WARNING_CFLAGS)
fi



dnl ############## Output files

AC_CONFIG_FILES([
  Makefile
  kissfft/Makefile
  qmsegmenter/Makefile
  src/Makefile
])

AC_OUTPUT
