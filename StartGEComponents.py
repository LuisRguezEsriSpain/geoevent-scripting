# -*- coding: utf-8 -*-

import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import requests, json
import time

def SetupLog(fichero):
	fileh = RotatingFileHandler(fichero,mode='a',maxBytes=5*1024*1024,backupCount=2, encoding=None, delay=0)
	logFormatter = logging.Formatter('')
	log = logging.getLogger()  # root logger
	for hdlr in log.handlers[:]:  # remove all old handlers
		log.removeHandler(hdlr)
	log.addHandler(fileh)

def GetLogMessage(msg):
	return datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S') + '. ' + msg
	
def GenerateToken(geoeventServer, username, password):
	tokenURL = 'https://{0}:6443/arcgis/tokens/'.format(geoeventServer)
	params = {'f': 'pjson', 'username': username, 'password': password, 'referer': 'https://{0}:6143/geoevent/admin'.format(geoeventServer)}
	r = requests.post(tokenURL, data = params, verify=False)
	response = json.loads(r.content)
	token = response['token']
	
	return token

def StartGEComponent(geoeventServer, component, geoeventComponent, token):
	response = None
	try:
		header = {'Content-Type':'application/json', 'GeoEventAuthorization':token}
		inputURL = 'https://{0}:6143/geoevent/admin/{1}/{2}/start'.format(geoeventServer, component, geoeventComponent)

		r = requests.get(inputURL, headers=header,  verify=False)
		response = json.loads(r.content)
	except Exception:
		line, filename, synerror = trace()
		logging.info(GetLogMessage("error on line: " % line))
		logging.info(GetLogMessage("error in file name: %s" % filename))
		logging.info(GetLogMessage("with error message: %s" % synerror))
		
	return response

# Disable warnings
requests.packages.urllib3.disable_warnings()

# Variables
geoeventServer = "" # server_fqdn name (e.g. myserver.domain.com)
username = "" # AGS site username
password = "" # AGS user password

# Each element of 'inputs', 'outputs' and 'services' lists can be obtained from 'ExtractGEComponents.py' script output.
inputs = [
	{"label": "input-1", "name": "975a7165-647e-4f9a-868e-456b481472d5"},
	{"label": "input-N", "name": "a223be0b-6bb4-415a-8038-1613e6edb69a"}
]

outputs = [
	{"label": "output-1", "name": "c00a8a92-74f5-4ca0-83c6-e4aedf194290"},
	{"label": "output-N", "name": "4031ae25-898a-4201-8b64-13c5bbf97c32"}
]

services = [
	{"label": "service1", "name": "4fd7c549-3abf-4cc6-8269-21ce1ead5d6c"},
	{"label": "serviceN", "name": "44b2e599-5217-4d3c-8df1-8036395c74cd"}
]

ficheroLog = r"C:\arcgisserver\StartGeoEventComponents\StartGeoEventComponents.log"
logging.basicConfig(filename=ficheroLog, level=logging.INFO)
SetupLog(ficheroLog)
logging.info(GetLogMessage("\n***** Beginning Starting"))

# Generate Token
token = GenerateToken(geoeventServer, username, password)
#print("Token: " + token)

# Start Services
logging.info(GetLogMessage('Starting services'))
for geoeventService in services:
	logging.info(GetLogMessage('\tservice {0}'.format(geoeventService["label"])))
	response = StartGEComponent(geoeventServer, "geoeventservice", geoeventService["name"], token)
	#print("Response start: " + json.dumps(response))
	time.sleep(4)

# Start Outputs
logging.info(GetLogMessage('Starting outputs'))
for geoeventOutput in outputs:
	logging.info(GetLogMessage('\toutput {0}'.format(geoeventOutput["label"])))
	response = StartGEComponent(geoeventServer, "output", geoeventOutput["name"], token)
	#print("Response start: " + json.dumps(response))
	time.sleep(4)

# Start Inputs
logging.info(GetLogMessage('Starting inputs'))
for geoeventInput in inputs:
	logging.info(GetLogMessage('\tinput {0}'.format(geoeventInput["label"])))
	response = StartGEComponent(geoeventServer, "input", geoeventInput["name"], token)
	#print("Response start: " + json.dumps(response))
	time.sleep(4)

logging.info(GetLogMessage("***** End Starting"))
