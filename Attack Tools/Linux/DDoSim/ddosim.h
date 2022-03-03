#ifndef __DCPPSIM_H__
#define __DCPPSIM_H__

#include <string>
#include <map>


extern "C" { 
	#include <libnet.h>
	#include <pthread.h>
	#include <string.h>
	#include <errno.h>
}

#ifndef LIBNET_ERR_BUF
#define LIBNET_ERR_BUF 255
#endif

#define HTTP_VALID 		1001
#define HTTP_INVALID 		1002
#define SMTP_EHLO 		1003

#define STATE_SYN_SENT  	200
#define STATE_ESTABLISHED  	201

using namespace std;

class Pkt {

	public:
		u_long srcIp;
		u_long dstIp;
		int srcPort;
		int dstPort;
		int seqn;
		int ackn;
};

class ConnInfo {
	public:
		u_long srcIp;  	//may be eliminated?
		int srcPort;	//may be eliminated?
		int state;
};

u_long getLocalIp(string const &ifName, string &error);
void mydelay(int wait);
string connId(u_long ip, int port);

#endif
