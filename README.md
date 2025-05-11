# flask-observability-deployment
Flask App Deployment
This project deploys a Flask web application to AWS EKS with observability using OpenTelemetry, Prometheus, and Grafana.
Prerequisites

AWS CLI configured with credentials
Terraform v1.9.8
Helm v3.16.2
kubectl v1.31.0
Docker
An ECR repository
ACM certificate for TLS

Setup Instructions

Build and Push Docker Image

Build the Docker image:docker build -t flask-app .


Tag and push to ECR:docker tag flask-app <your-ecr-repo>:latest
aws ecr get-login-password | docker login --username AWS --password-stdin <your-ecr-repo>
docker push <your-ecr-repo>:latest




Provision Infrastructure

Initialize Terraform:cd terraform
terraform init


Apply Terraform configuration:terraform apply




Configure kubectl

Update kubeconfig:aws eks update-kubeconfig --name flask-eks --region us-west-2




Deploy Application

Install the Helm chart:helm install flask-app ./helm/flask-app --set image.repository=<your-ecr-repo>




Access the Application

Get the Ingress URL:kubectl get ingress flask-app


Access the app at https://flask-app.example.com (update DNS to point to the ALB).



Usage

The app is available at the Ingress URL.
Monitor metrics in Grafana (deploy Prometheus and Grafana to the cluster separately).
View traces in Jaeger (if deployed).

Notes

Replace <your-ecr-repo> with your ECR repository URL.
Update <your-acm-certificate-arn> in the Ingress configuration.
Ensure DNS is configured for flask-app.example.com.

