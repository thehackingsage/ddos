#ifndef __CAPTURETHREAD_H__
#define __CAPTURETHREAD_H__

extern "C" { 
	#include <pthread.h>
	#include <errno.h>
}

void *capEngineThread(void *arg);


#endif

