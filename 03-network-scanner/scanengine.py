"""
Simple module with ability to execute nmap scan together with
parsing and printing its output to STDOUT and JSON files placed in /tmp/* directory

It also compares the subsequent scans for changes.
"""

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from time import sleep
import json
import os.path
import sys

class ScanEngine(object):
      """
      A class proving methods for executing and parsing nmap scan
      """
      def __init__(self, target, port):
          self._target = target
          self._port   = port

      """
      Name: run_scan
      Executes nmap scan with provided parameters (target and port)
      Return: NmapProcess object
      """
      def _run_scan(self):
          nmap_proc = NmapProcess(targets=self._target, options="-Pn -sT -sU -p "+self._port)
          nmap_proc.run_background()
          while nmap_proc.is_running():
              print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmap_proc.etc,
                                                             nmap_proc.progress))
              sleep(2)

          if nmap_proc.rc != 0:
             print("Nmap scan failed: {0}".format(nmap_proc.stderr))
             sys.exit(2)
          else:
             return nmap_proc

      """
      Name: parse_data
      Parse nmap scan output
      Return: NmapObject (NmapHost, NmapService or NmapReport)
      """
      def _parse_data(self, nmap_proc):
          try:
             parsed = NmapParser.parse(nmap_proc.stdout)
          except NmapParserException as e:
             print("Exception raised while parsing scan: {0}".format(e.msg))

          return parsed

      
      """
      Name: print_header_and_body
      Helper method for printing scan results
      """ 
      def _print_header_and_body(self, host_address, pserv):
          print("\n*target - {0}: Full Scan Results:*".format(host_address))
          print("TARGET              PORT         STATE         SERVICE")
          print(pserv)

      """
      Name: print_scan
      Print the parsed scan report and compare subsequent scans for
      changes.
      """
      def _print_scan(self, nmap_report):
          for host in nmap_report.hosts:
              new_data = {host.address: []}
              pserv = "";

              file_path = "/tmp/"+host.address+".json"

              for serv in host.services:
                  new_data[host.address].append(str(serv.port)+"/"+serv.protocol)

                  pserv += "{0:16s} {1:>5s}/{2:8s}  {3:12s}  {4}\n".format(
                       str(host.address),
                       str(serv.port),
                       serv.protocol,
                       serv.state,
                       serv.service)

              if os.path.isfile(file_path):
                 old_data = self._load_data(file_path)
                 if self._compare_data(new_data, old_data, host.address):
                    print("*Target - "+host.address+" : No new records found in the last scan.*")
                 else:
                    self._print_header_and_body(host.address, pserv)
                    self._save_data(file_path, new_data)
              else:
                 self._print_header_and_body(host.address, pserv)
                 self._save_data(file_path, new_data)

          print("\n" + nmap_report.summary)

      """
      Name: save_data
      Save scan results to JSON format to be able later to
      compare subsequent scans for changes
      """
      def _save_data(self, file_name, data):
          with open(file_name, 'w') as fp:
               json.dump(data, fp, sort_keys=True, indent=4)

      """
      Name: load_data
      Load old scan results from JSON format to be able to
      compare subsequent scans for changes
      """ 
      def _load_data(self, file_name):
          if os.path.isfile(file_name):
             with open(file_name, 'r') as fp:
                  data = json.load(fp)

             return data
          else:
             return

      """
      Name: compare_data
      Compare subsequent scans for changes
      """
      def _compare_data(self, new_data, old_data, address):
          old_list = [str(s) for s in old_data[address]]
          new_list = new_data[address]
          
          if sorted(old_list) == sorted(new_list):
             return True
          else:
             return False
 
      """
      Name: process
      Public method for scan execution
      """
      def process(self):
          data = self._run_scan()
          self._print_scan(self._parse_data(data))


