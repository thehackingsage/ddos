#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT([ddosim], [0.2], [adif2k8@gmail.com])
AC_CONFIG_SRCDIR([tcpUtils.cpp])
#AC_CONFIG_HEADER([config.h])

AM_INIT_AUTOMAKE([ddosim], [0.2])

AC_CONFIG_FILES([Makefile])


# Checks for programs.
AC_PROG_CXX
AC_PROG_CC

# Checks for libraries.
AC_CHECK_LIB([pcap], [pcap_open_live], [], AC_MSG_ERROR([libpcap (dev) is required for this program]))
AC_CHECK_LIB([pthread], [pthread_mutex_lock], [], AC_MSG_ERROR([libpthread (dev)is required for this program]))
AC_CHECK_LIB([net], [libnet_init_packet], [], AC_MSG_ERROR([libnet0 (dev) is required for this program]))

# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([arpa/inet.h string.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_CONST

# Checks for library functions.
AC_CHECK_FUNCS([gethostbyname inet_ntoa memset strerror])

AC_OUTPUT


