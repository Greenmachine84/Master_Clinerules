# API Design Standards

## Universal API Principles

### RESTful API Design
- **Resource-Based URLs**: Use nouns, not verbs in URL paths
- **HTTP Methods**: Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **Status Codes**: Return meaningful HTTP status codes
- **Consistent Naming**: Use consistent naming conventions across all endpoints
- **Stateless Design**: APIs should be stateless and not rely on server-side sessions

### API Versioning Strategy
- **Version in URL**: Use version numbers in URL path (e.g., `/api/v1/users`)
- **Backward Compatibility**: Maintain backward compatibility when possible
- **Deprecation Policy**: Provide clear deprecation timelines and migration paths
- **Version Documentation**: Document changes between versions
- **Semantic Versioning**: Follow semantic versioning principles

```python
# URL Structure Examples
GET    /api/v1/users              # List users
GET    /api/v1/users/{id}         # Get specific user
POST   /api/v1/users              # Create user
PUT    /api/v1/users/{id}         # Update entire user
PATCH  /api/v1/users/{id}         # Partial user update
DELETE /api/v1/users/{id}         # Delete user

# Nested Resources
GET    /api/v1/users/{id}/posts   # Get user's posts
POST   /api/v1/users/{id}/posts   # Create post for user
```

## Project-Specific Implementation Instructions

### For Each New API Project
**Create in project root**: `api/`
```
api/
├── schemas/
│   ├── requests/        # Request validation schemas
│   ├── responses/       # Response format schemas
│   └── shared/          # Shared data models
├── documentation/
│   ├── openapi.yaml     # OpenAPI specification
│   ├── postman/         # Postman collections
│   └── examples/        # Request/response examples
├── middleware/
│   ├── authentication.py
│   ├── authorization.py
│   ├── validation.py
│   └── error_handling.py
└── tests/
    ├── integration/     # API integration tests
    └── contract/        # API contract tests
```

### API-Specific Configuration
**Create in project `.clinerules/`**: `api-standards.md`
Include:
- API authentication and authorization strategy
- Rate limiting and throttling configuration
- CORS policy and security headers
- API documentation and testing procedures
- Performance requirements and monitoring

## Request and Response Standards

### Request Format Standards
```python
# Request validation with marshmallow
from marshmallow import Schema, fields, validate

class CreateUserSchema(Schema):
    email = fields.Email(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    role = fields.Str(missing='user', validate=validate.OneOf(['user', 'admin']))

class UpdateUserSchema(Schema):
    first_name = fields.Str(validate=validate.Length(min=1, max=50))
    last_name = fields.Str(validate=validate.Length(min=1, max=50))
    role = fields.Str(validate=validate.OneOf(['user', 'admin']))
```

### Response Format Standards
```python
# Consistent response structure
class APIResponse:
    def __init__(self, data=None, message=None, status_code=200):
        self.data = data
        self.message = message
        self.status_code = status_code
    
    def to_dict(self):
        response = {}
        if self.data is not None:
            response['data'] = self.data
        if self.message:
            response['message'] = self.message
        response['timestamp'] = datetime.utcnow().isoformat()
        return response

# Success response
{
    "data": {
        "id": 123,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "message": "User created successfully",
    "timestamp": "2024-01-15T10:30:00Z"
}

# Error response
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "email": ["This field is required"],
            "password": ["Password must be at least 8 characters"]
        }
    },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Project-Specific Schema Instructions
**Create in project `api/schemas/`**: Schema definition files
Include:
- Request validation schemas for all endpoints
- Response serialization schemas
- Shared data model definitions
- Validation rule documentation
- Schema versioning and migration procedures

## Authentication and Authorization

### Universal Auth Principles
- **Stateless Authentication**: Use JWT tokens or similar stateless mechanisms
- **Role-Based Access Control**: Implement RBAC for authorization
- **Token Expiration**: Use short-lived access tokens with refresh tokens
- **Secure Token Storage**: Never store tokens in localStorage, use httpOnly cookies
- **Multi-Factor Authentication**: Support MFA for sensitive operations

### JWT Implementation Example
```python
import jwt
from datetime import datetime, timedelta
from functools import wraps

class AuthService:
    def __init__(self, secret_key, algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def generate_tokens(self, user_id, roles):
        """Generate access and refresh tokens"""
        now = datetime.utcnow()
        
        # Access token (short-lived)
        access_payload = {
            'user_id': user_id,
            'roles': roles,
            'type': 'access',
            'iat': now,
            'exp': now + timedelta(minutes=15)
        }
        
        # Refresh token (long-lived)
        refresh_payload = {
            'user_id': user_id,
            'type': 'refresh',
            'iat': now,
            'exp': now + timedelta(days=30)
        }
        
        return {
            'access_token': jwt.encode(access_payload, self.secret_key, self.algorithm),
            'refresh_token': jwt.encode(refresh_payload, self.secret_key, self.algorithm),
            'expires_in': 900  # 15 minutes
        }
    
    def verify_token(self, token, token_type='access'):
        """Verify and decode token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get('type') != token_type:
                raise jwt.InvalidTokenError('Invalid token type')
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError('Token has expired')
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError('Invalid token')

def require_auth(roles=None):
    """Decorator for requiring authentication and authorization"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return {'error': 'Authentication required'}, 401
            
            try:
                payload = auth_service.verify_token(token)
                request.user_id = payload['user_id']
                request.user_roles = payload['roles']
                
                # Check roles if specified
                if roles and not any(role in request.user_roles for role in roles):
                    return {'error': 'Insufficient permissions'}, 403
                
                return func(*args, **kwargs)
            except jwt.InvalidTokenError as e:
                return {'error': str(e)}, 401
        
        return wrapper
    return decorator
```

### Project-Specific Auth Instructions
**Create in project `api/middleware/`**: `authentication.md`
Include:
- Authentication provider configuration
- Token management and rotation strategy
- Role and permission definitions
- OAuth/SSO integration if applicable
- Security audit and logging requirements

## Rate Limiting and Throttling

### Universal Rate Limiting Principles
- **Different Limits for Different Users**: Implement tiered rate limiting
- **Multiple Time Windows**: Use various time windows (per minute, hour, day)
- **Graceful Degradation**: Provide meaningful responses when limits are exceeded
- **Bypass Mechanisms**: Allow bypassing limits for internal services
- **Monitoring**: Track rate limit usage and adjust as needed

### Rate Limiting Implementation
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

# Redis-backed rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["1000 per day", "100 per hour"]
)

class CustomRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key, limit, window_seconds):
        """Check if request is within rate limit"""
        current_time = int(time.time())
        window_start = current_time - (current_time % window_seconds)
        
        pipe = self.redis.pipeline()
        pipe.incr(f"{key}:{window_start}")
        pipe.expire(f"{key}:{window_start}", window_seconds)
        results = pipe.execute()
        
        return results[0] <= limit
    
    def get_remaining(self, key, limit, window_seconds):
        """Get remaining requests in current window"""
        current_time = int(time.time())
        window_start = current_time - (current_time % window_seconds)
        current_count = self.redis.get(f"{key}:{window_start}") or 0
        return max(0, limit - int(current_count))

# Usage in routes
@app.route('/api/v1/users')
@limiter.limit("10 per minute")
@require_auth()
def get_users():
    # Implementation
    pass

@app.route('/api/v1/users', methods=['POST'])
@limiter.limit("5 per minute")
@require_auth(roles=['admin'])
def create_user():
    # Implementation
    pass
```

### Project-Specific Rate Limiting Instructions
**Create in project `api/middleware/`**: `rate-limiting.md`
Include:
- Rate limit tiers for different user types
- Endpoint-specific rate limiting rules
- Rate limit monitoring and alerting
- DDoS protection integration
- Rate limit bypass mechanisms for internal services

## Error Handling and Validation

### Universal Error Standards
- **Consistent Error Format**: Use standardized error response structure
- **Meaningful Error Codes**: Provide application-specific error codes
- **Detailed Error Messages**: Include helpful error messages for developers
- **Validation Errors**: Provide field-specific validation error details
- **Error Logging**: Log errors appropriately for debugging

### Error Handling Implementation
```python
from enum import Enum
from marshmallow import ValidationError

class ErrorCode(Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    AUTHORIZATION_FAILED = "AUTHORIZATION_FAILED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

class APIError(Exception):
    def __init__(self, code, message, details=None, status_code=400):
        self.code = code
        self.message = message
        self.details = details
        self.status_code = status_code
        super().__init__(message)

@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        'error': {
            'code': error.code.value,
            'message': error.message,
            'timestamp': datetime.utcnow().isoformat()
        }
    }
    
    if error.details:
        response['error']['details'] = error.details
    
    return jsonify(response), error.status_code

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return handle_api_error(APIError(
        ErrorCode.VALIDATION_ERROR,
        "Invalid input data",
        error.messages,
        400
    ))

@app.errorhandler(404)
def handle_not_found(error):
    return handle_api_error(APIError(
        ErrorCode.RESOURCE_NOT_FOUND,
        "Resource not found",
        status_code=404
    ))
```

### Project-Specific Error Handling Instructions
**Create in project `api/middleware/`**: `error-handling.md`
Include:
- Application-specific error codes and messages
- Error logging and monitoring configuration
- Error response format customization
- Client error handling guidelines
- Error recovery and retry strategies

## API Documentation

### OpenAPI/Swagger Standards
- **Complete Documentation**: Document all endpoints, parameters, and responses
- **Interactive Documentation**: Provide interactive API documentation
- **Code Examples**: Include request/response examples in multiple languages
- **Authentication Documentation**: Clearly document authentication requirements
- **Versioning**: Maintain documentation for all API versions

### OpenAPI Specification Example
```yaml
# api/documentation/openapi.yaml
openapi: 3.0.3
info:
  title: User Management API
  description: API for managing users and authentication
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@company.com

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

security:
  - BearerAuth: []

paths:
  /users:
    get:
      summary: List users
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
    
    post:
      summary: Create user
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/User'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          example: 123
        email:
          type: string
          format: email
          example: user@example.com
        first_name:
          type: string
          example: John
        last_name:
          type: string
          example: Doe
        created_at:
          type: string
          format: date-time
    
    CreateUserRequest:
      type: object
      required: [email, first_name, last_name, password]
      properties:
        email:
          type: string
          format: email
        first_name:
          type: string
          minLength: 1
          maxLength: 50
        last_name:
          type: string
          minLength: 1
          maxLength: 50
        password:
          type: string
          minLength: 8
```

### Project-Specific Documentation Instructions
**Create in project `api/documentation/`**: `documentation-standards.md`
Include:
- API documentation hosting and maintenance procedures
- Documentation update workflow and responsibilities
- Client SDK generation from OpenAPI specs
- API testing and validation procedures
- Documentation versioning and archival

## GraphQL API Standards

### GraphQL Best Practices
- **Schema Design**: Design schemas around business logic, not database structure
- **Query Complexity**: Implement query complexity analysis and limits
- **Caching Strategy**: Implement appropriate caching for GraphQL responses
- **Error Handling**: Use GraphQL error extensions for detailed error information
- **Security**: Implement query depth limiting and field-level authorization

### GraphQL Implementation Example
```python
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude_fields = ('password_hash',)

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(UserType)
    
    def mutate(self, info, email, first_name, last_name, password):
        # Validate input
        if not email or '@' not in email:
            raise GraphQLError("Invalid email address")
        
        # Check permissions
        current_user = get_current_user(info.context)
        if not has_permission(current_user, 'create_user'):
            raise GraphQLError("Insufficient permissions")
        
        # Create user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return CreateUserMutation(user=user)

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    
    def resolve_users(self, info):
        current_user = get_current_user(info.context)
        if not has_permission(current_user, 'read_users'):
            raise GraphQLError("Insufficient permissions")
        return User.query.all()
    
    def resolve_user(self, info, id):
        user = User.query.get(id)
        if not user:
            raise GraphQLError("User not found")
        return user

class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
```

### Project-Specific GraphQL Instructions
**Create in project `api/graphql/`**: `graphql-standards.md`
Include:
- GraphQL schema design patterns
- Query complexity analysis configuration
- Caching strategy for GraphQL responses
- Error handling and logging patterns
- Performance monitoring and optimization

## Real-Time APIs (WebSocket/Socket.IO)

### WebSocket Best Practices
- **Connection Management**: Implement proper connection lifecycle management
- **Authentication**: Authenticate WebSocket connections securely
- **Message Validation**: Validate all incoming messages
- **Rate Limiting**: Implement rate limiting for WebSocket messages
- **Error Handling**: Provide clear error responses for failed operations

### Socket.IO Implementation Example
```python
from flask_socketio import SocketIO, emit, join_room, leave_room
from functools import wraps

socketio = SocketIO(app, cors_allowed_origins="*")

def authenticated_only(f):
    """Decorator to require authentication for Socket.IO events"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not hasattr(request, 'user_id'):
            emit('error', {'message': 'Authentication required'})
            return
        return f(*args, **kwargs)
    return wrapped

@socketio.on('connect')
def handle_connect():
    # Authenticate connection
    token = request.args.get('token')
    if not token:
        return False
    
    try:
        payload = auth_service.verify_token(token)
        request.user_id = payload['user_id']
        request.user_roles = payload['roles']
        
        # Join user-specific room
        join_room(f"user_{request.user_id}")
        
        emit('connected', {'message': 'Connected successfully'})
        logger.info(f"User {request.user_id} connected")
        
    except jwt.InvalidTokenError:
        return False

@socketio.on('disconnect')
def handle_disconnect():
    if hasattr(request, 'user_id'):
        leave_room(f"user_{request.user_id}")
        logger.info(f"User {request.user_id} disconnected")

@socketio.on('join_chat')
@authenticated_only
def handle_join_chat(data):
    chat_id = data.get('chat_id')
    if not chat_id:
        emit('error', {'message': 'chat_id is required'})
        return
    
    # Validate user can join chat
    if not can_user_join_chat(request.user_id, chat_id):
        emit('error', {'message': 'Access denied'})
        return
    
    join_room(f"chat_{chat_id}")
    emit('joined_chat', {'chat_id': chat_id})

@socketio.on('send_message')
@authenticated_only
def handle_send_message(data):
    # Validate message data
    if not data.get('message') or not data.get('chat_id'):
        emit('error', {'message': 'Invalid message data'})
        return
    
    # Process and broadcast message
    message = create_chat_message(
        user_id=request.user_id,
        chat_id=data['chat_id'],
        content=data['message']
    )
    
    socketio.emit('new_message', {
        'id': message.id,
        'user_id': message.user_id,
        'content': message.content,
        'timestamp': message.created_at.isoformat()
    }, room=f"chat_{data['chat_id']}")
```

### Project-Specific Real-Time Instructions
**Create in project `api/realtime/`**: `websocket-standards.md`
Include:
- WebSocket event naming conventions
- Message format and validation standards
- Connection scaling and load balancing
- Real-time data synchronization patterns
- Performance monitoring for real-time features

## API Testing and Quality Assurance

### Testing Strategy
- **Unit Tests**: Test individual API functions and methods
- **Integration Tests**: Test complete API endpoints
- **Contract Tests**: Verify API contracts with consumers
- **Load Tests**: Test API performance under load
- **Security Tests**: Test for common API vulnerabilities

### API Testing Implementation
```python
import pytest
import json
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Create test user and get auth token
    user_data = {
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpassword123'
    }
    
    response = client.post('/api/v1/auth/register', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    token = response.json['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

class TestUserAPI:
    def test_create_user_success(self, client):
        user_data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'password123'
        }
        
        response = client.post('/api/v1/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['data']['email'] == user_data['email']
        assert 'password' not in response.json['data']
    
    def test_create_user_validation_error(self, client):
        invalid_data = {
            'email': 'invalid-email',
            'first_name': '',
            'password': '123'  # Too short
        }
        
        response = client.post('/api/v1/users',
                              data=json.dumps(invalid_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        assert response.json['error']['code'] == 'VALIDATION_ERROR'
        assert 'email' in response.json['error']['details']
    
    def test_get_users_authenticated(self, client, auth_headers):
        response = client.get('/api/v1/users', headers=auth_headers)
        
        assert response.status_code == 200
        assert 'data' in response.json
        assert isinstance(response.json['data'], list)
    
    def test_get_users_unauthenticated(self, client):
        response = client.get('/api/v1/users')
        
        assert response.status_code == 401
        assert response.json['error']['code'] == 'AUTHENTICATION_FAILED'
```

### Project-Specific Testing Instructions
**Create in project `api/tests/`**: `testing-strategy.md`
Include:
- Test coverage requirements and measurement
- Performance testing thresholds and procedures
- Security testing checklist and tools
- API contract testing with consumer teams
- Continuous testing integration in CI/CD

## Quality Checklist

Before deploying API changes, ensure:
- [ ] All endpoints are properly documented in OpenAPI spec
- [ ] Authentication and authorization are implemented correctly
- [ ] Input validation is comprehensive and tested
- [ ] Error handling provides meaningful responses
- [ ] Rate limiting is configured appropriately
- [ ] Security headers and CORS are properly configured
- [ ] API tests cover all critical paths and edge cases
- [ ] Performance requirements are met under load
- [ ] Monitoring and alerting are configured
- [ ] API versioning strategy is followed
- [ ] Breaking changes are properly communicated
- [ ] Client SDKs or documentation are updated
