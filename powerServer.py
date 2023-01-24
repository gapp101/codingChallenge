
# AT COMMAND LINE:
# flask --app powerServer run
# results in: server on http://127.0.0.1:5000

# flask --app powerServer run -h 0.0.0.0 -p 8888 
# results in: the server running on "all" ip addresses:  http://127.0.0.1:8888
# and another what looks like a local ip addr: http://143.210.xxx.xxx:8888 at L Uni
# both/all use port# 8888

# AT COMMAND LINE, to send a POST command with json Data:
#curl -X POST -H "Content-Type: application/json" -d jsonString  
#    http://localhost:5000/productionplan
# Fix above: depends on IP and port#

from flask import Flask, jsonify, request
import json
import logging

app = Flask(__name__)

# Set up logging file and level.
logging.basicConfig(filename='powerServer.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Testing Endpoints
@app.route("/")
def hello_world() :
  return "Hello World! Goodbye."
  
@app.route('/find/<int:find_id>')
def find(find_id) :
  return f"Find with id= {find_id}, one day I might get to it"


# ERROR HANDLING
from flask import json
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_exception(e):
  print("ERROR, returning")
  # start with the correct headers and status code from the error
  response = e.get_response()
  # replace the body with JSON
  response.data = json.dumps({
    "code": e.code,
    "name": e.name,
    "description": e.description,
  })
  response.content_type = "application/json"
  return response
# END OF ERROR HANDLING


# Local function: main "algorithm": extremely preliminary. pMin pretty much ignored
def generatePowerDistn(powerplants, load) :
  powerDistn=[]
    
  # Greedy Algorithm: gorge on cheapest power
  # The list of powerplants is sorted by ascending "cost"
  for plant in powerplants :
    availPower = plant["pmaxElec"]

    if (load < 0.1) : 
      assignPower = 0;
      
    elif (availPower > 0.0) :
      assignPower = min(load, availPower)
      # !!! pminElec may be greater than assignedPower. Use pminElec or assignedPower? need clarification.
      # powerDistn.append({"name":plant["name"], "p":assignPower})
      load -= assignPower     
  
    else :
      assignPower = 0;
      
    powerDistn.append({"name":plant["name"], "p":assignPower})
 
      # !!! pminElec is not used in decision-making. 
      # !!! A more expensive plant with a lower pminElec could be cheaper. Next release.
      
  return powerDistn

 
# The Production-plan endpoint.
@app.route('/productionplan', methods=['POST'])
def productionplan():
    payload = request.get_json()
    print("POST productionplan recieved, processing payLoad ...", end='')
    
    # initial dictionary access
    load =        payload["load"]         # integer, MWh
    fuels =       payload["fuels"]        # dictionary
    powerplants = payload["powerplants"]  # list of dictionaries

    # 1st pass through plants: add dictionary entries
    for plant in powerplants :
      plant["pminElec"] = plant["pmin"]
      plant["pmaxElec"] = plant["pmax"]

      # make adjustments for each fuel type
      if (plant["type"] == "windturbine") :
        # WIND: incorporate availability factor, null cost
        plant["pminElec"] = round(plant["pminElec"] * float(fuels["wind(%)"])/100.0, 1)
        plant["pmaxElec"] = round(plant["pmaxElec"] * float(fuels["wind(%)"])/100.0, 1)    
        plant["costMWh"] = 0.0     # assumed, not given in data
        # !!! there is an efficiency field, safe to assume always 100%?, probably not
        # !!! but, there is no fuel, so efficiency has no effect on fuel=>electricity conversion
    
      # For other fules, incorporate efficiency into cost per MWh
      elif (plant["type"] == "gasfired") :
        plant["costMWh"] = fuels["gas(euro/MWh)"]/float(plant["efficiency"])
        # add the CO2 cost:
        # Taken into account that a gas-fired powerplant also emits CO2, ... 
        # ... For this challenge, ... each MWh generated creates 0.3 ton of CO2.
        plant["costMWh"] += fuels["co2(euro/ton)"]*0.3 
        
      elif (plant["type"] == "turbojet") :
        plant["costMWh"] = fuels["kerosine(euro/MWh)"]/float(plant["efficiency"])

    # sort out pMin, pMax order
    # describe how to minimize pMin penaltiy when power needed < pMin.
    powerplants.sort(key=lambda x: (x['costMWh'], x['pmaxElec'], x['pminElec']))

    returnDistribution = generatePowerDistn(powerplants, load)    
    
    # PYTHON => JSON
    returnDataJson = json.dumps(returnDistribution)    
    print(" OK, returning.")
    return returnDataJson  

  
      
      