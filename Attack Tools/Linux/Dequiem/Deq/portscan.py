#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#+--------------------+
#|Creators :          |
#|-Drarqua GHS Storm  |
#|-Rebel Yell         |
#+--------------------+

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time
import socket
import os
import sys
import string

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
curdir = os.getcwd()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

address = raw_input( "Choose your target:" )
start = input( "From port:" )
stop = input( "To port:" )
openportsL = []
def portscan(address, port):
    ps = socket.socket()
    print ("Searching for open ports")
    try:
        ps.connect((address, port))
        print ("[Port %s is OPEN.]") %(port)
        openportsL[1:1] = [port]
        return True
    except socket.error, msg:
        return False
    s.close()
print ("Port Scan Started ... It may take time")
for port in range(start, stop):
    portscan(address, port)
print ("Port Scann completed")
print ("The open ports are :")
print ( openportsL )
if __name__ == "__main__":
    answer = raw_input("Do you want to Portscan again?")
    if answer.strip() in "y Y yes Yes YES".split():
        restart_program()
    else:
        os.system(curdir+"\Deq\main.py")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
