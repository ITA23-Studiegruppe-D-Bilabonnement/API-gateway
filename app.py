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

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY',"1234")
customer_microservice_url = os.getenv('CUSTOMER_MICROSERVICE', "https://customer-microservice-b4dsccfkbffjh5cv.northeurope-01.azurewebsites.net")
cars_microservice_url = os.getenv('CARS_MICROSERVICE', "https://cars-microservice-a7g2hqakb2cjffef.northeurope-01.azurewebsites.net")
subscription_microservice_url = os.getenv('SUBSCRIPTION_MICROSERVICE', "https://subscription-microservice-gxbuenczgcd5hfe4.northeurope-01.azurewebsites.net")
damage_report_microservice_url = os.getenv('DAMAGE_REPORT_MICROSERVICE', "https://damagereport-microservice-gpfchac2c4c9hzdc.northeurope-01.azurewebsites.net")
jwt = JWTManager(app)

# Initialize Swagger
init_swagger(app) 

# Documentaion endpoint
@app.route("/", methods=["GET"])
def homepoint():
    
    return jsonify({
        "SERVICE": "API-GATEWAY SERVICE",
        "AVAILABLE ENDPOINTS": [
            {
            "MICROSERVICE": "CUSTOMER-MICROSERVICE",
            "PATH": "/api/customer",
            "URL": f"{customer_microservice_url}",
            "AVAILABLE ENDPOINTS": []
            },
            {
            "MICROSERVICE": "SUBSCRIPTION-MICROSERVICE",
            "PATH": "/api/subscription",
            "URL": f"{subscription_microservice_url}",
            "AVAILABLE ENDPOINTS": []
            },
            {
            "MICROSERVICE": "CARS-MICROSERVICE",
            "PATH": "/api/cars",
            "URL": f"{cars_microservice_url}",
            "AVAILABLE ENDPOINTS": []
            },
            {
            "MICROSERVICE": "DAMAGE-REPORT-MICROSERVICE",
            "PATH": "/api/damage",
            "URL": f"{damage_report_microservice_url}",
            "AVAILABLE ENDPOINTS": []
            }
        ]
    }), 200

# CUSTOMER MICROSERVICE ***********************************************************************

# Handle the customer microservice endpoint
@app.route("/api/customer/<path:route>", methods=["GET","POST","DELETE"])
@swag_from("swagger/api_customer.yaml")
def customer_microservice(route):

    try:
        response = requests.request(
            url=f'{customer_microservice_url}/{route}',
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


#CARS MICROSERVICE *******************************************************************

# Handle the cars microservice
@app.route("/api/cars/<path:route>", methods=["GET","POST","DELETE","PUT"])
@swag_from("swagger/api_cars.yaml")
def cars_microservice(route):

    try:
        response = requests.request(
            url=f'{cars_microservice_url}/{route}',
            method=request.method,
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json(silent=True)
        )
        
        return response.text, response.status_code, response.headers.items()
    
    except Exception as e:
        return jsonify({
            "error": "OOPS! Something went wrong :(",
            "message": f'{e}'
        }), 500

#SUBSCRIPTION MICROSERVICE ************************************************************

#Handle the subscription microservice
@app.route("/api/subscription/<path:route>", methods=["GET","POST","DELETE","PATCH"])
@swag_from("swagger/api_subscription.yaml")
def subscription_microservice(route):

    try:
        response = requests.request(
            url=f'{subscription_microservice_url}/{route}',
            method=request.method,
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json(silent=True)
        )
        
        return response.text, response.status_code, response.headers.items()
    
    except Exception as e:
        return jsonify({
            "error": "OOPS! Something went wrong :(",
            "message": f'{e}'
        }), 500

#DAMAGE REPORT MICROSERVICE ************************************************************

#Handle the damage report microservice
@app.route("/api/damage/<path:route>", methods=["GET","POST","DELETE","PATCH"])
@swag_from("swagger/api_damage_report.yaml")
def damage_report_microservice(route):

    try:
        response = requests.request(
            url=f'{damage_report_microservice_url}/{route}',
            method=request.method,
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json(silent=True)
        )
        
        return response.text, response.status_code, response.headers.items()
    
    except Exception as e:
        return jsonify({
            "error": "OOPS! Something went wrong :(",
            "message": f'{e}'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)