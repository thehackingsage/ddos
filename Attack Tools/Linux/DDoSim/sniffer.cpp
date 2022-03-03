#include <iostream>
#include <string.h>
#include <assert.h>
#include "sniffer.h"

Sniffer::Sniffer()
{
	dev = "eth0";
	//catch SYN-ACK, RST-ACK and FIN-ACK
	filter_exp = "tcp[tcpflags]&tcp-syn != 0 && tcp[tcpflags]&tcp-ack != 0 ";
	filter_exp += "|| tcp[tcpflags]&tcp-rst != 0 && tcp[tcpflags]&tcp-ack != 0 ";
	filter_exp += "|| tcp[tcpflags]&tcp-fin != 0 && tcp[tcpflags]&tcp-ack != 0 ";
	initialized = false;
	run = true;
	handle = NULL;
}

Sniffer::~Sniffer()
{
	if(handle) {
		pcap_close(handle);
	}
}

bool Sniffer::init(string &ifName, int* rstNo, int* finNo, string &error)
{
	dev = ifName;
	this->rstNo = rstNo;
	this->finNo = finNo;
	struct bpf_program fp;			/* The compiled filter */

	/* Find the properties for the device */
	if (pcap_lookupnet((char*)dev.c_str(), &net, &mask, errbuf) == -1) {
		error = string("pcap_lookupnet() error: ") + errbuf;
		return false;
	}

	/* Open the session in promiscuous mode */
	handle = pcap_open_live((char*)dev.c_str(), BUFSIZ, 1, 1000, errbuf);
	if (handle == NULL) {
		error = "Couldn't open device " + dev + " because: " + string(errbuf);
		return false;
	}
	/* Compile and apply the filter */
	if (pcap_compile(handle, &fp, (char*)filter_exp.c_str(), 0, net) == -1) {
		error = "Couldn't parse filter " +  filter_exp + " because: " + string(pcap_geterr(handle));
		return false;
	}
	if (pcap_setfilter(handle, &fp) == -1) {
		error = "Couldn't install filter " + filter_exp + " because: " + string(pcap_geterr(handle));
		return false;
	}

	initialized = true;
	return true;
}


/* void processPacket(u_char *args, const struct pcap_pkthdr* pkthdr, const u_char* packet) */
void Sniffer::readPackets(pcap_handler processPacket, u_char* args)
{
	assert(initialized == true);
	int count;
	while(run) {
		count = pcap_dispatch(handle, 1, processPacket, args);
		if(count == 0) {
			//cout << "pcap_dispatch() timeout" << endl;
		} else if (count == -1) {
			cout << "pcap_dispatch() error" << endl;
		}
	}
}

bool Sniffer::checkIpHeader(const struct pcap_pkthdr* pkthdr, const u_char* packet, string &error)
{
	const struct ip_header* ip;
    u_int length = pkthdr->len;
    u_int hlen, version;
    unsigned int len;

    /* jump pass the ethernet header */
    ip = (struct ip_header*)(packet + sizeof(struct ether_header));
    length -= sizeof(struct ether_header); 

    /* check to see we have a packet of valid length */
    if (length < sizeof(struct ip_header)) {
        error = "Truncated ip";
        return false;
    }

    len     = ntohs(ip->ip_len);
    hlen    = IP_HL(ip); 			/* header length */
    version = IP_V(ip);				/* ip version */

    /* check version */
    if(version != 4) {
		error = "Unknown IP version";
		return false;
    }

    /* check header length */
//     if(hlen < 5 ) {
//         printf("Bad header length %d \n",hlen);
//     }
    /* see if we have as much packet as we should */
//     if(length < len) {
//         printf("Truncated IP - %d bytes missing\n",len - length);
// 	}
	return true;
}

bool Sniffer::checkTcpHeader(const struct pcap_pkthdr* pkthdr, const u_char* packet, string &error)
{
	if(!checkIpHeader(pkthdr, packet, error)) {
		return false;
	}

	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 

	if(ip->ip_p != IPPROTO_TCP) {
		error = "Not a tcp packet";
		return false;
	}

	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
	u_int tcp_hlen = TH_OFF(tcp)*4;
	if (tcp_hlen < 20) {
		error = "Invalid TCP header length";
		return false;
	}

	return true;
}


//assumes the ip header checking has already been done
string Sniffer::getSrcIp(const u_char* packet)
{
	const struct ip_header* ip;
    ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	return string(inet_ntoa(ip->ip_src));
}

int Sniffer::getSrcIpRaw(const u_char* packet)
{
	const struct ip_header* ip;
    ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	return ip->ip_src.s_addr;
}

//assumes the ip header checking has already been done
string Sniffer::getDstIp(const u_char* packet)
{
	const struct ip_header* ip;
    ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	return string(inet_ntoa(ip->ip_dst));
}

int Sniffer::getDstIpRaw(const u_char* packet)
{
	const struct ip_header* ip;
    ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	return ip->ip_dst.s_addr;
}

//assumes the tcp header checking has already been done
int Sniffer::getTcpDstPort(const u_char* packet)
{
	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 

	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
 	return ntohs(tcp->th_dport);
}

//assumes the tcp header checking has already been done
int Sniffer::getTcpSrcPort(const u_char* packet)
{
	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 
	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
 	return ntohs(tcp->th_sport);
}

int Sniffer::getTcpSEQ(const u_char* packet)
{
	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 

	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
	return ntohl(tcp->th_seq);
}

int Sniffer::getTcpACK(const u_char* packet)
{
	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 

	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
	return ntohl(tcp->th_ack);
}


string Sniffer::getTcpData(const struct pcap_pkthdr* pkthdr, const u_char* packet)
{
	u_int length = pkthdr->len;		// whole packet length

	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 
	length -= sizeof(struct ether_header);

	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
	u_int tcp_hlen = TH_OFF(tcp)*4;
	length -= ip_hlen;

	u_char* payload = (u_char *)(packet + sizeof(struct ether_header) + ip_hlen + tcp_hlen);
	length -= tcp_hlen;

	char* buf = new char[length+1];
	memset(buf, 0, length+1);
	memcpy(buf, payload, length);
	string ret = (char*)buf;			//this does not work when data contains 0
	delete buf;

	return ret;
}

bool Sniffer::isRst(const u_char* packet) {
	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 

	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
	return tcp->th_flags & TH_RST;
}

bool Sniffer::isFin(const u_char* packet) {
	const struct ip_header* ip = (struct ip_header*)(packet + sizeof(struct ether_header));
	u_int ip_hlen    = IP_HL(ip)*4; 	// ip header length 

	const struct tcp_header* tcp = (struct tcp_header*)(packet + sizeof(struct ether_header) + ip_hlen);
	return tcp->th_flags & TH_FIN;
}


/*
int getDevAddress(char* dev, struct in_addr* ip, char* errbuf)
{
	ip->s_addr = 0;
	pcap_if_t *interfaces;
	struct sockaddr_in *saddr;
	int retValue = FALSE;
	if(pcap_findalldevs(&interfaces, errbuf) != 0) {
		return FALSE;
	}
	if(interfaces == NULL) {
		sprintf(errbuf, "No interfaces found!");
		retValue = FALSE;
	} else {
		for(pcap_if_t *pif = interfaces; pif != NULL; pif = pif->next) {
			if(strcmp(dev, pif->name) == 0) {
				if(pif->addresses != NULL) {
					if (pif->addresses->addr->sa_family == AF_INET) {
						saddr = (struct sockaddr_in*)pif->addresses->addr;
						assert(saddr != NULL);
						printf("address: %s", inet_ntoa(saddr->sin_addr));
						retValue = TRUE;
					} else {
						sprintf(errbuf, "Interface %s is not of the AF_INET type! %i", pif->name, pif->addresses->addr->sa_family);
						struct sockaddr_ll *sll = (struct sockaddr_ll*)pif->addresses->addr;
						for(int i=0; i < 8; i++) {
							printf("%c\n", sll->sll_addr[i]);
						}
						retValue = FALSE;
					}
					break;
				} else {
					sprintf(errbuf, "Interface %s has no ip address!", pif->name);
					retValue = FALSE;
					break;
				}
			}
		}
	}
	pcap_freealldevs (interfaces);
	return retValue;
}
*/
