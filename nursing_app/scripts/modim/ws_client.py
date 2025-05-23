#!/usr/bin/env python

# Example of use
# export MODIM_IP=<modim server IP>
# python
# >>> from ws_client import *
# >>> q = ModimWSClient()
# >>> q.cconnect()
# >>> q.csend("im.execute('ciao')")
# >>> q.csend("im.robot.say('ciao')")


from __future__ import print_function
import sys
import os
import socket
import importlib
import re
import argparse
import time
import inspect
import textwrap
import csv

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"


def setServerAddr(ip, port):
    print("%sDEPRECATED. Use ModimWSClient.setCmdServerAddr.%s" %(RED,RESET))
    


class ModimWSClient:

    def __init__(self):
        ip = os.getenv('MODIM_IP')
        if (ip==None):
            ip = os.getenv('PEPPER_IP')
        if (ip==None):
            ip = '127.0.0.1'
        self.server_ip = ip
        self.server_port = 9101
        self.demo_ip = ''
        self.demo_port = 0
        self.demo_path = ''
        self.csock = None
        self.code = ""
        self.BUFFER_SIZE = 200
        self.connected = False

    def setCmdServerAddr(self, ip, port):
        self.server_ip = ip
        self.server_port = port

    def setCmdServerAddr(self, ip):
        self.server_ip = ip

    def setDemoServerAddr(self, ip, port):
        self.demo_ip = ip
        self.demo_port = port


    def setDemoPath(self, path):
        self.demo_path = path


    def setDemoPathAuto(self, filename):
        dfile = os.path.dirname(os.path.realpath(filename))
        l = dfile.rfind('/')
        dd = dfile[0:l]
        print("setDemoPathAuto ", dd)
        self.setDemoPath(dd)


    def cconnect(self):
        if self.csock == None: 
            print ("ModimWSClient:: connecting to %s:%d ..." %(self.server_ip, self.server_port))
            self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.csock.connect((self.server_ip,self.server_port))
                print ("ModimWSClient:: connected to %s:%d" %(self.server_ip, self.server_port))
                self.connected = True
            except Exception as e:
                print("Connection error to %s:%d" %(self.server_ip,self.server_port))
                print(e)
                self.csock = None


    def csendfile(self, program):
        if self.connected:
            f = open(program,'r') 
            data = f.read() 
            f.close()
            self.csend(data)


    def csend_noblock(self, data):
        if self.csock==None:
            self.cconnect()
        if self.connected:
            print ("ModimWSClient:: sending data ...")
            self.csock.send(data+"\n###ooo###\n\n")
            print ("WS client:: data sent")


    def csend(self, data):
        if self.csock==None:
            self.cconnect()
        if self.connected:
            print ("ModimWSClient:: sending data ...")
            self.csock.send(data+"\n###ooo###\n\n")
            print ("WS client:: data sent")

        time.sleep(0.5)

        print ("WS client:: waiting for reply ...")
        try:
            rdata = self.csock.recv(self.BUFFER_SIZE)
            rdata = rdata.strip()
        except KeyboardInterrupt:
            rdata = "user quit"
        except socket.error:
            rdata = "socket error"
        print("Reply: (%s)"%rdata)
        return rdata

    def cclose(self):
        if self.connected:
            self.csock.close()
            print("Closed connection")
            self.csock = None
            self.connected = False

    def run_interaction(self, interaction):
        try:
            lcode = inspect.getsourcelines(interaction)
        except Exception as e:
            print("ERROR: "+str(e))
            return
        locode = ""
        if (self.demo_path != ''):
            self.csend("im.setDemoPath('%s')\n" %(self.demo_path))
        if (self.demo_ip!=''):
            self.csend("im.setDemoServer('%s', %d)\n" %(self.demo_ip, self.demo_port))
        for l in lcode[0][1:]:
            locode += l
        locode = textwrap.dedent(locode)
        self.code = locode
        print(self.code)
        self.cconnect()
        self.csend(self.code)

    def store_interaction(self, interaction):
        lcode = inspect.getsourcelines(interaction)    
        for l in lcode[0][0:]:
            self.code += l
        self.code += '\n'

    def setGlobalVar(self, var, value):
        self.code += '%s = %r\n' %(var,value)


def run_interaction(interaction):
    print("%sDEPRECATED. Use ModimWSClient.run_interaction.%s" %(RED,RESET))
    mws = ModimWSClient()
    mws.run_interaction(interaction)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serverip", type=str, default='127.0.0.1',
                        help="Server IP address.")
    parser.add_argument("--serverport", type=int, default=9100,
                        help="Server port")
    parser.add_argument("--program", type=str, default="default.py",
                        help="Program file to send")

    args = parser.parse_args()
    server_ip = args.serverip
    server_port = args.serverport 
    program = args.program

    #Starting application
    #start_client(server_ip,server_port,program)
    modim.csendprogram(program)


if __name__ == "__main__":
    main()


