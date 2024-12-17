# API Gateway Service

This Flask-based API Gateway serves as a single entry point for multiple microservices, including customer management, car management, and subscription services. It supports routing, request forwarding, and basic error handling.

---

## File structure
```
project/
├── app.py                   
├── swagger/                 
│   ├── gateway.yaml                
│   ├── swagger_config.py    
├── .dockerignore            
├── .env                     
├── .github/                 
│   └── workflows/           
│       └── main_API-gatewayservice.yml 
├── .gitignore               
├── Dockerfile               
├── README.md                
├── requirements.txt
```

## Endpoints

| HTTP Method | Action             | Example Endpoint     | Notes                                   |
|-------------|--------------------|----------------------|-----------------------------------------|
| `GET`,`POST`,`DELETE`,`PUT`,`PATCH` | Connects to the specified microservice | `/<microservice>/<route>` | Allows for the use of microservices. |


### **Home Endpoint**

- **URL**: `/`
- **Method**: `GET`
- **Description**: Provides a summary of the available endpoints
- **Response**:
    ```json
    {
        "SERVICE": "API-GATEWAY SERVICE",
        "AVAILABLE ENDPOINTS": [
            {
                "MICROSERVICE": "CUSTOMER-MICROSERVICE",
                "PATHS": ["List of endpoints"]
            },
            {
                "MICROSERVICE": "SUBSCRIPTION-MICROSERVICE",
                "PATHS": ["List of endpoints"]
            },
            {
                "MICROSERVICE": "CARS-MICROSERVICE",
                "PATHS": ["List of endpoints"]
            },
            {
                "MICROSERVICE": "DAMAGE-MICROSERVICE",
                "PATHS": ["List of endpoints"]
            }
        ]
    }
    ```
---

#### **Dynamic Route**
- **URL**: `/<microservice>/<route>`
- **Methods**: `GET`, `POST`, `DELETE`, `PUT`, `PATCH`
- **Description**: Forwards dynamic requests to the specified  microservice.
- **Response**:
    - Status codes and response body are forwarded from the specified microservice.
    - **500 Internal Server Error**: If an exception occurs, the gateway returns:
        ```json
        {
            "Error": "OOPS! Something went wrong :(",
            "Message": "Error details"
        }
        ```

---

## Environment Variables

| Variable                     | Required | Default                                                                                      | Description                                      |
|------------------------------|----------|----------------------------------------------------------------------------------------------|--------------------------------------------------|
| `JWT_SECRET_KEY`             | Yes      | -                                                                                            | Secret key for JWT token generation             |
| `CUSTOMER_MICROSERVICE`      | Yes      | `https://customer-microservice-b4dsccfkbffjh5cv.northeurope-01.azurewebsites.net`           | URL of the customer microservice                |
| `CARS_MICROSERVICE`          | Yes      | `https://cars-microservice-a7g2hqakb2cjffef.northeurope-01.azurewebsites.net`               | URL of the cars microservice                    |
| `SUBSCRIPTION_MICROSERVICE`  | Yes      | `https://subscription-microservice-gxbuenczgcd5hfe4.northeurope-01.azurewebsites.net`       | URL of the subscription microservice            | `DAMAGE_REPORT_MICROSERVICE`          | Yes      | `https://damagereport-microservice-gpfchac2c4c9hzdc.northeurope-01.azurewebsites.net` | URL of the cars damage report microservice                    |

---

## Error Handling

All microservices forward their status codes and responses to the client. The gateway only handles `500 Internal Server Error` cases, where a generic error message is returned.

---
