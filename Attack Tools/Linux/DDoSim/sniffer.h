#ifndef __SNIFFER_H__
#define __SNIFFER_H__

#include <netinet/ether.h>
#include <arpa/inet.h>

#include <string>
#include <pcap.h>

using namespace std;

struct ip_header {
	u_int8_t	ip_vhl;		/* header length, version */
#define IP_V(ip)	(((ip)->ip_vhl & 0xf0) >> 4)
#define IP_HL(ip)	((ip)->ip_vhl & 0x0f)
	u_int8_t	ip_tos;		/* type of service */
	u_int16_t	ip_len;		/* total length */
	u_int16_t	ip_id;		/* identification */
	u_int16_t	ip_off;		/* fragment offset field */
#define	IP_DF 0x4000		/* dont fragment flag */
#define	IP_MF 0x2000		/* more fragments flag */
#define	IP_OFFMASK 0x1fff	/* mask for fragmenting bits */
	u_int8_t	ip_ttl;		/* time to live */
	u_int8_t	ip_p;		/* protocol */
	u_int16_t	ip_sum;		/* checksum */
	struct	in_addr ip_src, ip_dst;	/* source and dest address */
};

/* TCP header */
struct tcp_header {
	u_short th_sport;	/* source port */
	u_short th_dport;	/* destination port */
	u_int32_t th_seq;		/* sequence number */
	u_int32_t th_ack;		/* acknowledgement number */

	u_char th_offx2;	/* data offset, rsvd */
#define TH_OFF(th)	(((th)->th_offx2 & 0xf0) >> 4)
	u_char th_flags;
#define TH_FIN 0x01
#define TH_SYN 0x02
#define TH_RST 0x04
#define TH_PUSH 0x08
#define TH_ACK 0x10
#define TH_URG 0x20
#define TH_ECE 0x40
#define TH_CWR 0x80
#define TH_FLAGS (TH_FIN|TH_SYN|TH_RST|TH_ACK|TH_URG|TH_ECE|TH_CWR)
	u_short th_win;		/* window */
	u_short th_sum;		/* checksum */
	u_short th_urp;		/* urgent pointer */
};


class Sniffer
{
	private:
		pcap_t *handle;					/* Session handle */
		char errbuf[PCAP_ERRBUF_SIZE];	/* Error string */

	public:
		string dev;						/* Device to sniff on */
		string filter_exp;				/* The filter expression */
		bpf_u_int32 mask;				/* Our netmask */
		bpf_u_int32 net;				/* Our network address */
		bool initialized;
		bool run;
		int* rstNo;		//number of RST-ACK packets received from server
		int* finNo;		//number of FIN-ACK packets received from server
		Sniffer();
		~Sniffer();
		bool init(string &ifName, int* rstNo, int* finNo, string &error);
		void readPackets(pcap_handler processPacket, u_char* args);
		static bool checkIpHeader(const struct pcap_pkthdr* pkthdr, const u_char* packet, string &error);	
		static bool checkTcpHeader(const struct pcap_pkthdr* pkthdr, const u_char* packet, string &error);

		static string getSrcIp(const u_char* packet);
		static string getDstIp(const u_char* packet);
		static int getSrcIpRaw(const u_char* packet);
		static int getDstIpRaw(const u_char* packet);
		static int getTcpDstPort(const u_char* packet);
		static int getTcpSrcPort(const u_char* packet);
		static int getTcpSEQ(const u_char* packet);
		static int getTcpACK(const u_char* packet);
		static bool isRst(const u_char* packet);
		static bool isFin(const u_char* packet);
		static string getTcpData(const struct pcap_pkthdr* pkthdr, const u_char* packet);
};


#endif

