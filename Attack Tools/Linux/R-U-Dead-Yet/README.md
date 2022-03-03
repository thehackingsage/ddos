This is the README file for:
R-U-Dead-Yet version 2.2

New Features In This Version:
-----------------------------

1) Handles TCP ports other than 80 using the :PORT parameter in the URL

R-U-Dead-Yet is run in one of two modes:

1) Interactive menu mode
2) Unattended configuration-based execution

In order to run using the first mode, run as following:

r-u-dead-yet.py <URL>

whereas URL is the FQDN link leading to a web page containing a web form to attack. 
r-u-dead-yet will take care of the rest of the procedure allowing the user to pick:
1) Form to attack
2) Form field to use
3) How many concurrent connections
4) Whether use a SOCKS proxy such as Tor

In the unattended mode, you will need to place a file called:

rudeadyet.conf

in the same directory as the code (BeautifulSoup.py is also required).
The file should look like this:

[parameters]

URL: http://www.victim.com/path-to-post-url.php
number_of_connections: 500
attack_parameter: login

proxy_addr: ""

proxy_port: 0

Whereas:
--------
URL = POST URL
number_of_connections = concurrent processes to execute
attack_parameter = POST parameter to fuzz
proxy_addr = IP of the SOCKS4 proxy to use (leave as empty string if no proxy required)
proxy_port = TCP port on which the SOCKS4 proxy is listening (leave as 0 if no proxy required)

TODO
----

- Add custom headers and POST parameters needed
