# Python Development Standards Template

## Python Code Quality

### Style and Formatting
- Follow PEP 8 style guide strictly
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter standard)
- Use meaningful, descriptive names for variables, functions, and classes
- Prefer explicit over implicit code

### Type Hints and Documentation
- Include type hints for all function parameters and return values
- Write comprehensive docstrings using Google or NumPy style
- Document complex logic with inline comments
- Include examples in docstrings for public APIs

### Import Management
- Group imports: standard library, third-party, local imports
- Use absolute imports over relative imports
- Sort imports alphabetically within groups
- Remove unused imports

## Error Handling Patterns

### Exception Handling Strategy
```python
# Preferred pattern for external API calls
try:
    result = external_api_call()
    return result
except SpecificException as e:
    logger.error(f"Specific error occurred: {e}")
    # Handle specific case
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Graceful fallback
    return default_value
```

### Logging Standards
- Use Python's `logging` module, not `print()` statements
- Include appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Include context in log messages (user ID, request ID, etc.)
- Structure log messages for easy parsing

## Testing Requirements

### Unit Testing
- Write tests for all core functionality
- Use pytest for testing framework
- Mock external API calls in tests
- Achieve minimum 80% code coverage

### Test Structure
```python
def test_function_with_valid_input_returns_expected_result():
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_result
```

## Virtual Environment Management
- Always use virtual environments for development
- Pin dependency versions in requirements.txt
- Use requirements-dev.txt for development dependencies
- Document Python version requirements

## Performance Considerations
- Use generators for large datasets
- Implement proper cleanup for resources
- Monitor memory usage for long-running processes
- Profile code before optimizing
