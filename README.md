# DevSecOps CI/CD Pipeline

A production-grade DevSecOps pipeline with automated security scanning,
Kubernetes orchestration, and full AWS observability stack.

## 🔗 Live Demo
- Docker deployment: http://98.88.1.75:8080
- Kubernetes deployment: http://98.88.1.75:30080

## 🏗️ Architecture
```
Developer Laptop
      │
      │  git push
      ▼
┌─────────────────────────────────────┐
│           GitHub Actions            │
│                                     │
│  1. Checkout Code                   │
│  2. OWASP Safety Scan ──────────── FAIL if vulnerable deps
│  3. Docker Build                    │
│  4. Trivy CVE Scan ─────────────── FAIL if CRITICAL found
│  5. Push to Docker Hub              │
│  6. Deploy to EC2                   │
└─────────────────────────────────────┘
      │
      │  SSH deploy
      ▼
┌─────────────────────────────────────┐
│         AWS EC2 (Free Tier)         │
│                                     │
│  ┌──────────────────────────────┐   │
│  │   Kubernetes (Minikube)      │   │
│  │                              │   │
│  │  Pod 1: devsecops-app:8080   │   │
│  │  Pod 2: devsecops-app:8080   │   │
│  │         │                    │   │
│  │  NodePort Service :30080     │   │
│  └──────────────────────────────┘   │
│                                     │
│  CloudWatch Agent                   │
│  (CPU, Memory, Disk → CloudWatch)   │
└─────────────────────────────────────┘
      │                    │
      │                    │  metrics
      ▼                    ▼
 Internet User      CloudWatch Dashboard
 (Live URL)               │
                    CloudWatch Alarms
                          │
                    SNS Email Alerts
                          ▲
                    Lambda /health check
                    (every 5 minutes)

AWS CloudTrail → S3 (all API actions logged)
```

## 🛠️ Complete Tech Stack

| Category       | Technology                        |
|---------------|-----------------------------------|
| Cloud          | AWS EC2, Lambda, SNS, CloudTrail  |
| Monitoring     | CloudWatch Agent + Dashboard      |
| Containers     | Docker, Docker Hub                |
| Orchestration  | Kubernetes (Minikube)             |
| CI/CD          | GitHub Actions                    |
| Security Scan  | Trivy (image), OWASP Safety (deps)|
| Networking     | VPC, Security Groups, Elastic IP  |
| IaC            | Kubernetes YAML manifests         |
| Language       | Python (Flask)                    |

## 🔒 Security Features
- OWASP Safety scans all Python dependencies on every push
- Trivy scans Docker image for OS and library CVEs
- CRITICAL vulnerabilities automatically block deployment
- Least-privilege IAM roles for all AWS services
- CloudTrail audit log of every AWS API call
- Kubernetes resource limits prevent container abuse

## 📊 Monitoring Features
- CloudWatch Agent collects metrics every 60 seconds
- Live dashboard: CPU, memory, disk usage
- Alarm fires email if CPU exceeds 80%
- Lambda health check pings /health every 5 minutes
- Email alert if app stops responding

## 🔄 CI/CD Pipeline Flow
```
Code Push → OWASP Scan → Docker Build → Trivy Scan
         → Docker Hub Push → EC2 Deploy → Kubernetes
```

## 📌 API Endpoints
| Endpoint  | Description                  |
|-----------|------------------------------|
| GET /     | App status, version, time    |
| GET /health | Health check (monitored)   |

## 🗂️ Project Structure
```
devsecops-pipeline/
├── .github/workflows/pipeline.yml  # CI/CD pipeline
├── k8s/
│   ├── deployment.yaml              # Kubernetes deployment
│   └── service.yaml                 # Kubernetes service
├── app.py                           # Flask application
├── Dockerfile                       # Container definition
└── requirements.txt                 # Python dependencies
```