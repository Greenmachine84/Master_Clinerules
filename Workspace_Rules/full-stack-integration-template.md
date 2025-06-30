# Full Stack Integration Template

## Project Overview
This template provides standards for full stack applications with integrated frontend and backend components, focusing on seamless data flow and user experience.

## Architecture Standards

### Technology Stack Guidelines
**Create in project `.clinerules/`**: `tech-stack.md`
Document your chosen technologies:
- **Frontend Framework**: React, Vue.js, Angular, or vanilla JavaScript
- **Backend Framework**: Flask, Django, Express.js, or FastAPI
- **Database**: PostgreSQL, MySQL, MongoDB, or SQLite
- **Real-time Communication**: Socket.IO, WebSockets, or Server-Sent Events
- **State Management**: Redux, Zustand, Pinia, or Context API
- **Authentication**: JWT, OAuth, or session-based auth

### Project Structure
```
project-root/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── utils/
│   │   └── types/
│   ├── public/
│   ├── package.json
│   └── .env.example
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── __init__.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── shared/
│   ├── types/
│   └── constants/
├── deployment/
│   ├── docker/
│   ├── scripts/
│   └── config/
└── docs/
    ├── api/
    ├── setup/
    └── deployment/
```

## Development Standards

### API Integration Patterns
**Create in project `.clinerules/`**: `api-integration.md`
Define your API integration approach:
- **API Base URL Configuration**: Environment-specific API endpoints
- **Request/Response Formats**: Standardized data structures
- **Error Handling**: Consistent error response handling
- **Authentication Flow**: Token management and refresh strategies
- **Caching Strategy**: Client-side and server-side caching rules

### State Management Strategy
**Create in project `.clinerules/`**: `state-management.md`
Document your state management approach:
- **Global vs Local State**: Guidelines for when to use each
- **State Structure**: How to organize application state
- **Action Patterns**: Naming conventions and async handling
- **State Persistence**: Which state to persist and how
- **Real-time Synchronization**: How to handle live updates

### Component Architecture
**Create in project `.clinerules/`**: `component-standards.md`
Establish component development patterns:
- **Component Naming**: Consistent naming conventions
- **Props Interface**: TypeScript interfaces for component props
- **State Management**: When to use local vs global state
- **Error Boundaries**: Error handling in components
- **Testing Patterns**: Component testing strategies

## Data Flow Standards

### Frontend-Backend Communication
- **API Endpoints**: RESTful or GraphQL API design
- **Data Validation**: Client-side and server-side validation
- **Optimistic Updates**: When and how to implement
- **Error Recovery**: Retry mechanisms and fallback strategies
- **Loading States**: User feedback during async operations

### Real-time Features
**Create in project `.clinerules/`**: `realtime-standards.md`
If your application includes real-time features:
- **WebSocket Management**: Connection lifecycle and reconnection
- **Event Naming**: Consistent event naming conventions
- **Message Validation**: Validate real-time messages
- **Authentication**: Secure WebSocket connections
- **Scaling Considerations**: How real-time features scale

## Security Implementation

### Authentication and Authorization
**Create in project `.clinerules/`**: `auth-implementation.md`
Define your authentication strategy:
- **Token Management**: Storage, refresh, and expiration
- **Route Protection**: Frontend route guards and backend middleware
- **Role-Based Access**: Permission checking patterns
- **Session Management**: User session handling
- **Logout Procedures**: Secure logout implementation

### Data Security
- **Input Sanitization**: Both frontend and backend validation
- **API Security**: Rate limiting, CORS, and headers
- **Sensitive Data**: Handling of passwords, tokens, and PII
- **HTTPS Enforcement**: SSL/TLS configuration
- **Security Headers**: Content Security Policy and others

## Performance Optimization

### Frontend Performance
**Create in project `.clinerules/`**: `frontend-performance.md`
Optimization strategies for your frontend:
- **Bundle Optimization**: Code splitting and lazy loading
- **Asset Optimization**: Image and resource compression
- **Caching Strategy**: Browser caching and service workers
- **Rendering Optimization**: Virtual scrolling, memoization
- **Performance Monitoring**: Metrics and alerting

### Backend Performance
**Create in project `.clinerules/`**: `backend-performance.md`
Backend optimization guidelines:
- **Database Optimization**: Query optimization and indexing
- **Caching Layer**: Redis or in-memory caching
- **API Response Time**: Target response times and monitoring
- **Resource Management**: Memory and CPU optimization
- **Scalability Planning**: Horizontal scaling strategies

## Testing Strategy

### Frontend Testing
**Create in project `.clinerules/`**: `frontend-testing.md`
Frontend testing approach:
- **Unit Testing**: Component and utility function tests
- **Integration Testing**: API integration and user flow tests
- **E2E Testing**: End-to-end user journey tests
- **Visual Testing**: Screenshot and visual regression tests
- **Performance Testing**: Frontend performance benchmarks

### Backend Testing
**Create in project `.clinerules/`**: `backend-testing.md`
Backend testing standards:
- **Unit Testing**: Function and class tests
- **Integration Testing**: Database and API tests
- **Contract Testing**: API contract validation
- **Load Testing**: Performance under load
- **Security Testing**: Vulnerability and penetration tests

### Full Stack Testing
**Create in project `.clinerules/`**: `integration-testing.md`
End-to-end testing strategy:
- **User Journey Tests**: Complete workflow testing
- **Cross-browser Testing**: Compatibility testing
- **Mobile Responsiveness**: Mobile device testing
- **Real-time Feature Testing**: WebSocket and real-time tests
- **Error Scenario Testing**: Error handling validation

## Deployment and DevOps

### Environment Management
**Create in project `.clinerules/`**: `environment-config.md`
Environment-specific configurations:
- **Development Environment**: Local development setup
- **Staging Environment**: Pre-production testing
- **Production Environment**: Live application configuration
- **Environment Variables**: Secure configuration management
- **Database Configurations**: Environment-specific database settings

### CI/CD Pipeline
**Create in project `.clinerules/`**: `cicd-config.md`
Continuous integration and deployment:
- **Build Process**: Frontend and backend build steps
- **Testing Pipeline**: Automated test execution
- **Deployment Strategy**: Blue-green, rolling, or canary deployment
- **Rollback Procedures**: Quick rollback mechanisms
- **Monitoring Integration**: Post-deployment monitoring

### Monitoring and Observability
**Create in project `.clinerules/`**: `monitoring-setup.md`
Application monitoring strategy:
- **Application Metrics**: Performance and usage metrics
- **Error Tracking**: Error monitoring and alerting
- **Log Aggregation**: Centralized logging setup
- **Health Checks**: Application health monitoring
- **User Analytics**: User behavior tracking

## Documentation Standards

### API Documentation
**Create in project `docs/api/`**: API documentation files
- **Endpoint Documentation**: Complete API reference
- **Authentication Guide**: Auth implementation details
- **Error Codes**: Comprehensive error code reference
- **SDK Examples**: Client library usage examples
- **Postman Collections**: API testing collections

### Developer Documentation
**Create in project `docs/`**: Development documentation
- **Setup Guide**: Local development environment setup
- **Architecture Overview**: System design and component relationships
- **Coding Standards**: Project-specific coding guidelines
- **Troubleshooting**: Common issues and solutions
- **Contributing Guide**: Guidelines for new developers

## Quality Assurance

### Code Quality Standards
**Create in project `.clinerules/`**: `code-quality.md`
Code quality enforcement:
- **Linting Configuration**: ESLint, Prettier, and code formatters
- **Type Safety**: TypeScript configuration and usage
- **Code Reviews**: Review process and checklist
- **Git Workflow**: Branch naming and commit conventions
- **Pre-commit Hooks**: Automated quality checks

### Performance Standards
**Create in project `.clinerules/`**: `performance-targets.md`
Performance benchmarks and targets:
- **Page Load Time**: Target load times for different pages
- **API Response Time**: Maximum acceptable response times
- **Bundle Size**: JavaScript bundle size limits
- **Lighthouse Scores**: Performance, accessibility, SEO targets
- **Database Query Performance**: Query execution time limits

## Development Workflow

### Local Development
**Create in project `docs/setup/`**: `local-development.md`
Local development procedures:
- **Environment Setup**: Required tools and dependencies
- **Database Setup**: Local database configuration
- **Service Integration**: External service configuration
- **Hot Reload**: Development server configuration
- **Debugging Setup**: Debugging tools and configuration

### Team Collaboration
**Create in project `.clinerules/`**: `collaboration.md`
Team collaboration guidelines:
- **Communication Channels**: How team communicates
- **Issue Tracking**: Bug and feature tracking process
- **Knowledge Sharing**: Documentation and knowledge transfer
- **Code Review Process**: Review workflow and standards
- **Release Planning**: Sprint planning and release cycles

## Security Checklist

Before deploying full stack applications, ensure:
- [ ] Authentication and authorization implemented correctly
- [ ] Input validation on both frontend and backend
- [ ] HTTPS enforced in production
- [ ] Security headers configured properly
- [ ] Sensitive data encrypted and secured
- [ ] API rate limiting implemented
- [ ] CORS configured appropriately
- [ ] Dependencies regularly updated and scanned
- [ ] Security testing included in CI/CD
- [ ] Error messages don't expose sensitive information

## Performance Checklist

Optimize full stack application performance:
- [ ] Frontend bundle size optimized
- [ ] Images and assets compressed
- [ ] Database queries optimized with proper indexing
- [ ] Caching implemented at appropriate levels
- [ ] CDN configured for static assets
- [ ] Lazy loading implemented for large components
- [ ] API responses optimized and paginated
- [ ] Performance monitoring and alerting configured
- [ ] Load testing completed with acceptable results
- [ ] Memory leaks identified and resolved

## Maintenance and Updates

### Regular Maintenance Tasks
**Create in project `.clinerules/`**: `maintenance-procedures.md`
Ongoing maintenance guidelines:
- **Dependency Updates**: Regular security and feature updates
- **Database Maintenance**: Index optimization and cleanup
- **Performance Monitoring**: Regular performance reviews
- **Security Audits**: Periodic security assessments
- **Backup Verification**: Regular backup testing

### Feature Development Process
**Create in project `.clinerules/`**: `feature-development.md`
New feature development workflow:
- **Requirements Analysis**: Feature specification and planning
- **Design and Architecture**: Technical design documentation
- **Implementation**: Development and testing procedures
- **Code Review**: Peer review and approval process
- **Deployment**: Feature rollout and monitoring
