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

shelp = raw_input("In which command you need help ?")
if shelp == "help -ddos":
    print ("+---------------------------------------------+")
    print ("|This is ddos mode , in which you can send    |")
    print ("|packets to a website in order to take it down|")
    print ("+---------------------------------------------+")
    if __name__ == "__main__":
        answer = raw_input("Do you want to find help for more commands?")
        if answer.strip() in "y Y yes Yes YES".split():
            restart_program()
        else:
            os.system(curdir+"\Deq\main.py")
elif shelp == "help -findip":
    print ("+----------------------------------------+")
    print ("|In this mode you can find a website's ip|")
    print ("|in oreder to make another attacks.      |")
    print ("+----------------------------------------+")
    if __name__ == "__main__":
        answer = raw_input("Do you want to find help for more commands?")
        if answer.strip() in "y Y yes Yes YES".split():
            restart_program()
        else:
            os.system(curdir+"\Deq\main.py")
elif shelp == "help -hack":
    print ("+---------------------------------------------+")
    print ("|Hack mode currently doesn't work ,but we are |")
    print ("|working on it                                |")
    print ("|It will probably be a SQLInjection tool      |")
    print ("+---------------------------------------------+")
    if __name__ == "__main__":
        answer = raw_input("Do you want to find help for more commands?")
        if answer.strip() in "y Y yes Yes YES".split():
            restart_program()
        else:
            os.system(curdir+"\Deq\main.py")
elif shelp =="help -help":
    print ("+---------------------------------------------+")
    print ("|Help is a mode where you can find information|")
    print ("|about other modes .                          |")
    print ("+---------------------------------------------+")
    if __name__ == "__main__":
        answer = raw_input("Do you want to find help for more commands?")
        if answer.strip() in "y Y yes Yes YES".split():
            restart_program()
        else:
            os.system(curdir+"\Deq\main.py")
elif shelp =="help -portscan":
    print ("+---------------------------------------------+")
    print ("|Port Scan is about find open ports for a     |")
    print ("|a successfull ddos attack or something else  |")
    print ("+---------------------------------------------+")
    if __name__ == "__main__":
        answer = raw_input("Do you want to find help for more commands?")
        if answer.strip() in "y Y yes Yes YES".split():
            restart_program()
        else:
            os.system(curdir+"\Deq\main.py")
else:
    print("We cant find help about" + shelp )
    if __name__ == "__main__":
        answer = raw_input("Do you want to find help for more commands?")
        if answer.strip() in "y Y yes Yes YES".split():
            restart_program()
        else:
            os.system(curdir+"\Deq\main.py")
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
