# DevSecOps CI/CD Pipeline

## 🔗 Live Demo
http://3.80.134.192:8080

## 🛠️ Tech Stack
- **Cloud:** AWS EC2, CloudWatch, CloudTrail, Lambda, SNS
- **Containers:** Docker
- **CI/CD:** GitHub Actions
- **Security Scanning:** Trivy, OWASP Safety
- **Monitoring:** CloudWatch Agent, Custom Dashboard
- **Alerting:** Lambda health check + SNS email alerts
- **Audit Logging:** AWS CloudTrail

## 🔒 Security Pipeline
- OWASP Safety scans Python dependencies on every push
- Trivy scans Docker image for CRITICAL CVEs
- CRITICAL vulnerabilities block deployment automatically
- CloudTrail logs every AWS API action for audit

## 📊 Monitoring
- CloudWatch collects CPU, memory, disk metrics every 60s
- CloudWatch Dashboard shows live graphs
- CPU alarm fires if usage exceeds 80%
- Lambda pings /health endpoint every 5 minutes
- Email alert sent immediately if app goes down

## 🔄 Pipeline Stages
Code Push
  → OWASP Dependency Scan
  → Docker Build
  → Trivy Image Scan
  → Push to Docker Hub (only if clean)
  → Deploy to EC2 (only if clean)

## 📌 Endpoints
- GET /        → App status and version
- GET /health  → Health check (monitored by Lambda)