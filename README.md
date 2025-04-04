# Transformer Model Deployment on AWS

This project sets up a scalable deployment of a sentiment analysis transformer model using Docker, Kubernetes, and AWS.

## Prerequisites

- Docker
- kubectl
- AWS CLI
- EKS cluster
- AWS IAM permissions for EKS and ECR
- Python 3.9+

## Project Structure

```
.
├── app/
│   └── main.py           # FastAPI application with sentiment analysis
├── k8s/
│   ├── deployment.yaml   # Kubernetes deployment
│   ├── service.yaml      # Kubernetes service
│   └── hpa.yaml         # Horizontal Pod Autoscaler
├── .github/
│   └── workflows/        # GitHub Actions workflows
│       ├── test.yml     # Testing and linting
│       ├── docker.yml   # Docker build and push
│       └── deploy.yml   # Kubernetes deployment
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── test_model.py       # Local model testing script
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Testing and Linting** (on every push/PR):
   - Runs Python tests with coverage
   - Checks code formatting with black
   - Verifies import sorting with isort
   - Uploads coverage reports to Codecov

2. **Docker Build** (on push to main or new tag):
   - Builds Docker image
   - Pushes to GitHub Container Registry (ghcr.io)
   - Uses layer caching for faster builds

3. **Kubernetes Deployment** (on new tag):
   - Updates deployment with new image
   - Verifies rollout status
   - Checks service and HPA status

### Required Secrets

Add these secrets to your GitHub repository:
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_REGION`: AWS region
- `KUBE_CONFIG`: Kubernetes configuration file

## Local Development

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Test the model locally:
```bash
python test_model.py
```

4. Run the API service locally:
```bash
cd app
python main.py
```

5. Test the API endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Make a prediction
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "This movie is absolutely fantastic!"}'
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
- `POST /predict`: Make sentiment analysis predictions

Example prediction request:
```bash
curl -X POST "http://<load-balancer-url>/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your input text here"}'
```

Response format:
```json
{
    "label": "POSITIVE",
    "score": 0.9998760223388672
}
```

## Model Details

The service uses the `distilbert-base-uncased-finetuned-sst-2-english` model from Hugging Face, which is fine-tuned for sentiment analysis on the SST-2 dataset.

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