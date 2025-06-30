# Application Monitoring and Observability Workflow

## Purpose
Comprehensive monitoring setup for the ADA application to ensure reliability, performance, and quick issue resolution.

## Prerequisites
- Monitoring tools installed (Prometheus, Grafana, ELK stack)
- Log aggregation system configured
- Alert notification channels set up

## Steps

### 1. Application Logging Setup
```python
import logging
import logging.handlers
import json
from datetime import datetime
import traceback

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logs"""
    def format(self, record):
        log_obj = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_obj['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Add custom fields
        if hasattr(record, 'user_id'):
            log_obj['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_obj['request_id'] = record.request_id
        
        return json.dumps(log_obj)

def setup_logging():
    """Configure application logging"""
    # Create logger
    logger = logging.getLogger('ada_app')
    logger.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/ada_app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(JSONFormatter())
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Usage
logger = setup_logging()
```

### 2. Request Tracking Middleware
```python
import uuid
from flask import request, g
import time

@app.before_request
def before_request():
    """Set up request tracking"""
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()
    
    # Log request start
    logger.info(
        "Request started",
        extra={
            'request_id': g.request_id,
            'method': request.method,
            'url': request.url,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
    )

@app.after_request
def after_request(response):
    """Log request completion"""
    duration = time.time() - g.start_time
    
    logger.info(
        "Request completed",
        extra={
            'request_id': g.request_id,
            'status_code': response.status_code,
            'duration': duration,
            'response_size': response.content_length
        }
    )
    
    # Add request ID to response headers
    response.headers['X-Request-ID'] = g.request_id
    return response
```

### 3. Health Checks Implementation
```python
import psutil
import redis
from sqlalchemy import text

@app.route('/health')
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': os.getenv('APP_VERSION', '1.0.0')
    })

@app.route('/health/detailed')
def detailed_health_check():
    """Detailed health check with dependencies"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'checks': {}
    }
    
    # Database check
    try:
        db.session.execute(text('SELECT 1'))
        health_status['checks']['database'] = {'status': 'healthy'}
    except Exception as e:
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['status'] = 'unhealthy'
    
    # Redis check
    try:
        redis_client.ping()
        health_status['checks']['redis'] = {'status': 'healthy'}
    except Exception as e:
        health_status['checks']['redis'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['status'] = 'unhealthy'
    
    # System resources
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status['checks']['system'] = {
            'status': 'healthy',
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent
        }
        
        # Mark unhealthy if resources are critically low
        if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
            health_status['checks']['system']['status'] = 'warning'
            
    except Exception as e:
        health_status['checks']['system'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code
```

### 4. Metrics Collection
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Define metrics
REQUEST_COUNT = Counter('ada_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('ada_request_duration_seconds', 'Request duration')
ACTIVE_CONNECTIONS = Gauge('ada_active_connections', 'Active Socket.IO connections')
ERROR_COUNT = Counter('ada_errors_total', 'Total errors', ['error_type'])

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        start_time = time.time()
        
        def new_start_response(status, response_headers, exc_info=None):
            duration = time.time() - start_time
            
            # Record metrics
            method = environ.get('REQUEST_METHOD', 'GET')
            path = environ.get('PATH_INFO', '/')
            status_code = status.split()[0]
            
            REQUEST_COUNT.labels(method=method, endpoint=path, status=status_code).inc()
            REQUEST_DURATION.observe(duration)
            
            return start_response(status, response_headers, exc_info)
        
        return self.app(environ, new_start_response)

# Add metrics endpoint
@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# Socket.IO connection tracking
@socketio.on('connect')
def handle_connect():
    ACTIVE_CONNECTIONS.inc()

@socketio.on('disconnect')
def handle_disconnect():
    ACTIVE_CONNECTIONS.dec()
```

### 5. Error Tracking and Alerting
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

# Configure Sentry for error tracking
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[
        FlaskIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
)

class AlertManager:
    def __init__(self):
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    def send_alert(self, severity, message, details=None):
        """Send alert to monitoring channels"""
        alert_data = {
            'severity': severity,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'service': 'ada-app',
            'details': details or {}
        }
        
        # Log alert
        logger.error(f"ALERT: {message}", extra=alert_data)
        
        # Send to external systems
        if self.webhook_url and severity in ['critical', 'high']:
            self._send_slack_alert(alert_data)
    
    def _send_slack_alert(self, alert_data):
        """Send alert to Slack"""
        payload = {
            'text': f"🚨 ADA Alert: {alert_data['message']}",
            'attachments': [{
                'color': 'danger' if alert_data['severity'] == 'critical' else 'warning',
                'fields': [
                    {'title': 'Severity', 'value': alert_data['severity'], 'short': True},
                    {'title': 'Service', 'value': alert_data['service'], 'short': True},
                    {'title': 'Time', 'value': alert_data['timestamp'], 'short': True}
                ]
            }]
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")

alert_manager = AlertManager()
```

### 6. Performance Monitoring
```python
import threading
import psutil
from datetime import datetime, timedelta

class PerformanceMonitor:
    def __init__(self):
        self.metrics_history = []
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'response_time': 2.0,
            'error_rate': 0.05
        }
        self.monitoring = False
        
    def start_monitoring(self, interval=60):
        """Start performance monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _monitor_loop(self, interval):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last 24 hours of data
                cutoff_time = datetime.now() - timedelta(hours=24)
                self.metrics_history = [
                    m for m in self.metrics_history 
                    if m['timestamp'] > cutoff_time
                ]
                
                # Check for alerts
                self._check_alerts(metrics)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
            
            time.sleep(interval)
    
    def _collect_metrics(self):
        """Collect system and application metrics"""
        return {
            'timestamp': datetime.now(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'active_connections': len(socketio.server.manager.rooms.get('/', {})),
            'response_time': self._get_avg_response_time(),
            'error_rate': self._get_error_rate()
        }
    
    def _check_alerts(self, metrics):
        """Check metrics against thresholds"""
        for metric, threshold in self.alert_thresholds.items():
            if metric in metrics and metrics[metric] > threshold:
                alert_manager.send_alert(
                    'high',
                    f'{metric.replace("_", " ").title()} is high: {metrics[metric]:.2f}',
                    {'metric': metric, 'value': metrics[metric], 'threshold': threshold}
                )

# Start monitoring
performance_monitor = PerformanceMonitor()
performance_monitor.start_monitoring()
```

### 7. Log Analysis and Dashboards
```python
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import pandas as pd

class LogAnalyzer:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    def search_logs(self, query, start_time, end_time, size=1000):
        """Search logs in Elasticsearch"""
        search_body = {
            'query': {
                'bool': {
                    'must': [
                        {'query_string': {'query': query}},
                        {'range': {
                            'timestamp': {
                                'gte': start_time.isoformat(),
                                'lte': end_time.isoformat()
                            }
                        }}
                    ]
                }
            },
            'sort': [{'timestamp': {'order': 'desc'}}],
            'size': size
        }
        
        result = self.es.search(index='ada-logs-*', body=search_body)
        return result['hits']['hits']
    
    def get_error_trends(self, hours=24):
        """Get error trends over time"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        search_body = {
            'query': {
                'bool': {
                    'must': [
                        {'term': {'level': 'ERROR'}},
                        {'range': {
                            'timestamp': {
                                'gte': start_time.isoformat(),
                                'lte': end_time.isoformat()
                            }
                        }}
                    ]
                }
            },
            'aggs': {
                'errors_over_time': {
                    'date_histogram': {
                        'field': 'timestamp',
                        'interval': '1h'
                    }
                }
            }
        }
        
        result = self.es.search(index='ada-logs-*', body=search_body)
        return result['aggregations']['errors_over_time']['buckets']

# Dashboard generation
def generate_dashboard_data():
    """Generate data for monitoring dashboard"""
    analyzer = LogAnalyzer()
    
    # Get recent errors
    recent_errors = analyzer.search_logs('level:ERROR', 
                                       datetime.now() - timedelta(hours=1),
                                       datetime.now())
    
    # Get performance metrics
    metrics = performance_monitor.metrics_history[-60:]  # Last hour
    
    return {
        'recent_errors': len(recent_errors),
        'avg_response_time': sum(m['response_time'] for m in metrics) / len(metrics) if metrics else 0,
        'current_cpu': psutil.cpu_percent(),
        'current_memory': psutil.virtual_memory().percent,
        'active_connections': len(socketio.server.manager.rooms.get('/', {}))
    }
```

## Monitoring Checklist

### Infrastructure Monitoring
- [ ] CPU, memory, disk usage tracking
- [ ] Network connectivity monitoring
- [ ] Database performance monitoring
- [ ] Redis/cache monitoring
- [ ] Load balancer health checks

### Application Monitoring  
- [ ] Request/response metrics
- [ ] Error rates and types
- [ ] Response time percentiles
- [ ] User session tracking
- [ ] Feature usage analytics

### Business Metrics
- [ ] User engagement metrics
- [ ] AI processing success rates
- [ ] File upload statistics
- [ ] API usage patterns
- [ ] Revenue/cost tracking

### Alerting Setup
- [ ] Critical error alerts
- [ ] Performance degradation alerts
- [ ] Resource exhaustion alerts
- [ ] Security incident alerts
- [ ] Business metric alerts

### Dashboard Creation
- [ ] Real-time system overview
- [ ] Application performance dashboard
- [ ] Error analysis dashboard
- [ ] User activity dashboard
- [ ] Business metrics dashboard

## Tools and Integration

### Monitoring Stack
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **ELK Stack**: Log aggregation and analysis
- **Sentry**: Error tracking and alerting
- **Slack/PagerDuty**: Alert notifications

### Custom Solutions
- Performance monitoring scripts
- Health check endpoints
- Metrics collection middleware
- Alert management system
- Dashboard generation tools
