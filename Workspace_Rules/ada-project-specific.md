# ADA Application Project Guidelines

## Project Overview
This is a Python Flask application with Socket.IO for real-time communication, featuring an AI assistant (ADA) with voice capabilities, weather integration, and web search functionality.

## Architecture Standards

### Core Components
- **Flask Backend**: Main application server with Socket.IO for WebSocket communication
- **ADA AI Engine**: Core AI functionality in `ADA_Online.py` and `ADA_Live_API.py`
- **Real-time Communication**: Flask-SocketIO for client-server communication
- **Environment Management**: Python virtual environment with specific dependencies

### File Structure Guidelines
- `app.py`: Main Flask application and Socket.IO server
- `ADA_Online.py`: Core ADA AI functionality
- `ADA_Live_API.py`: Live API integrations and real-time features
- `requirements.txt`: Dependency management
- `.env`: Environment variables (never commit to version control)
- `venv/`: Virtual environment (never commit to version control)

## Development Standards

### Python Code Style
- Follow PEP 8 conventions
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Maintain consistent indentation (4 spaces)
- Use type hints where appropriate

### Error Handling
- Always implement proper try-catch blocks for external API calls
- Log errors appropriately with context
- Provide graceful fallbacks for API failures
- Use Flask's logging system consistently

### Socket.IO Best Practices
- Always emit acknowledgments for important events
- Handle connection and disconnection events properly
- Implement proper error handling for Socket.IO events
- Use meaningful event names that describe their purpose

## API Integration Guidelines

### External Services
- **Google Gemini AI**: Primary AI model integration
- **Weather APIs**: Weather information retrieval
- **Google Maps**: Location-based services
- **Web Search**: Information retrieval capabilities

### API Key Management
- Store all API keys in `.env` file
- Never hardcode API keys in source code
- Use `os.getenv()` with sensible defaults
- Validate API key presence on application startup

## Testing and Debugging

### Local Development
- Always run in virtual environment
- Use `python app.py` or appropriate startup command
- Monitor console output for errors and warnings
- Test Socket.IO connections with browser developer tools

### Environment Setup
- Ensure `.env` file is properly configured
- Verify all required packages are installed
- Check Python version compatibility
- Validate API key functionality before deployment

## Security Considerations

### Environment Variables
- Never commit `.env` files to version control
- Use secure, random secret keys for Flask sessions
- Validate and sanitize all user inputs
- Implement proper CORS settings for production

### Data Handling
- Sanitize user inputs before processing
- Implement rate limiting for API calls
- Log security-relevant events appropriately
- Handle sensitive data with appropriate care

## Performance Guidelines

### Resource Management
- Implement proper cleanup for threads and async operations
- Monitor memory usage, especially for long-running processes
- Use connection pooling for database operations if applicable
- Implement proper shutdown procedures

### Async Operations
- Use proper async/await patterns
- Handle threading carefully with Flask-SocketIO
- Implement proper error handling for async operations
- Monitor for potential deadlocks or race conditions

## Communication Preferences for ADA Development

### Code Review Focus
- Prioritize Socket.IO connection stability
- Ensure AI response quality and consistency
- Validate API integration robustness
- Check for proper error handling in real-time features

### Development Workflow
- Test voice features thoroughly across different browsers
- Validate weather API responses for accuracy
- Ensure web search functionality works reliably
- Monitor AI token usage and costs during development
