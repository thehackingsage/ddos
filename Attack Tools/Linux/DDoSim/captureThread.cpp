#include <iostream>
#include <map>
#include <list>
#include "captureThread.h"
#include "sniffer.h"
#include "tcpUtils.h"
#include "ddosim.h"

using namespace std;

extern list<Pkt> pktsToSend; 					//first send these packets
extern map<string, ConnInfo> connsInited;		//info about initiated connections
extern map<string, ConnInfo> connsEstab;		//info about established connections
extern pthread_mutex_t connMutex; //mutual exclusion when accessing the connsInited map
extern pthread_mutex_t ackMutex;  //mutual exclusion when accessing pktsToSend (ACKs)
extern pthread_mutex_t countMutex;  //mutual exclusion when accessing pktsToSend (ACKs)

extern bool v; 	//verbose

void processPacket(u_char *args, const struct pcap_pkthdr* pkthdr, const u_char* packet);

void* capEngineThread(void *arg)
{
	if(v)cout << "Capture Engine started " << endl;
	Sniffer *snf = (Sniffer *)arg;
	snf->readPackets(processPacket, (u_char *)arg);
	if(v)cout << "Capture Engine stopped " << endl;
	return 0;
}

void processPacket(u_char *args, const struct pcap_pkthdr* pkthdr, const u_char* packet)
{
	Sniffer *snf = (Sniffer *)args;
	map<string, ConnInfo>::iterator it;

	u_long dstIp = snf->getDstIpRaw(packet);
	int dstPort = snf->getTcpDstPort(packet);
	
	if(snf->isRst(packet)) {
		if(v)cout << "Got RST-ACK packet from " << snf->getSrcIp(packet) << " to " << snf->getDstIp(packet) << endl;
	} else if(snf->isFin(packet)){
		if(v)cout << "Got FIN-ACK packet from " << snf->getSrcIp(packet) << " to " << snf->getDstIp(packet) << endl;
		pthread_mutex_lock(&connMutex);
		it = connsEstab.find(connId(dstIp, dstPort));
		if(it != connsEstab.end()) { 	// we received FIN for an established TCP connection
			connsEstab.erase(it);		// delete the established connections
			pthread_mutex_unlock(&connMutex);
			pthread_mutex_lock(&countMutex);
			(*snf->finNo)++;			// increase number of finished connections
			pthread_mutex_unlock(&countMutex);
		} else {
			pthread_mutex_unlock(&connMutex);
		}
	} else {
		if(v)cout << "Got SYN-ACK packet from " << snf->getSrcIp(packet) << " to " << snf->getDstIp(packet) << endl;
	}

	pthread_mutex_lock(&connMutex);
	it = connsInited.find(connId(dstIp, dstPort));
	if(it != connsInited.end()) {
		if(v)cout << "Found session " << endl;
		connsInited.erase(it);
		pthread_mutex_unlock(&connMutex);

		if(snf->isRst(packet)) {
			pthread_mutex_lock(&countMutex);
			(*snf->rstNo)++;
			pthread_mutex_unlock(&countMutex);
			return;
		} else if(snf->isFin(packet)) {
			pthread_mutex_lock(&countMutex);
			(*snf->finNo)++;
			pthread_mutex_unlock(&countMutex);
			return;
		}
		
		Pkt pkt; //This is the ACK packet that we send
		pkt.srcIp = snf->getDstIpRaw(packet);
		pkt.dstIp = snf->getSrcIpRaw(packet);
		pkt.srcPort = snf->getTcpDstPort(packet);
		pkt.dstPort = snf->getTcpSrcPort(packet);
		pkt.seqn = snf->getTcpACK(packet);
		pkt.ackn = snf->getTcpSEQ(packet) + 1;

		pthread_mutex_lock(&ackMutex);
		pktsToSend.push_back(pkt);			//ACKs will be sent from this queue (to complete 3-way handshake)
		pthread_mutex_unlock(&ackMutex);
	} else {
		pthread_mutex_unlock(&connMutex);
	}
}

