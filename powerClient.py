# powerClient
# execute a POST REST request with a json payload file and display + save the response.
# the response is saved in the file "pcResponse.json"

# Arguments: the (JSON) payload filename and the server IP address
# the payload file argument is not checked at all.
# the IP address is checked for sanity.

# there's a 20 sec timeout on the API invoke command.
 
import sys
from sys import argv

import getopt, os
import os.path

# program usage statement
usage = "Usage: " + os.path.basename((sys.argv[0])) + " payload.json IP-address"

# process options: NONE
try:
	myopts, ArgsRemaining = getopt.gnu_getopt(sys.argv[1:], "")
except getopt.GetoptError as err:
  print (str(err))
  print (usage)
  sys.exit(2);
 

# Check whether input filename is given and that the file exists
# !!! Check subscript is: .json
numArgs = len(ArgsRemaining)
filename = (ArgsRemaining[0] if numArgs > 0 else "")

if not( numArgs > 1 and os.path.isfile(filename)) :
	print (usage)
	sys.exit(2)

# Check 2nd parameter is a valid IP address
serverIP = ArgsRemaining[1]
import ipaddress
try:
  ipaddress.ip_address(serverIP)
except: 
  print (usage)
  sys.exit(3)


import json
import requests

# the keys should be defined in 1 place and used as variables.

with open(filename, "r") as jsFile :
    payload = json.load(jsFile)

# FIRST SEND THE PAYLOAD TO THE SERVER
# url = 'http://localhost:5000/productionplan'
# url = 'http://192.168.1.180:8888/productionplan'
url     = f"http://{serverIP}:8888/productionplan"
# a dictionary with 1 item-value pair
header = {'Content-Type' : 'application/json'}
# And this JSON-ifies the data, PYTHON=>JSON
payloadJson = json.dumps(payload)

try:
  res = requests.post(url, data=payloadJson, headers=header, timeout=20)
except requests.Timeout:
    print (f"no reponse from: {url}")    
    sys.exit(3)
except requests.ConnectionError:
    print (f"connection error with: {url}")    
    sys.exit(3)

schedule = res.json()

# Python => JSON
scheduleJson = json.dumps(schedule)
print("\nRETURNED DIST'N: ", scheduleJson,"\n")

# Try to write the response to a local file:
try:
  respFile = open("pcResponse.json", 'w')
  json.dump(schedule, respFile, ensure_ascii=False, indent = 2)
  respFile.close()  
except :
	print ("Could not access file pcResponse.json")

jsFile.close()






