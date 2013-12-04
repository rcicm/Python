#!/opt/generic/python27/bin/python
#coding: utf-8

import os
import glob
import logging
import socket
from stompy.simple import Client

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y - %H:%M:%S] -',level=logging.INFO)

DIR = "/[PATH]/OpenAd/Logs/oay/out/"
OFFSET = "/tmp/.line_counter.offset"

def mtime(file):
    return os.stat(os.path.join(DIR,file)).st_mtime

def get_last_file():
    last_file="nenhum"
    try:
        f=open(OFFSET,'r')
        last_file=f.read().rstrip()
    except IOError, msg:
       pass 
    return last_file

def get_current_file():
    return sorted(glob.glob(DIR + "adstream.log.*[0-9][0-9]"), key=mtime, reverse=True)[0]

def PostToSCE(lines):
    logging.info ('Number of impressions: %s' % lines) 
    stomp = Client(host='activemq.dashboard.myinternaldomain.com')
    stomp.connect()
    body="{'host' : '%s', 'lines' : %d}" %(socket.gethostname(),lines)
    stomp.put(body,"/queue/events",conf={'eventtype' : 'banner_line_count'})
    stomp.disconnect()

def count_lines(filename):
    lines = 0
    for line in open(filename):
        lines += 1
    return lines

def update_offset(filename):
    f = open (OFFSET,'w') 
    f.write (filename)
    f.close()

lastfile=get_last_file()
currentfile = get_current_file()

logging.info ('Last file processed: %s'  % lastfile )
logging.info ('next file on dir:    ' + currentfile)

if currentfile == lastfile:
    logging.info ('Files are the same. No sending data')
    exit(0)

line_numbers=count_lines(currentfile)
PostToSCE(line_numbers)
update_offset(currentfile)
