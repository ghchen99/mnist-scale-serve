# Docker Instructions

## Initial Setup and Running

1. Build the Docker image:
```bash
docker build -t mnist-classifier .
```

2. Create a volume for model persistence:
```bash
docker volume create mnist-models
```

3. Run the container:
```bash
docker run -p 8000:8000 -v mnist-models:/app/models mnist-classifier
```

## Testing the API

4. Send a test request:
```bash
curl -X POST -F "file=@five.jpg" http://localhost:8000/predict
```

## Daily Development Workflow

### Starting Your Day
```bash
# If container exists but is stopped
docker start $(docker ps -a -q --filter ancestor=mnist-classifier)

# If you need to create a new container
docker run -p 8000:8000 -v mnist-models:/app/models mnist-classifier
```

### After Code Changes
```bash
# Stop and remove container
docker stop $(docker ps -q --filter ancestor=mnist-classifier)
docker rm $(docker ps -a -q --filter ancestor=mnist-classifier)

# Rebuild image
docker build -t mnist-classifier .

# Run new container
docker run -p 8000:8000 -v mnist-models:/app/models mnist-classifier
```

### End of Day
```bash
# Stop container (if you plan to reuse it tomorrow)
docker stop $(docker ps -q --filter ancestor=mnist-classifier)
```

## Cleanup Scenarios

### Light Cleanup (Keeping Model Data)
When to use: After testing, daily development, or when freeing up resources
```bash
# Stop and remove container
docker stop $(docker ps -q --filter ancestor=mnist-classifier)
docker rm $(docker ps -a -q --filter ancestor=mnist-classifier)
```

### Medium Cleanup (Removing Image)
When to use: After significant code changes or when updating dependencies
```bash
# Stop and remove container
docker stop $(docker ps -q --filter ancestor=mnist-classifier)
docker rm $(docker ps -a -q --filter ancestor=mnist-classifier)

# Remove image
docker rmi mnist-classifier
```

### Full Cleanup (Complete Reset)
When to use: Project completion, system cleanup, or when you want to start fresh
```bash
# Stop and remove container
docker stop $(docker ps -q --filter ancestor=mnist-classifier)
docker rm $(docker ps -a -q --filter ancestor=mnist-classifier)

# Remove image
docker rmi mnist-classifier

# Remove volume (deletes trained model!)
docker volume rm mnist-models
```

## Useful Commands

### Check Status
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List images
docker images

# List volumes
docker volume ls
```

### Debugging
```bash
# View container logs
docker logs $(docker ps -q --filter ancestor=mnist-classifier)

# Access container shell
docker exec -it $(docker ps -q --filter ancestor=mnist-classifier) /bin/bash

# Check volume data
docker volume inspect mnist-models
```

## Common Scenarios

### After Successful API Call
- If continuing development: Leave container running
- If done testing: Use Light Cleanup
- If changing code: Follow "After Code Changes" workflow

### When to Remove Volume
- When you want to force model retraining
- When the model architecture changes significantly
- When cleaning up the project completely
- When troubleshooting model-related issues

### When to Rebuild Image
- After changing any code
- After modifying requirements.txt
- After changing Dockerfile
- When switching between local and production configurations

### When to Remove Container Only
- When stopping work for the day
- When needing to free up system resources
- Before rebuilding image after code changes
- When troubleshooting container-specific issues
