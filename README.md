# codingChallenge
GEMS Coding Challenge: Powerplant Scheduling

This document describes the Python-based solution to the powerplant-coding-challenge. 

4 files are included in this solution/project: the powerServer python file, an optional powerClient python file, requirements.txt and this README file. 

Assumptions
===========
1. CO2 emissions only occur for the fuel: gas. And these emissions translate into €-cost according to the parameters given. This €-cost (emissions) has the same “merit order” weighting as fuel cost.

2. There is no “cost” associated with the p-max parameter of a plant. Two plants with equivalent parameters except for the p-max parameter have the same “merit-order”. For equivalent plants, the algorithm always tries to use the plant with the lower p-max value.

3. The p-min parameter is not considered fully and this is a short-coming in the algorithm. To be implemented in next release!


Requirements
============
Python 3 installed with the following Python packages also installed:
1. pip &emsp;&emsp;&emsp;&emsp;&emsp;Python3 -m pip install
2. requests &emsp;&emsp;&emsp;via pip
3. Flask&emsp; &emsp;&emsp;&emsp;via pip
4. Werkzeug &emsp;&emsp;(this may be included in the Flask installation)

Note: the file “requirements.txt” was generated from my computing environment (Macintosh, terminal) using the command

>  pip freeze > requirements.txt

After the standard Python 3 installation and installing requests and Flask, the other packages in the requirements.txt listing, should be pulled in.

There are no build operations required.


powerServer.py
==============
This file contains the Python code for implementing the REST API.

To run the power-server, enter the following command at the shell prompt:

>  flask --app powerServer run  -h 0.0.0.0  -p 8888

This runs the powerServer on “all” IP addresses. Seems dodgy to me, but it certainly has the server accept requests on 2 IP addresses: 127.0.0.1 and another local IP that is determined by your network. The second IP can be seen in the first few lines in the log file entries for a particular execution. Not particularly "friendly".

For all IP addresses, the server listens on port 8888.

3 APIs are accessible (“exposed”):
/						Returns the proverbial “Hello World” string.		
/find/ID					ID is an integer. Returns a string containing the ID.
/productionplan/payload	payload is a JSON specification as defined.
						a JSON power distribution list is returned on successful execution.

The first two APIs are GET APIs (testing purposes) and the third is a POST API.

The above APIs can be accessed by a client in the usual REST manner. That is, these APIs can be accessed via HTTP using the URL field of a standard browser. The APIs can also be accessed from the command line using a curl command.


powerClient.py
==============
For convenience a Python-based script is included allowing JSON payload files to be sent to the server as part of a productionplan API call.

With JSON payload files in the same directory as the powerClient program, invoke the productionplan API on a currently running powerServer by executing the following command at the shell prompt:

>  python3  powerClient.py  payload.json  127.0.0.1

powerClient will invoke the productionplan API, sending the payload file to the server and display the returned power station distribution to the screen. It will also write this distribution as a JSON string to the file “pcResponse.json” saving the file in the same directory as powerClient.py.

Note: every execution of powerClient will overwrite the contents of pcResponse.json with the latest returned powerServer response. Previous execution responses will be lost.

powerClient will timeout after 20 seconds if no response is received from powerServer.

If the IP address 127.0.0.1 does not work, then try the 2nd IP address written to the log file at startup (see below).


Logging
=======
At start-up, powerServer opens the file (creates if it does not exist) “powerServer.log”. All API requests are logged here including failed requests. Amoungst the first few log entries of each execution is a listing of the 2 IP addresses the server is using. One being: 127.0.0.1 and the other an IP address determined by your network. One of these IPs is necessary to make REST request when calling the API.

If a problem occurs when the powerServer is processing an API request, then in addition to making a log entry, the server returns a JSON string (Python dictionary) containing the error attributes. 



