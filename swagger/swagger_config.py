from flasgger import Swagger

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "specs": [
                {
                    "endpoint": 'Gateway service',
                    "route": '/microservice/route',
                    "spec": '/swagger/gateway_yaml'
                }
            ],
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

template = {
    "info": {
        "title": "API-Gateway",
        "description": "API-Gateway service that handles all communication between the microservices and the user",
        "version": "1.0.0",
        "contact": {
            "name": "API-Gateway",
            "url": "https://api-gatewayservice-cbc0dydhctg9g0hk.northeurope-01.azurewebsites.net"
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
        }
    }
}

def init_swagger(app):
    """Initialize Swagger with the given Flask app"""
    return Swagger(app, config=swagger_config, template=template)