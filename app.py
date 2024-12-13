from flask import Flask, jsonify, request
import requests
import os
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flasgger import swag_from
from swagger.swagger_config import init_swagger

app = Flask(__name__)

#Load the enviroment variables
load_dotenv()

#JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY',"1234")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 
jwt = JWTManager(app)

# Microservice url env variables
customer_microservice_url = os.getenv('CUSTOMER_MICROSERVICE', "https://customer-microservice-b4dsccfkbffjh5cv.northeurope-01.azurewebsites.net")
cars_microservice_url = os.getenv('CARS_MICROSERVICE', "https://cars-microservice-a7g2hqakb2cjffef.northeurope-01.azurewebsites.net")
subscription_microservice_url = os.getenv('SUBSCRIPTION_MICROSERVICE', "https://subscription-microservice-gxbuenczgcd5hfe4.northeurope-01.azurewebsites.net")
damage_report_microservice_url = os.getenv('DAMAGE_REPORT_MICROSERVICE', "https://damagereport-microservice-gpfchac2c4c9hzdc.northeurope-01.azurewebsites.net")

#Create list of microservices
microservice_list = {
    "customer": customer_microservice_url,
    "cars": cars_microservice_url,
    "subscription": subscription_microservice_url,
    "damage": damage_report_microservice_url
}

# Initialize Swagger
init_swagger(app) 

# Documentaion endpoint
@app.route("/", methods=["GET"])
def homepoint():
    
    #Dynamically add the available endpoints
    available_endpoints = []
    for service in microservice_list:
        #Get the documentation form "/" endpoint
        response = requests.get(microservice_list[service])

        #Create the list object
        list_of_endpoints = response.json()

        #Append it to the list
        available_endpoints.append(list_of_endpoints)

    return jsonify({
            "SERVICE": "API-GATEWAY SERVICE",
            "AVAILABLE ENDPOINTS": available_endpoints
        })

# Dynamic gateway:
@app.route("/<string:service>/<path:route>", methods=["GET","POST","PUT","PATCH","DELETE"])
@swag_from("swagger/gateway.yaml")
def gateway(service, route):

    #Check to see the provided service exists
    if service not in microservice_list:
        return jsonify({
            "error": "OOPS! Something went wrong :(",
            "message": "Couldnt find the microservice, please check your spelling!"
        }),404
    
    #Send request to the provided microservice
    try:
        response = requests.request(
            url=f"{microservice_list[service]}/{route}",
            method=request.method,
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json(silent=True),
            allow_redirects=False
        )

        return response.text, response.status_code, response.headers.items()
    
    except Exception as e:
        return jsonify({
            "error": "OOPS! Something went wrong :(",
            "message": f'{e}'
        }), 500
        
if __name__ == "__main__":
    app.run(debug=True)