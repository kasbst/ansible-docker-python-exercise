#!/usr/bin/python

import os.path
import getopt, sys

from scanengine import ScanEngine

def usage():
    print ("""
SCRIPT: {script}
USAGE: {script} <params>...
Where params can be the following:
         --target : Supply target to scan. Can be: [subnet, IP Range, single IP, comma-separated IP's, hostname, comma-separated hostnames]
         --port   : Supply port to scan. Can be: [single port, port range, - (dash) for all ports]
         --help   : Print this message

Example:
         --target=192.168.1.120 | 192.168.1.0/24 | 192.168.1.20-180 | "example.com,example1.com"
         --port=22 | 10-1000 | -
""").format(script=sys.argv[0])

try:
    opts, args = getopt.getopt(sys.argv[1:], 't:p:h', ['target=', 'port=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-t', '--target'):
        target = arg
    elif opt in ('-p', '--port'):
        port = arg
    else:
        usage()
        sys.exit(2)

try: target and port
except NameError:
   print ("You must provide target and port to be scanned!")
   usage()
   sys.exit(2)

def main():
    if os.getuid() != 0:
       print ("Nmap scan failed: You requested a scan type which requires root privileges.")
       sys.exit(2)

    scanner = ScanEngine(target, port)
    scanner.process()

if __name__ == "__main__":
    main()

