# DevOps and Deployment Standards

## Universal DevOps Principles

### Infrastructure as Code (IaC)
- **Version Control Everything**: Infrastructure definitions, configurations, and scripts
- **Immutable Infrastructure**: Replace rather than modify infrastructure components
- **Environment Parity**: Keep development, staging, and production environments similar
- **Automated Provisioning**: Use tools to automate infrastructure creation and management
- **Documentation**: Maintain clear documentation for infrastructure and deployment processes

### Continuous Integration/Continuous Deployment (CI/CD)
- **Automated Testing**: Run comprehensive tests on every code change
- **Build Automation**: Automate build processes for consistency and reliability
- **Deployment Automation**: Minimize manual deployment steps
- **Rollback Capabilities**: Ensure quick rollback mechanisms for failed deployments
- **Environment Promotion**: Use consistent processes to promote code through environments

## Project-Specific Implementation Instructions

### For Each New Project
**Create in project root**: `deployment/`
```
deployment/
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── .dockerignore
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── scripts/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── health-check.sh
└── documentation/
    ├── deployment-guide.md
    ├── infrastructure-overview.md
    └── troubleshooting.md
```

### Environment Configuration
**Create in project `.clinerules/`**: `deployment-standards.md`
Include:
- Deployment target configuration (cloud provider, on-premise)
- Environment variable management strategy
- Secret management and rotation procedures
- Monitoring and alerting setup
- Backup and disaster recovery procedures

## Containerization Standards

### Docker Best Practices
```dockerfile
# Multi-stage build example
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runtime
# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

WORKDIR /app
# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

# Switch to non-root user
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000
CMD ["npm", "start"]
```

### Container Security Standards
- **Minimal Base Images**: Use alpine or distroless images when possible
- **Non-Root User**: Always run containers as non-root user
- **Security Scanning**: Scan images for vulnerabilities regularly
- **Resource Limits**: Set appropriate CPU and memory limits
- **Read-Only Filesystems**: Use read-only root filesystems when possible

### Project-Specific Container Instructions
**Create in project `deployment/docker/`**: `container-strategy.md`
Include:
- Base image selection and justification
- Multi-stage build strategy for optimization
- Container registry configuration and access
- Image tagging and versioning strategy
- Container security scanning setup

## CI/CD Pipeline Standards

### Universal Pipeline Principles
- **Fail Fast**: Detect issues early in the pipeline
- **Parallel Execution**: Run independent steps in parallel
- **Artifact Management**: Store and version build artifacts
- **Environment Isolation**: Use separate environments for different stages
- **Pipeline as Code**: Define pipelines in version-controlled files

### GitHub Actions Example
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run security scan
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: security-scan-results.sarif

  build:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to production
      run: |
        # Deploy using your preferred method
        ./deployment/scripts/deploy.sh
```

### Project-Specific Pipeline Instructions
**Create in project `.github/workflows/`** or equivalent CI system:
Include:
- Test strategy and coverage requirements
- Build optimization and caching strategy
- Deployment target configuration
- Environment-specific deployment procedures
- Rollback and recovery procedures

## Infrastructure as Code

### Terraform Best Practices
```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "company-terraform-state"
    key    = "apps/myapp/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Application infrastructure
resource "aws_ecs_cluster" "app_cluster" {
  name = "${var.project_name}-${var.environment}"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_service" "app_service" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.app_task.arn
  desired_count   = var.app_instance_count
  
  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.app_tg.arn
    container_name   = "app"
    container_port   = 8000
  }
}
```

### Infrastructure Security Standards
- **State File Security**: Encrypt and secure Terraform state files
- **Access Control**: Use IAM roles and policies for least privilege access
- **Network Security**: Implement proper VPC, subnet, and security group configurations
- **Secrets Management**: Use cloud-native secret management services
- **Compliance**: Implement compliance frameworks and auditing

### Project-Specific Infrastructure Instructions
**Create in project `deployment/terraform/`**: `infrastructure-design.md`
Include:
- Architecture diagram and component descriptions
- Resource naming conventions and tagging strategy
- Network design and security considerations
- Scaling and capacity planning
- Cost optimization strategies

## Monitoring and Observability

### Universal Monitoring Principles
- **Three Pillars**: Implement metrics, logs, and traces
- **SLA Definition**: Define and monitor service level agreements
- **Alert Fatigue**: Avoid too many alerts, focus on actionable issues
- **Dashboard Design**: Create clear, actionable dashboards
- **Incident Response**: Have clear escalation and response procedures

### Application Monitoring Setup
```python
# Example monitoring setup with Prometheus and Grafana
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import logging
import time

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')
ACTIVE_USERS = Gauge('app_active_users', 'Active users')

def monitor_request(func):
    """Decorator to monitor request metrics"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            REQUEST_COUNT.labels(method='GET', endpoint='/api', status='200').inc()
            return result
        except Exception as e:
            REQUEST_COUNT.labels(method='GET', endpoint='/api', status='500').inc()
            raise
        finally:
            REQUEST_DURATION.observe(time.time() - start_time)
    return wrapper

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Start metrics server
start_http_server(8000)
```

### Project-Specific Monitoring Instructions
**Create in project `deployment/monitoring/`**: `observability-setup.md`
Include:
- Monitoring stack choice and configuration
- Key performance indicators and alert thresholds
- Log aggregation and analysis setup
- Distributed tracing configuration
- Dashboard design and maintenance procedures

## Security and Compliance

### DevOps Security Standards
- **Secrets Management**: Never store secrets in code or containers
- **Access Control**: Implement least privilege access to systems
- **Security Scanning**: Scan code, dependencies, and infrastructure
- **Compliance Monitoring**: Automate compliance checks and reporting
- **Incident Response**: Have security incident response procedures

### Security Scanning Integration
```yaml
# Example security scanning in CI/CD
security-scan:
  runs-on: ubuntu-latest
  steps:
  - uses: actions/checkout@v4
  
  # SAST - Static Application Security Testing
  - name: Run SAST scan
    uses: securecodewarrior/github-action-add-sarif@v1
    with:
      sarif-file: sast-results.sarif
  
  # Dependency scanning
  - name: Run dependency check
    uses: dependency-check/Dependency-Check_Action@main
    with:
      project: 'my-app'
      path: '.'
      format: 'ALL'
  
  # Container scanning
  - name: Run container scan
    uses: aquasec/trivy-action@master
    with:
      image-ref: '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest'
      format: 'sarif'
      output: 'trivy-results.sarif'
```

### Project-Specific Security Instructions
**Create in project `deployment/security/`**: `security-procedures.md`
Include:
- Security scanning tool configuration
- Vulnerability management procedures
- Compliance framework implementation
- Security incident response procedures
- Access management and rotation procedures

## Environment Management

### Environment Strategy
- **Development**: Local development with hot reload and debugging
- **Staging**: Production-like environment for integration testing
- **Production**: Live environment with monitoring and alerting
- **Feature Environments**: Temporary environments for feature development

### Environment Configuration Management
```bash
#!/bin/bash
# deployment/scripts/deploy.sh

set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "Deploying to $ENVIRONMENT with version $VERSION"

# Load environment-specific configuration
source "deployment/config/$ENVIRONMENT.env"

# Validate required variables
required_vars=("DATABASE_URL" "REDIS_URL" "SECRET_KEY")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "Error: $var is not set"
        exit 1
    fi
done

# Deploy application
if [[ "$ENVIRONMENT" == "production" ]]; then
    # Production deployment with blue-green strategy
    ./deployment/scripts/blue-green-deploy.sh "$VERSION"
else
    # Direct deployment for non-production
    kubectl set image deployment/app-deployment app="$IMAGE_REGISTRY/app:$VERSION"
    kubectl rollout status deployment/app-deployment
fi

# Run health checks
./deployment/scripts/health-check.sh "$ENVIRONMENT"

echo "Deployment to $ENVIRONMENT completed successfully"
```

### Project-Specific Environment Instructions
**Create in project `deployment/config/`**: Environment configuration files
Include:
- Environment-specific variable definitions
- Service configuration for each environment
- Resource allocation and scaling parameters
- Monitoring and alerting configuration
- Backup and recovery procedures

## Deployment Strategies

### Blue-Green Deployment
```bash
#!/bin/bash
# deployment/scripts/blue-green-deploy.sh

VERSION=$1
CURRENT_ENV=$(kubectl get service app-service -o jsonpath='{.spec.selector.environment}')
NEW_ENV=$([ "$CURRENT_ENV" = "blue" ] && echo "green" || echo "blue")

echo "Current environment: $CURRENT_ENV"
echo "Deploying to: $NEW_ENV"

# Deploy to new environment
kubectl set image deployment/app-$NEW_ENV-deployment app="$IMAGE_REGISTRY/app:$VERSION"
kubectl rollout status deployment/app-$NEW_ENV-deployment

# Health check new environment
if ! ./deployment/scripts/health-check.sh $NEW_ENV; then
    echo "Health check failed, rolling back"
    exit 1
fi

# Switch traffic to new environment
kubectl patch service app-service -p '{"spec":{"selector":{"environment":"'$NEW_ENV'"}}}'

echo "Successfully switched to $NEW_ENV environment"
```

### Rolling Deployment
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myregistry/myapp:latest
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Project-Specific Deployment Instructions
**Create in project `deployment/documentation/`**: `deployment-strategies.md`
Include:
- Deployment strategy choice and justification
- Rollback procedures and automation
- Canary deployment configuration if applicable
- Feature flag integration for controlled rollouts
- Performance impact assessment procedures

## Disaster Recovery

### Backup and Recovery Standards
- **Automated Backups**: Implement automated backup procedures
- **Recovery Testing**: Regularly test backup restoration procedures
- **RTO/RPO Objectives**: Define recovery time and point objectives
- **Geographic Distribution**: Store backups in multiple regions
- **Documentation**: Maintain clear disaster recovery procedures

### Recovery Procedures Template
```bash
#!/bin/bash
# deployment/scripts/disaster-recovery.sh

BACKUP_DATE=${1:-$(date -d "yesterday" +%Y-%m-%d)}
RECOVERY_ENVIRONMENT=${2:-staging}

echo "Starting disaster recovery for $BACKUP_DATE to $RECOVERY_ENVIRONMENT"

# Restore database
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier "app-recovery-$(date +%s)" \
    --db-snapshot-identifier "app-snapshot-$BACKUP_DATE"

# Restore application data
aws s3 sync "s3://app-backups/$BACKUP_DATE/" ./recovery-data/

# Deploy application in recovery mode
kubectl apply -f deployment/kubernetes/recovery-deployment.yaml

# Verify recovery
./deployment/scripts/recovery-verification.sh

echo "Disaster recovery completed"
```

### Project-Specific Recovery Instructions
**Create in project `deployment/documentation/`**: `disaster-recovery-plan.md`
Include:
- Recovery time objectives and procedures
- Data backup and restoration procedures
- Communication plan during disasters
- Recovery testing schedule and procedures
- Post-recovery validation and reporting

## Quality Checklist

Before deploying to production, ensure:
- [ ] All tests pass in CI/CD pipeline
- [ ] Security scans completed with acceptable results
- [ ] Infrastructure changes are code-reviewed and tested
- [ ] Monitoring and alerting are configured and tested
- [ ] Rollback procedures are tested and documented
- [ ] Performance benchmarks meet requirements
- [ ] Security configurations are validated
- [ ] Backup and recovery procedures are tested
- [ ] Documentation is updated and accessible
- [ ] Incident response procedures are in place
