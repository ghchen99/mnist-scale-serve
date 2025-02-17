# mnist-scale-serve

A scalable, production-ready service for real-time image classification using MNIST dataset, orchestrated with Kubernetes and FastAPI for high-performance inference and seamless horizontal scaling.

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application
│   ├── model.py             # TensorFlow model definition
│   └── utils.py             # Utility functions
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   ├── service.yaml         # Kubernetes service
│   └── hpa.yaml             # Horizontal Pod Autoscaler
├── Dockerfile               # Docker configuration
└── requirements.txt         # Python dependencies
```