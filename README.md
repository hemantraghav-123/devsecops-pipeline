# DevSecOps CI/CD Pipeline

A production-style DevSecOps pipeline built on AWS with automated 
build, push, and deployment on every code push.

## 🔗 Live Demo
http://3.80.134.192:8080

## 🛠️ Tech Stack
- **Cloud:** AWS EC2 (Free Tier)
- **Containers:** Docker
- **CI/CD:** GitHub Actions
- **Registry:** Docker Hub
- **Language:** Python (Flask)

## 🔄 Pipeline Flow
Code Push → GitHub Actions → Docker Build → Push to Docker Hub → Deploy to EC2

## 📌 Endpoints
- `GET /`       → App status
- `GET /health` → Health check
