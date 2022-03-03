#ifndef __SENDER_THREAD_H__
#define __SENDER_THREAD_H__

#include "ddosim.h"
#include <string>

using namespace std;

class SenderThreadArg {
	public:
		string ifName;
		bool doSpoof;
		int count;
		int *synNo;	 //connections initiated
		int *connNo; //connections completed
		int wait;
		int verbose;
		u_long victimIp;
		int victimPort;
		string srcNetStr;
		int threadId;
		int requestType;
		bool *run;
};

void *senderThread(void *arg);
int getNumConnsEstab();

#endif

