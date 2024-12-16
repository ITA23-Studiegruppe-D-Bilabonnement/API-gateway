# API Gateway Service

This Flask-based API Gateway serves as a single entry point for multiple microservices, including customer management, car management, and subscription services. It supports routing, request forwarding, and basic error handling.

---

# File structure
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
| `GET`       | Connect to customer microservice | `/api/customer` | Allows for the use of microservice. |
| `GET`       | Connect to subscription microservice | `/api/subscription`| Allows for the use of microservice.|
| `GET`       | Connect to cars microservice  | `/api/cars`        | Allows for the use of microservice. |


### **Home Endpoint**

- **URL**: `/`
- **Method**: `GET`
- **Description**: Provides a summary of the available microservices and their base paths.
- **Response**:
    ```json
    {
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
    }
    ```

---

### **Customer Microservice**

- **Base Path**: `/api/customer`

#### **Home Endpoint**
- **URL**: `/api/customer`
- **Method**: `GET`
- **Description**: Forwards the root request to the customer microservice.
- **Response**:
    - The response is forwarded directly from the customer microservice.

#### **Dynamic Route**
- **URL**: `/api/customer/<path:route>`
- **Methods**: `GET`, `POST`, `DELETE`
- **Description**: Forwards dynamic requests to the customer microservice.
- **Response**:
    - Status codes and response body are forwarded from the customer microservice.
    - **500 Internal Server Error**: If an exception occurs, the gateway returns:
        ```json
        {
            "Error": "OOPS! Something went wrong :(",
            "Message": "Error details"
        }
        ```

---

### **Cars Microservice**

- **Base Path**: `/api/cars`

#### **Home Endpoint**
- **URL**: `/api/cars`
- **Method**: `GET`
- **Description**: Forwards the root request to the cars microservice.
- **Response**:
    - The response is forwarded directly from the cars microservice.

#### **Dynamic Route**
- **URL**: `/api/cars/<path:route>`
- **Methods**: `GET`, `POST`, `DELETE`
- **Description**: Forwards dynamic requests to the cars microservice.
- **Response**:
    - Status codes and response body are forwarded from the cars microservice.
    - **500 Internal Server Error**: If an exception occurs, the gateway returns:
        ```json
        {
            "Error": "OOPS! Something went wrong :(",
            "Message": "Error details"
        }
        ```

---

### **Subscription Microservice**

- **Base Path**: `/api/subscription`

#### **Home Endpoint**
- **URL**: `/api/subscription`
- **Method**: `GET`
- **Description**: Forwards the root request to the subscription microservice.
- **Response**:
    - The response is forwarded directly from the subscription microservice.

#### **Dynamic Route**
- **URL**: `/api/subscription/<path:route>`
- **Methods**: `GET`, `POST`, `DELETE`, `PATCH`
- **Description**: Forwards dynamic requests to the subscription microservice.
- **Response**:
    - Status codes and response body are forwarded from the subscription microservice.
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
| `SUBSCRIPTION_MICROSERVICE`  | Yes      | `https://subscription-microservice-gxbuenczgcd5hfe4.northeurope-01.azurewebsites.net`       | URL of the subscription microservice            |

---

## Error Handling

All microservices forward their status codes and responses to the client. The gateway only handles `500 Internal Server Error` cases, where a generic error message is returned.

---
