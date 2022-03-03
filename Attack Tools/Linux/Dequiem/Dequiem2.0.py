#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#+--------------------+
#|Creators :          |
#|-Drarqua GHS Storm  |
#|-Rebel Yell         |
#+--------------------+

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import webbrowser
import os
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

music = raw_input( "Do you want to hear the featured music of the week ?" )
if music in "y Y yes Yes YES".split():
    webbrowser.open_new("http://www.youtube.com/watch?v=kmBnvajSfWU")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
print ( "Dequiem Tool")      
print ( "Version 2.0" )
print ( "Currentrly Working:")
print ( "+-----------+")
print ( "|ddos       |")
print ( "|findip     |")
print ( "|portscan   |")
print ( "|help       |")
print ( "+-----------+")
curdir = os.getcwd()
os.system(curdir+"\Deq\main.py")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
