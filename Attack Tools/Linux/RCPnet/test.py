#Actualizado Lunes,28 de mayo dos mil diez y ocho
#Autor: Rosnel Alejandro Leyva-Cortes#
import os
import re
import sys
import struct
import socket
import urllib
import time
from subprocess import Popen, PIPE
import json as m_json
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
try:
    import urllib.request #Python3.x
except ImportError:
    import urllib2 #Python2.x
#End of import#

def q():
    print(''' You are a horrible ''')
    exit()

#initial ping
#for the hostname

def ping ():
    welcome = str = raw_input('''\nIn order to perform a test, we must determine if the host is up.''')
    hostname = str1 = raw_input("\nInput Hostname: ")
    response = os.system("ping -c 10 " + hostname)

    #and then check the response...
    if response == 0:
        print (hostname + ' is up! ') #End result is self explanatory
        mainMenu()
def Cloudflare():
     print('Not ready yet')
     mainMenu()

def traceroute(url,*arg):
    print('''This function uses ICMP to trace a host and give an IP.
    Please run as root and don't include HTTPS in url. ''')
    url = raw_input("\nPlease type in url to traceroute a website: ");
    while True:
        if 'http' not in url:
            url = "http://" + url
        elif "www" not in url:
            url = "www."[:7] + url[7:]
        else:
            url = url
            break
    url = urlparse(url)
    url = url.netloc
    print(url)
    p = Popen(['tracert', url], stdout=PIPE)
    while True:
        line = p.stdout.readline()
        line2 = str(line).replace('\\r','').replace('\\n','')
        if len(arg)>0:
            file = open(arg[0], "a")
            file.write(line2)
            file.close()
        print(line2)
        if not line:
            break



def mainMenu():
        print (''' 
     _______    ______   _______  
    /       \  /      \ /       \ 
    $$$$$$$  |/$$$$$$  |$$$$$$$  |
    $$ |__$$ |$$ |  $$/ $$ |__$$ |
    $$    $$< $$ |      $$    $$/ 
    $$$$$$$  |$$ |   __ $$$$$$$/  
    $$ |  $$ |$$ \__/  |$$ |      
    $$ |  $$ |$$    $$/ $$ |      
    $$/   $$/  $$$$$$/  $$/  net   

    https://sourceforge.net/projects/rcpnet/
    https://twitter.com/PotatoSkins16
    Choose one
                              ''')
        print('1. Ping host')
        print('2. Cloudflare check')
        print('3. tracert')
        print('4 Quit')
        sel=int(input("\nEnter choice: "))
        if sel==1:
            ping()
        elif sel==2:
            Cloudflare()
        elif sel==3:
            traceroute()
        elif sel==4:
            q()
        else:
            print('That is not a valid choice!!!')
            mainMenu()




mainMenu()
