#!/usr/bin/python2.7
#coding: utf-8

import os
import glob
import logging
import socket
from stompy.simple import Client

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y - %H:%M:%S] -',level=logging.INFO)

def Campaigns():
    os.system("mysql -uUSER -pPASS -hoas.mysql.internal.com -A rmlaPrimary -A -e \"select count(Id) from Campaign where Status='L';\" > /tmp/.live_campaigns_counter.offset")
    try:
        result=open('/tmp/.live_campaigns_counter.offset', 'rb')
        lines = result.readlines()
        campaigns = lines[1]
    except IOError, msg:
        pass
    return campaigns



def PostToSCE(livecampaigns):
    logging.info ('Number of live Campaigns: %s' % livecampaigns) 
    stomp = Client(host='activemq.dashboard.internaldomain.com')
    stomp.connect()
    body="{'host' : '%s', 'campaigns' : %s}" %(socket.gethostname(),livecampaigns)
    stomp.put(body,"/queue/events",conf={'eventtype' : 'banner_live_camp'})
    stomp.disconnect()

livecamp=Campaigns()
PostToSCE(livecamp)
