# CI/CD Pipeline

## Pipeline Flow

```
Checkout Code
      ↓
Install Dependencies
      ↓
Run Linting
      ↓
Run Unit Tests
      ↓
Run Integration Tests
      ↓
Build Docker Images
      ↓
Security Scan
      ↓
Push Docker Images
      ↓
Deploy to Kubernetes
      ↓
Smoke Test
      ↓
Notify Team
```

---

## Stages

### Checkout

Downloads the latest repository.

### Install Dependencies

Backend

- pip install -r requirements.txt

Frontend

- npm install

### Lint

Checks coding errors.

### Unit Tests

Runs backend and frontend tests.

### Integration Tests

Verifies API integration.

### Docker Build

Builds backend and frontend images.

### Security Scan

Scans filesystem using Trivy.

### Push Images

Pushes Docker images to registry.

### Deploy

Deploys to Kubernetes cluster.

### Smoke Test

Verifies deployment is healthy.

### Notification

Sends deployment status.
