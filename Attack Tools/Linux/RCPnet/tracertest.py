#!/usr/bin/env python
# (c) December 2007 Thomas Guettler http://www.thomas-guettler.de
# tcptraceroute.py
# This script is in the public domain

import os
import re
import sys
import struct
import socket

def usage():
    print '''Usage: %s host port
Tries to connect to host at TCP port with increasing TTL (Time to live).
If /etc/services exists (on most Unix systems), you can give the protocol
name for the port. Example 'ssh' instead of 22.
''' % os.path.basename(sys.argv[0])

def main():
    if not len(sys.argv)==3:
        usage()
        sys.exit(1)
    ttl=1
    host, port = sys.argv[1:]
    port_int=None
    try:
        port_int=int(port)
    except ValueError:
        if not os.path.exists('/etc/services'):
            print 'port needs to be an integer if /etc/services does not exist.'
            sys.exit(1)
        fd=open('/etc/services')
        for line in fd:
            match=re.match(r'^%s\s+(\d+)/tcp.*$' % port, line)
            if match:
                port_int=int(match.group(1))
                break
        if not port_int:
            print 'port %s not in /etc/services' % port
            sys.exit(1)
    port=port_int
    for ttl in range(1, 30):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
        s.settimeout(2)
        try:
            try:
                s.connect((host, port))
            except (socket.error, socket.timeout), err:
                print 'ttl=%02d: %s' % (ttl, err)
                continue
            except KeyboardInterrupt:
                print 'ttl=%02d (KeyboardInterrupt)' % ttl
                break
        finally:
            s.close()
        print 'ttl=%02d: OK' % (ttl)
        break

if __name__=='__main__':
    main()