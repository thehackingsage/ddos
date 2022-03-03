AUTOMAKE_OPTIONS = foreign

INCLUDES=`libnet-config --defines` -Wall -Wno-deprecated -O2
LDFLAGS=-lnet -lpcap -lpthread

bin_PROGRAMS = ddosim
ddosim_SOURCES = ddosim.cpp sniffer.cpp senderThread.cpp captureThread.cpp tcpUtils.cpp \
ddosim.h sniffer.h senderThread.h captureThread.h tcpUtils.h

