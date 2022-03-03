#ifndef __TCPUTILS_H__
#define __TCPUTILS_H__

extern "C" { 
	#include <libnet.h>
}

class TcpUtils {

	public:
	static void buildSYN(u_char *packet, u_long sourceIp, u_long victimIp, int sourcePort, int victimPort, int seqn, int ackn);
	static void buildACK(u_char *packet, u_long sourceIp, u_long victimIp, int sourcePort, int victimPort, int seqn, int ackn);
	static void buildTcpData(u_char *packet, 
							u_long sourceIp, u_long victimIp, 
							int sourcePort, int victimPort, 
							int seqn, int ackn, 
							const u_char *payload);
};

#endif

