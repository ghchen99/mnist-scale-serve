# MNIST Digit Classifier API

A scalable, containerised REST API for handwritten digit classification using TensorFlow and FastAPI, deployed on Kubernetes.

## Overview

This application provides a REST API service that accepts handwritten digit images and returns predictions using a convolutional neural network (CNN) trained on the MNIST dataset. The service is containerised using Docker and designed to be deployed on Kubernetes with automatic scaling capabilities.

## Features

- FastAPI-based REST API
- TensorFlow CNN model for digit classification
- Docker containerisation
- Kubernetes deployment with:
  - Horizontal Pod Autoscaling
  - Persistent volume for model storage
  - Load balancing
  - Health checks
- CORS support for cross-origin requests
- Automatic model training if no pre-trained model exists

## Prerequisites

- Docker
- Kubernetes cluster
- Python 3.12
- kubectl CLI tool

## Project Structure

```
├── Dockerfile
├── app
│   ├── main.py          # FastAPI application
│   ├── model.py         # ML model definition and training
│   └── utils.py         # Image preprocessing utilities
├── k8s
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── persistent-volume.yaml
│   └── service.yaml
└── requirements.txt
```

## Installation

1. Build the Docker image:
```bash
docker build -t mnist-classifier:latest .
```

2. Apply the Kubernetes configurations:
```bash
kubectl apply -f k8s/
```

## API Endpoints

### GET /
Health check endpoint that returns a simple status message.

**Response:**
```json
{
    "message": "MNIST Classification API"
}
```

### POST /predict
Accepts an image file and returns the predicted digit with confidence score.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: Image file (supported formats: JPEG, PNG)

**Response:**
```json
{
    "predicted_digit": 5,
    "confidence": 0.98
}
```

## Model Architecture

The CNN architecture consists of:
- 3 Convolutional layers with ReLU activation
- 2 MaxPooling layers
- Dense layer with 64 units
- Output layer with 10 units (softmax activation)

The model is trained on the MNIST dataset with the following specifications:
- Input shape: (28, 28, 1)
- Optimiser: Adam
- Loss function: Sparse Categorical Crossentropy
- Training epochs: 5

## Kubernetes Configuration

The application is deployed with the following Kubernetes resources:

- **Deployment:** 3 replicas with resource limits and readiness probes
- **HorizontalPodAutoscaler:** Scales from 3 to 10 replicas based on CPU utilization
- **PersistentVolume:** 1GB storage for model persistence
- **Service:** LoadBalancer type for external access

### Resource Limits
- CPU: 1000m (1 core)
- Memory: 1Gi

### Scaling Policy
- Minimum replicas: 3
- Maximum replicas: 10
- Target CPU utilisation: 70%

## Development

To run the application locally for development:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Security Considerations

- The API currently allows all origins through CORS. For production, configure specific allowed origins.
- The model is stored in a persistent volume. Ensure proper access controls in production.
- Consider implementing authentication for the API endpoints in production.

## Performance Optimisation

- The application uses CPU-only mode to avoid GPU dependencies, suitable for most deployment scenarios.
- Image preprocessing is optimised for the MNIST format (28x28 grayscale).
- Kubernetes HPA ensures efficient resource utilisation and scalability.

