# DevSecOps CI/CD Pipeline

A production-style DevSecOps pipeline with automated security 
scanning, built on AWS.

## 🔗 Live Demo
http://3.80.134.192:8080

## 🛠️ Tech Stack
- **Cloud:** AWS EC2 (Free Tier)
- **Containers:** Docker
- **CI/CD:** GitHub Actions
- **Security Scanning:** Trivy (image scan), Safety (dependency scan)
- **Registry:** Docker Hub
- **Language:** Python (Flask)

## 🔒 Security Pipeline
- OWASP Safety scans Python dependencies on every push
- Trivy scans Docker image for OS and library CVEs
- CRITICAL vulnerabilities automatically block deployment
- Only verified clean images are deployed to production

## 🔄 Pipeline Stages
Code Push
  → OWASP Dependency Scan
  → Docker Build
  → Trivy Image Scan
  → Push to Docker Hub (only if clean)
  → Deploy to EC2 (only if clean)

## 📌 Endpoints
- GET /        → App status and version
- GET /health  → Health check