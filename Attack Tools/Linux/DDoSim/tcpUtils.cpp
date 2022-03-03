#include "tcpUtils.h"
#include <iostream>

using namespace std;

void TcpUtils::buildSYN(u_char *packet, u_long sourceIp, u_long victimIp, int sourcePort, int victimPort, int seqn, int ackn) {

    libnet_build_ip(LIBNET_TCP_H,   /* size of the packet sans IP header */
            IPTOS_LOWDELAY,         /* IP tos */
            242,                    /* IP ID */
            0,                      /* frag stuff */
            48,                     /* TTL */
            IPPROTO_TCP,            /* transport protocol */
            sourceIp, 				/* source IP */
            victimIp,               /* destination IP */
            NULL,                   /* payload (none) */
            0,                      /* payload length */
            packet);                /* packet header memory */

    libnet_build_tcp(sourcePort,	/* source TCP port */
            victimPort,             /* destination TCP port */
            seqn,	                /* sequence number */
            ackn,                   /* acknowledgement number */
            TH_SYN,                 /* control flags */
            1024,                   /* window size */
            0,                      /* urgent pointer */
            NULL,                   /* payload (none) */
            0,                      /* payload length */
            packet + LIBNET_IP_H);  /* packet header memory */

    if (libnet_do_checksum(packet, IPPROTO_TCP, LIBNET_TCP_H) == -1) {
        libnet_error(LIBNET_ERR_FATAL, (char*)"libnet_do_checksum failed\n");
    }

}

void TcpUtils::buildACK(u_char *packet, u_long sourceIp, u_long victimIp, int sourcePort, int victimPort, int seqn, int ackn) {

    libnet_build_ip(LIBNET_TCP_H,   /* size of the packet sans IP header */
            IPTOS_LOWDELAY,         /* IP tos */
            242,                    /* IP ID */
            0,                      /* frag stuff */
            48,                     /* TTL */
            IPPROTO_TCP,            /* transport protocol */
            sourceIp, 				/* source IP */
            victimIp,               /* destination IP */
            NULL,                   /* payload (none) */
            0,                      /* payload length */
            packet);                /* packet header memory */

    libnet_build_tcp(sourcePort,	/* source TCP port */
            victimPort,             /* destination TCP port */
            seqn,	                /* sequence number */
            ackn,                   /* acknowledgement number */
            TH_ACK,                 /* control flags */
            5840,                   /* window size */
            0,                      /* urgent pointer */
            NULL,                   /* payload (none) */
            0,                      /* payload length */
            packet + LIBNET_IP_H);  /* packet header memory */

    if (libnet_do_checksum(packet, IPPROTO_TCP, LIBNET_TCP_H) == -1) {
        libnet_error(LIBNET_ERR_FATAL, (char*)"libnet_do_checksum failed\n");
    }

}

void TcpUtils::buildTcpData(u_char *packet, u_long sourceIp, u_long victimIp, int sourcePort, int victimPort, int seqn, int ackn, const u_char *payload) {
    libnet_build_ip(LIBNET_TCP_H + strlen((const char*)payload),   /* size of the packet sans IP header */
            IPTOS_LOWDELAY,         /* IP tos */
            242,                    /* IP ID */
            0,                      /* frag stuff */
            48,                     /* TTL */
            IPPROTO_TCP,            /* transport protocol */
            sourceIp, 				/* source IP */
            victimIp,               /* destination IP */
            NULL,                   /* payload (none) */
            0,                      /* payload length */
            packet);                /* packet header memory */

    libnet_build_tcp(sourcePort,	/* source TCP port */
            victimPort,             /* destination TCP port */
            seqn,	                /* sequence number */
            ackn,                   /* acknowledgement number */
            TH_ACK|TH_PUSH,         /* control flags */
            5840,                   /* window size */
            0,                      /* urgent pointer */
            payload,                /* payload (none) */
            strlen((const char*)payload), /* payload length */
            packet + LIBNET_IP_H);  /* packet header memory */

    if (libnet_do_checksum(packet, IPPROTO_TCP, LIBNET_TCP_H + strlen((const char*)payload)) == -1) {
        libnet_error(LIBNET_ERR_FATAL, (char*)"libnet_do_checksum failed\n");
    }
}






