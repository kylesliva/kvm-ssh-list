#!/usr/bin/env python3
import re
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def main():
    arpCache = str(subprocess.check_output(["arp", "-a"]))
    logging.debug(arpCache)
    logging.debug(type(arpCache))
    logging.debug(re.findall("192\.168\.122\.\d{1,3}", arpCache))
    
    opts = re.findall("192\.168\.122\.\d{1,3}", arpCache) 
    
    printOptions(opts)

#checks for KVM IP
def match(ip):
    test = re.compile("192\.168\.122\.\d{1,3}")

    if test.match(ip):
        return True
    return False

def printOptions(opts):
    selectionIndex = -1 
    for num, item in enumerate(opts):
        logging.debug(num)
        print(f"{num}) {item} ")
    selectionIndex = int(input("Please select an option from the above list"))
        


    

if __name__ == '__main__':
    main()
