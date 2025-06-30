You are implementing a new feature following best practices for design, development, and delivery. Use this comprehensive workflow to ensure high-quality, maintainable feature development.

## Feature Development Process

### 1. Requirements Analysis and Planning

#### A. Understand the Feature Requirements
```xml
<ask_followup_question>
<question>What type of feature are we developing?</question>
<options>["New User Interface Component", "API Endpoint/Service", "Data Processing Feature", "Integration with External Service", "Performance/Security Enhancement", "Other"]</options>
</ask_followup_question>
```

```xml
<ask_followup_question>
<question>Do you have detailed requirements or user stories for this feature?</question>
<options>["Yes, I have detailed requirements", "I have basic requirements that need elaboration", "I need help defining the requirements"]</options>
</ask_followup_question>
```

#### B. Requirements Gathering and Clarification
If requirements need elaboration, gather:

**Functional Requirements:**
- What should the feature do?
- Who will use it?
- How should it behave in different scenarios?
- What are the success criteria?

**Non-Functional Requirements:**
- Performance expectations
- Security considerations
- Scalability requirements
- Compatibility constraints

**Acceptance Criteria:**
- Specific, testable conditions
- Edge cases and error scenarios
- User experience expectations
- Integration requirements

### 2. Architecture and Design Phase

#### A. Analyze Current System
```xml
<read_file>
<path>[main application file]</path>
</read_file>
```

Understand:
- Current architecture patterns
- Existing similar features
- Integration points
- Data models and schemas

#### B. Design the Feature Architecture
```xml
<ask_followup_question>
<question>Should I create a technical design document for this feature?</question>
<options>["Yes, create full design doc", "Just outline the approach", "Proceed with implementation"]</options>
</ask_followup_question>
```

Design considerations:
- **Component Architecture:** How will the feature fit into existing structure?
- **Data Flow:** How will data move through the system?
- **API Design:** What interfaces will be exposed or consumed?
- **Database Schema:** What data storage changes are needed?
- **Security Model:** What authentication/authorization is required?
- **Error Handling:** How will errors be managed and reported?

#### C. Create Implementation Plan
Break down the feature into manageable tasks:

1. **Database/Schema Changes** (if needed)
2. **Backend Implementation**
3. **API Development** (if applicable)
4. **Frontend Implementation** (if applicable)
5. **Integration Points**
6. **Testing Implementation**
7. **Documentation**

### 3. Implementation Phase

#### A. Set Up Development Environment
Ensure proper setup:
```xml
<search_files>
<path>.</path>
<regex>requirements|package\.json|Gemfile</regex>
<file_pattern>*.*</file_pattern>
</search_files>
```

- Verify all dependencies are installed
- Check development environment configuration
- Ensure testing framework is ready
- Set up any new development tools needed

#### B. Database/Schema Implementation (if needed)
```python
# Example migration/schema change
def upgrade():
    """Add new tables/columns for the feature"""
    # Create new tables
    op.create_table('feature_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feature_field', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add new columns to existing tables
    op.add_column('existing_table', 
        sa.Column('new_field', sa.String(100), nullable=True))
```

#### C. Backend/Core Logic Implementation
Implement the core feature logic:

```python
# Example feature implementation structure
class FeatureService:
    """Service class for the new feature"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def create_feature_item(self, data: FeatureData) -> FeatureResult:
        """
        Main feature functionality
        
        Args:
            data: Input data for the feature
            
        Returns:
            FeatureResult: Result of the operation
            
        Raises:
            FeatureValidationError: If input data is invalid
            FeatureProcessingError: If processing fails
        """
        try:
            # Input validation
            self._validate_input(data)
            
            # Core processing
            processed_data = self._process_data(data)
            
            # Persistence
            result = self._save_data(processed_data)
            
            # Success logging
            self.logger.info(f"Feature item created successfully: {result.id}")
            
            return result
            
        except ValidationError as e:
            self.logger.error(f"Validation error in feature creation: {e}")
            raise FeatureValidationError(str(e))
            
        except Exception as e:
            self.logger.error(f"Unexpected error in feature creation: {e}")
            raise FeatureProcessingError(f"Failed to create feature item: {str(e)}")
    
    def _validate_input(self, data: FeatureData) -> None:
        """Validate input data"""
        if not data:
            raise ValidationError("Input data is required")
        
        # Add specific validation logic
        pass
    
    def _process_data(self, data: FeatureData) -> ProcessedData:
        """Process the feature data"""
        # Implement core business logic
        pass
    
    def _save_data(self, data: ProcessedData) -> FeatureResult:
        """Save processed data"""
        # Implement persistence logic
        pass
```

#### D. API Implementation (if applicable)
```python
# Example API endpoint implementation
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

feature_bp = Blueprint('feature', __name__, url_prefix='/api/feature')

@feature_bp.route('/', methods=['POST'])
def create_feature():
    """Create a new feature item"""
    try:
        # Request validation
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Schema validation
        feature_data = FeatureSchema().load(data)
        
        # Service call
        result = feature_service.create_feature_item(feature_data)
        
        # Response serialization
        return jsonify(FeatureResultSchema().dump(result)), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
        
    except FeatureValidationError as e:
        return jsonify({'error': str(e)}), 400
        
    except FeatureProcessingError as e:
        return jsonify({'error': str(e)}), 500
        
    except Exception as e:
        logger.error(f"Unexpected error in feature API: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@feature_bp.route('/<int:feature_id>', methods=['GET'])
def get_feature(feature_id):
    """Get a specific feature item"""
    try:
        result = feature_service.get_feature_item(feature_id)
        if not result:
            return jsonify({'error': 'Feature not found'}), 404
        
        return jsonify(FeatureResultSchema().dump(result)), 200
        
    except Exception as e:
        logger.error(f"Error retrieving feature {feature_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500
```

#### E. Frontend Implementation (if applicable)
```javascript
// Example frontend component
class FeatureComponent {
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        document.getElementById('create-feature-btn')
            .addEventListener('click', () => this.createFeature());
    }
    
    async createFeature() {
        try {
            const formData = this.getFormData();
            
            // Validate form data
            if (!this.validateFormData(formData)) {
                this.showError('Please fill in all required fields');
                return;
            }
            
            // Show loading state
            this.setLoading(true);
            
            // API call
            const result = await this.apiClient.post('/api/feature', formData);
            
            // Handle success
            this.handleSuccess(result);
            
        } catch (error) {
            this.handleError(error);
        } finally {
            this.setLoading(false);
        }
    }
    
    validateFormData(data) {
        // Implement client-side validation
        return data && data.requiredField && data.requiredField.trim() !== '';
    }
    
    handleSuccess(result) {
        this.showSuccess('Feature created successfully');
        this.resetForm();
        this.refreshFeatureList();
    }
    
    handleError(error) {
        const message = error.response?.data?.error || 'An error occurred';
        this.showError(message);
    }
}
```

### 4. Testing Implementation

#### A. Unit Tests
```python
import pytest
from unittest.mock import Mock, patch

class TestFeatureService:
    
    def setup_method(self):
        self.config = Mock()
        self.feature_service = FeatureService(self.config)
    
    def test_create_feature_item_success(self):
        """Test successful feature item creation"""
        # Arrange
        input_data = FeatureData(field1="value1", field2="value2")
        expected_result = FeatureResult(id=1, status="created")
        
        # Act
        result = self.feature_service.create_feature_item(input_data)
        
        # Assert
        assert result.id == expected_result.id
        assert result.status == expected_result.status
    
    def test_create_feature_item_validation_error(self):
        """Test feature creation with invalid input"""
        # Arrange
        invalid_data = FeatureData(field1="", field2=None)
        
        # Act & Assert
        with pytest.raises(FeatureValidationError):
            self.feature_service.create_feature_item(invalid_data)
    
    def test_create_feature_item_processing_error(self):
        """Test feature creation with processing failure"""
        # Arrange
        input_data = FeatureData(field1="value1", field2="value2")
        
        with patch.object(self.feature_service, '_process_data', 
                         side_effect=Exception("Processing failed")):
            # Act & Assert
            with pytest.raises(FeatureProcessingError):
                self.feature_service.create_feature_item(input_data)
```

#### B. Integration Tests
```python
class TestFeatureAPI:
    
    def test_create_feature_endpoint_success(self, client):
        """Test feature creation API endpoint"""
        # Arrange
        feature_data = {
            'field1': 'test value',
            'field2': 'another value'
        }
        
        # Act
        response = client.post('/api/feature/', 
                              json=feature_data,
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['status'] == 'created'
    
    def test_create_feature_endpoint_validation_error(self, client):
        """Test feature creation with invalid data"""
        # Arrange
        invalid_data = {'field1': ''}  # Missing required field2
        
        # Act
        response = client.post('/api/feature/', 
                              json=invalid_data,
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
```

### 5. Documentation

#### A. Code Documentation
Ensure comprehensive documentation:
- Function/method docstrings
- Class documentation
- API endpoint documentation
- Configuration options

#### B. User Documentation
```xml
<ask_followup_question>
<question>Should I create user-facing documentation for this feature?</question>
<options>["Yes, create user guide", "Just technical documentation", "Documentation not needed"]</options>
</ask_followup_question>
```

If user documentation is needed:
- Feature overview and benefits
- Step-by-step usage instructions
- Common use cases and examples
- Troubleshooting guide

### 6. Quality Assurance and Review

#### A. Code Review Checklist
Before submitting for review:
- [ ] Code follows project conventions
- [ ] All edge cases are handled
- [ ] Error handling is comprehensive
- [ ] Tests provide adequate coverage
- [ ] Documentation is complete
- [ ] Security considerations addressed
- [ ] Performance impact assessed

#### B. Manual Testing
```xml
<ask_followup_question>
<question>Should I create a manual testing checklist for this feature?</question>
<options>["Yes, create test scenarios", "Automated tests are sufficient", "I'll handle manual testing"]</options>
</ask_followup_question>
```

### 7. Deployment and Monitoring

#### A. Deployment Preparation
- Database migrations (if needed)
- Configuration updates
- Feature flags or gradual rollout plan
- Rollback procedures

#### B. Monitoring Setup
```xml
<ask_followup_question>
<question>Should I set up monitoring and alerting for this feature?</question>
<options>["Yes, create monitoring plan", "Basic error tracking only", "No additional monitoring needed"]</options>
</ask_followup_question>
```

If monitoring is needed:
- Feature usage metrics
- Error rates and types
- Performance metrics
- User satisfaction indicators

### 8. Post-Deployment Follow-up

#### A. Validation
- Verify feature works as expected in production
- Monitor initial usage patterns
- Check for any deployment-related issues

#### B. Feedback Collection
- Gather user feedback
- Monitor support requests
- Analyze usage analytics
- Identify improvement opportunities

## Feature Development Checklist

- [ ] Requirements clearly defined and understood
- [ ] Technical design documented
- [ ] Implementation follows best practices
- [ ] Comprehensive testing completed
- [ ] Documentation created
- [ ] Code review passed
- [ ] Security review completed
- [ ] Performance impact assessed
- [ ] Deployment plan prepared
- [ ] Monitoring and alerting configured
- [ ] Post-deployment validation completed

## Best Practices for Feature Development

1. **Start with Requirements:** Ensure clear understanding before coding
2. **Design First:** Plan the architecture and approach before implementing
3. **Test Early and Often:** Write tests as you develop, not after
4. **Document Continuously:** Keep documentation current with code changes
5. **Security by Design:** Consider security implications from the start
6. **Performance Awareness:** Monitor and optimize performance impact
7. **User-Centric:** Keep the end user experience in mind throughout development
8. **Iterative Improvement:** Plan for feedback and continuous enhancement
