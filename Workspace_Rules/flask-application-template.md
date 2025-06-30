# Flask Web Application Template

## Flask Application Structure

### Application Factory Pattern
```python
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
```

### Configuration Management
- Use different config classes for development, testing, and production
- Store sensitive information in environment variables
- Use `Flask.config.from_object()` for configuration loading
- Validate required configuration on application startup

## Database Integration

### SQLAlchemy Best Practices
- Use Flask-SQLAlchemy for database operations
- Implement proper migration strategies with Flask-Migrate
- Use database connection pooling for production
- Handle database errors gracefully with proper rollback

### Model Design
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'
```

## API Development

### RESTful API Design
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Implement proper status codes
- Use consistent URL patterns
- Include API versioning strategy

### Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
```

## Security Implementation

### Input Validation
- Validate all user inputs on the server side
- Use Flask-WTF for form validation
- Sanitize data before processing or storage
- Implement proper CSRF protection

### Authentication
- Use Flask-Login for user session management
- Implement secure password hashing
- Use secure session management
- Implement proper logout functionality

## Testing Flask Applications

### Test Configuration
```python
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
```

### Testing Patterns
- Test route handlers and business logic separately
- Use Flask's test client for endpoint testing
- Mock external dependencies in tests
- Test both success and error scenarios

## Deployment Considerations

### Production Settings
- Disable debug mode in production
- Use environment variables for configuration
- Implement proper logging
- Use WSGI server (Gunicorn, uWSGI) for production
- Configure proper error pages
