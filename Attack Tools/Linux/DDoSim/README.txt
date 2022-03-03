Installation
------------
./configure
make
make install


Usage
-----
./ddosim
     -d IP           Target IP address
     -p PORT         Target port
    [-k NET]         Source IP from class C network  (ex. 10.4.4.0)
    [-i IFNAME]      Output interface name
    [-c COUNT]       Number of connections to establish
    [-w DELAY]       Delay (in milliseconds) between SYN packets
    [-r TYPE]        Request to send after TCP 3-way handshake. TYPE can be HTTP_VALID or HTTP_INVALID or SMTP_EHLO
    [-t NRTHREADS]   Number of threads to use when sending packets (default 1)
    [-n]             Do not spoof source address (use local address)
    [-v]             Verbose mode (slower)
    [-h]             Print this help message
