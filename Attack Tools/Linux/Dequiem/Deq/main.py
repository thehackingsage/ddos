#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#+--------------------+
#|Creators :          |
#|-Drarqua GHS Storm  |
#|-Rebel Yell         |
#+--------------------+

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
curdir = os.getcwd()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mode = raw_input( "Choose the mode you want this program to use:" )
if mode == "hack":
    os.system(curdir+"\Deq\hack.py")
elif mode == "help":
    print ( "+-----------+")
    print ( "|Modes are: |" )
    print ( "|-hack      |" )
    print ( "|-help      |" )
    print ( "|-ddos      |" )
    print ( "|-findip    |" )
    print ( "|-portscan  |" )
    print ( "+-----------+")
    print ( "For further help about a command type 'help <command>'")
    print ( "For example: help -ddos")
    fhelp = raw_input("Do you need more help ?")
    if fhelp in "n No NO N no".split():
        restart_program()
    else:
        os.system(curdir+"\Deq\help.py")
elif mode == "findip":
    os.system(curdir+"\Deq\findip.py")
elif mode in "DDoS ddos -ddos -DDoS".split():
    os.system(curdir+"\Deq\ddos.py")
elif mode == "portscan":
    os.system(curdir+"\Deq\portscan.py")
else:
    print ( "This mode doesn't exist" )
    print ( "Restart the Dequiem please" )
    if __name__ == "__main__":
        answer = raw_input("Do you want to restart Dequiem ?")
        if answer.strip() in "y Y yes Yes YES".split():
            print ( "Thank you for using Dequiem 2.0 ") 
            restart_program()
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
