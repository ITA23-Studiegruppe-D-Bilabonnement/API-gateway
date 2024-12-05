from flask import Flask, jsonify, request
import requests
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from flasgger import swag_from

app = Flask(__name__)

#Load the enviroment variables
load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
customer_microservice_url = os.getenv('CUSTOMER_MICROSERVICE', "https://customer-microservice-b4dsccfkbffjh5cv.northeurope-01.azurewebsites.net")
cars_microservice_url = os.getenv('CARS_MICROSERVICE')
subscription_microservice_url = os.getenv('SUBSCRIPTION_MICROSERVICE')
jwt = JWTManager(app)

# Initialize Swagger
#init_swagger(app) 


# Documentaion endpoint
@app.route("/", methods=["GET"])
def homepoint():
    return jsonify({
        "SERVICE": "API-GATEWAY SERVICE",
        "AVAILABLE ENDPOINTS": [
            {
            "MICROSERVICE": "CUSTOMER-MICROSERVICE",
            "PATH": "/api/customer"
            },
            {
            "MICROSERVICE": "SUBSCRIPTION-MICROSERVICE",
            "PATH": "/api/subscription"
            },
            {
            "MICROSERVICE": "CARS-MICROSERVICE",
            "PATH": "/api/cars"
            }
        ]
    })


# CUSTOMER MICROSERVICE
@app.route("/api/customer/<path:route>", methods=["GET","POST","DELETE"])
def customer_microservice(route):
    
    try:
        response = requests.request(
            method=request.method,
            url=f'{customer_microservice_url}/{route}',
            headers=request.headers,
            json=request.get_json(silent=True)
        )

        return response.text, response.status_code, response.headers.items()
    
    except Exception as e:
        return jsonify({
            "Error": "OOPS! Something went wrong :(",
            "Message": f'{e}'
        }), 500
        

#CARS MICROSERVICE

#SUBSCRIPTION MICROSERVICE

if __name__ == "__main__":
    app.run(debug=True)