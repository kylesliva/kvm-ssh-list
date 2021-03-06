#!/usr/bin/env python3
import re
import subprocess
import logging
import socket
import argparse

'''
info goes here
'''


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-v", "--verbose", help="set logging level to INFO", action="store_true")
    parser.add_argument("-d", "--debug", help="set logging level to DEBUG", action="store_true")
    parser.add_argument("-l", "--list", help="print list of guest VMs", action="store_true")
    parser.add_argument("--json", help="print list of guest VMs in JSON format", action="store_true")
    
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s- %(message)s')
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
    # pull out arp cache from shell. is there a better way to use socket for this?
    arpCache = str(subprocess.check_output(["arp", "-a"]))
    logging.debug(arpCache)
    logging.debug(re.findall("192\.168\.122\.\d{1,3}", arpCache))

    # Right now this will match any number up to 999
    # known limitation
    
    opts = re.findall("192\.168\.122\.\d{1,3}", arpCache) 
    
    if not opts:
        logging.error("error: no KVM hosts running on machine")
        return
    if not args.list:
        connect_host(print_options(opts))
    if args.list:
        [print(f"{ip}") for ip in opts]



def print_options(opts):
    hostname = ""
    output = None

    for num, item in enumerate(opts):
        try:
            hostname = f"{socket.gethostbyaddr(item)[0]}"
        except socket.herror:
            logging.info("Warning: cannot resolve KVM guest addresses. Is 192.168.122.1 the primary nameserver?")
            hostname = item
        print(f"{num + 1}) {hostname}")
    selectionIndex = int(input("Please select an option from the above list: ")) - 1
    logging.debug(f"selection index: {selectionIndex}")

    try:
        output = opts[selectionIndex]
    except Exception as e:
        print("please enter a valid list index")
    
    logging.debug(
                f"ip: {output}\n"
                f"hostname: {hostname}"
    )

    return output

#initiates SSH connection to ip
def connect_host(ip):
    if ip is None:
        return
    print(f"\nConnecting to {ip}\n")
    subprocess.run(["ssh", ip])

if __name__ == '__main__':
    main()
