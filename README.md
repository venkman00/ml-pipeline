# Transformer Model Deployment on AWS

This project sets up a scalable deployment of a transformer model using Docker, Kubernetes, and AWS.

## Prerequisites

- Docker
- kubectl
- AWS CLI
- EKS cluster
- AWS IAM permissions for EKS and ECR

## Project Structure

```
.
├── app/
│   └── main.py           # FastAPI application
├── k8s/
│   ├── deployment.yaml   # Kubernetes deployment
│   ├── service.yaml      # Kubernetes service
│   └── hpa.yaml         # Horizontal Pod Autoscaler
├── Dockerfile           # Docker configuration
└── requirements.txt     # Python dependencies
```

## Deployment Steps

1. Build and push Docker image:
```bash
# Set your ECR repository URL
export DOCKER_REGISTRY=<your-ecr-repository-url>

# Build the image
docker build -t ${DOCKER_REGISTRY}/transformer-model:latest .

# Login to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin ${DOCKER_REGISTRY}

# Push the image
docker push ${DOCKER_REGISTRY}/transformer-model:latest
```

2. Deploy to Kubernetes:
```bash
# Apply Kubernetes configurations
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

3. Verify deployment:
```bash
kubectl get pods
kubectl get services
kubectl get hpa
```

## API Usage

The service exposes the following endpoints:

- `GET /health`: Health check endpoint
- `POST /predict`: Make predictions with the transformer model

Example prediction request:
```bash
curl -X POST "http://<load-balancer-url>/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your input text here"}'
```

## Scaling

The deployment includes:
- Horizontal Pod Autoscaler (HPA) for automatic scaling
- Resource limits and requests for CPU and memory
- Health checks and readiness probes

## Monitoring

Monitor your deployment using:
- AWS CloudWatch
- Kubernetes metrics
- Application logs

## Security Considerations

- Use AWS IAM roles for service accounts
- Implement proper network policies
- Use AWS Secrets Manager for sensitive data
- Enable encryption at rest and in transit 