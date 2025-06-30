# ADA Application Security Standards

## Input Validation and Sanitization

### User Input Processing
```python
import re
from flask import request
from markupsafe import escape

def validate_user_message(message):
    """Validate and sanitize user messages"""
    if not message or len(message.strip()) == 0:
        raise ValueError("Message cannot be empty")
    
    if len(message) > 10000:  # Reasonable limit
        raise ValueError("Message too long")
    
    # Remove potential script injections
    sanitized = escape(message)
    
    # Additional sanitization for specific patterns
    sanitized = re.sub(r'<script.*?</script>', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized

def validate_file_upload(file):
    """Validate uploaded files"""
    if not file or file.filename == '':
        raise ValueError("No file selected")
    
    # Check file extension
    allowed_extensions = {'.txt', '.csv', '.json', '.pdf', '.docx'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise ValueError(f"File type {file_ext} not allowed")
    
    # Check file size (max 10MB)
    if len(file.read()) > 10 * 1024 * 1024:
        raise ValueError("File too large")
    
    file.seek(0)  # Reset file pointer
    return True
```

### SQL Injection Prevention
```python
from sqlalchemy import text

# NEVER do this:
# query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ALWAYS use parameterized queries:
def get_user_by_name(name):
    """Safe database query with parameters"""
    result = db.session.execute(
        text("SELECT * FROM users WHERE name = :name"),
        {"name": name}
    )
    return result.fetchone()

# Or use SQLAlchemy ORM:
def get_user_by_name_orm(name):
    """Safe ORM query"""
    return User.query.filter(User.name == name).first()
```

## Authentication and Authorization

### Session Management
```python
from flask_session import Session
import secrets

# Secure session configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'ada_session:'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function
```

### API Key Security
```python
import hashlib
import hmac
from datetime import datetime, timedelta

class APIKeyManager:
    @staticmethod
    def generate_api_key():
        """Generate secure API key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key):
        """Hash API key for storage"""
        salt = secrets.token_bytes(32)
        key_hash = hashlib.pbkdf2_hmac('sha256', api_key.encode(), salt, 100000)
        return salt + key_hash
    
    @staticmethod
    def verify_api_key(api_key, stored_hash):
        """Verify API key against stored hash"""
        salt = stored_hash[:32]
        stored_key = stored_hash[32:]
        key_hash = hashlib.pbkdf2_hmac('sha256', api_key.encode(), salt, 100000)
        return hmac.compare_digest(stored_key, key_hash)
```

## Data Protection

### Encryption at Rest
```python
from cryptography.fernet import Fernet
import base64

class DataEncryption:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY', self.generate_key())
        self.cipher_suite = Fernet(self.key)
    
    @staticmethod
    def generate_key():
        """Generate encryption key"""
        return Fernet.generate_key()
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        return self.cipher_suite.decrypt(encrypted_data).decode()
```

### PII Handling
```python
import re

class PIIHandler:
    @staticmethod
    def detect_pii(text):
        """Detect potential PII in text"""
        patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        
        found_pii = {}
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                found_pii[pii_type] = matches
        
        return found_pii
    
    @staticmethod
    def mask_pii(text):
        """Mask PII in text for logging"""
        # Mask email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                     '[EMAIL_MASKED]', text)
        
        # Mask phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', 
                     '[PHONE_MASKED]', text)
        
        return text
```

## Rate Limiting and DOS Protection

### Request Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

# Configure rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["1000 per hour"]
)

# Apply to specific endpoints
@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
@require_auth
def chat_endpoint():
    """Chat endpoint with rate limiting"""
    pass

@app.route('/api/upload', methods=['POST'])
@limiter.limit("5 per minute")
@require_auth
def upload_endpoint():
    """Upload endpoint with stricter rate limiting"""
    pass
```

### Resource Protection
```python
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta

class ResourceMonitor:
    def __init__(self):
        self.request_counts = defaultdict(deque)
        self.blocked_ips = set()
        self.lock = threading.Lock()
    
    def check_request_rate(self, ip_address, max_requests=100, time_window=60):
        """Check if IP is making too many requests"""
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=time_window)
            
            # Clean old requests
            while (self.request_counts[ip_address] and 
                   self.request_counts[ip_address][0] < cutoff):
                self.request_counts[ip_address].popleft()
            
            # Add current request
            self.request_counts[ip_address].append(now)
            
            # Check if over limit
            if len(self.request_counts[ip_address]) > max_requests:
                self.blocked_ips.add(ip_address)
                return False
            
            return True
```

## Logging and Monitoring

### Security Event Logging
```python
import logging
from datetime import datetime

# Configure security logger
security_logger = logging.getLogger('security')
security_handler = logging.FileHandler('logs/security.log')
security_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
security_handler.setFormatter(security_formatter)
security_logger.addHandler(security_handler)
security_logger.setLevel(logging.INFO)

def log_security_event(event_type, details, user_id=None, ip_address=None):
    """Log security-related events"""
    log_data = {
        'event_type': event_type,
        'timestamp': datetime.now().isoformat(),
        'details': details,
        'user_id': user_id,
        'ip_address': ip_address
    }
    
    security_logger.info(f"SECURITY_EVENT: {log_data}")

# Usage examples:
# log_security_event('LOGIN_ATTEMPT', 'Failed login', user_id='user123', ip_address='192.168.1.1')
# log_security_event('FILE_UPLOAD', 'Suspicious file type', user_id='user456')
# log_security_event('RATE_LIMIT_EXCEEDED', 'Too many requests', ip_address='192.168.1.100')
```

## Environment Security

### Secure Configuration
```python
# .env file template (never commit this file)
"""
# Application
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DEBUG=False

# Database
DATABASE_URL=postgresql://user:pass@localhost/ada_db

# API Keys (never log these)
GEMINI_API_KEY=your-gemini-key
WEATHER_API_KEY=your-weather-key

# Security
ENCRYPTION_KEY=your-encryption-key
SESSION_TIMEOUT=7200

# Rate Limiting
REDIS_URL=redis://localhost:6379
MAX_REQUESTS_PER_MINUTE=60

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_FOLDER=/secure/uploads/
"""

# Secure environment variable handling
def get_required_env(key):
    """Get required environment variable or raise error"""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Required environment variable {key} not set")
    return value

def get_env_bool(key, default=False):
    """Get boolean environment variable"""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')
```

## HTTPS and Transport Security

### Flask HTTPS Configuration
```python
from flask_talisman import Talisman

# Force HTTPS and security headers
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
    }
)

# CORS configuration
from flask_cors import CORS

CORS(app, 
    origins=['https://yourdomain.com'],
    methods=['GET', 'POST'],
    allow_headers=['Content-Type', 'Authorization'],
    supports_credentials=True
)
```

## Security Checklist

- [ ] All user inputs validated and sanitized
- [ ] SQL injection protection implemented
- [ ] Authentication and authorization in place
- [ ] API keys properly secured
- [ ] PII detection and masking implemented
- [ ] Rate limiting configured
- [ ] Security logging active
- [ ] HTTPS enforced
- [ ] Environment variables secured
- [ ] File upload restrictions implemented
- [ ] Session management configured
- [ ] CORS properly configured
- [ ] Security headers set
- [ ] Regular security audits scheduled
