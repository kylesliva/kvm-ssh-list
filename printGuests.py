#!/usr/bin/env python3
import re
import subprocess
import logging
import socket
import argparse

'''
#todo
* add argparse 
    * for setting log level
* opt selector 
* exception handling
* more verbose logging
* convert main method to a strict flow control method
'''

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def main():
    # pull out arp cache from shell. is there a better way to use socket for this?
    arpCache = str(subprocess.check_output(["arp", "-a"]))
    logging.debug(arpCache)
    logging.debug(re.findall("192\.168\.122\.\d{1,3}", arpCache))
    
    opts = re.findall("192\.168\.122\.\d{1,3}", arpCache) 
    
    connectHost(printOptions(opts))



def printOptions(opts):
    selectionIndex = -1 

    for num, item in enumerate(opts):
        print(f"{num}) {socket.gethostbyaddr(item)[0]} ")
    selectionIndex = int(input("Please select an option from the above list: "))
    logging.debug(f"selection index: {selectionIndex}")

    try:
        output = opts[selectionIndex]
    except Exception as e:
        print("please enter a valid list index")
    
    logging.debug(
                f"ip: {output}\n"
                f"hostname: {socket.gethostbyaddr(output)[0]}"
    )

    return output

#initiates SSH connection to ip
def connectHost(ip):
    subprocess.run(["ssh", ip])

if __name__ == '__main__':
    main()
