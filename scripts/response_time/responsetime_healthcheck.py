#!/opt/generic/python27/bin/python
#coding: utf-8

import os
import glob
import logging
import urllib
import time
import socket
from stompy.simple import Client

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y - %H:%M:%S] -',level=logging.INFO)


def PostToSCE(responsetime):
    logging.info ('The Response Timei was: %s' % responsetime) 
    stomp = Client(host='activemq.mydomain.com')
    stomp.connect()
    body="{'host' : '%s', 'responsetime' : %s}" %(socket.gethostname(),responsetime)
    stomp.put(body,"/queue/events",conf={'eventtype' : 'banner_responsetime'})
    stomp.disconnect()


def Download(server):
    healthcheck = "http://" + str(server) + "/healthcheck"
    start = int(round(time.time() * 1000))
    content = urllib.urlopen(healthcheck)
    end = int(round(time.time() * 1000))
    page = content.read()
    if "Working" in page:
        totaltime = (end - start)
        content.close()
    else:
        print ('Healthcheck failed. I will not send data')
        content.close()
        exit(0)
    return totaltime


responsetime = Download(socket.gethostname())
PostToSCE(responsetime)
