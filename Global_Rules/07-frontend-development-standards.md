# Frontend Development Standards

## Universal Frontend Principles

### Code Quality Standards
- **Component-Based Architecture**: Build reusable, modular components
- **Separation of Concerns**: Keep logic, styling, and markup properly separated
- **Responsive Design First**: Design for mobile-first, scale up to desktop
- **Accessibility Standards**: Follow WCAG guidelines for inclusive design
- **Performance by Design**: Optimize for loading speed and runtime performance

### JavaScript/TypeScript Standards
- **Modern ES6+ Syntax**: Use arrow functions, destructuring, async/await
- **Type Safety**: Use TypeScript for complex applications, JSDoc for simpler ones
- **Error Handling**: Implement proper try-catch blocks and user feedback
- **Code Formatting**: Use Prettier and ESLint for consistent formatting
- **Module Organization**: Use ES6 modules with clear import/export patterns

```javascript
// Preferred patterns
const ApiService = {
  async fetchData(endpoint) {
    try {
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API fetch failed:', error);
      throw error; // Re-throw for component handling
    }
  }
};
```

## Project-Specific Implementation Instructions

### For React Projects
**Create in project `.clinerules/`**: `react-standards.md`
Include:
- Component naming conventions (PascalCase for components)
- Hook usage patterns and custom hook creation
- State management approach (Context API, Redux, Zustand)
- Props validation with PropTypes or TypeScript interfaces
- Testing strategy with React Testing Library

### For Vue.js Projects  
**Create in project `.clinerules/`**: `vue-standards.md`
Include:
- Component structure (template, script, style blocks)
- Composition API vs Options API usage guidelines
- State management with Vuex/Pinia patterns
- Component prop validation and events
- Testing with Vue Test Utils

### For Vanilla JavaScript Projects
**Create in project `.clinerules/`**: `vanilla-js-standards.md`
Include:
- DOM manipulation best practices
- Event handling patterns
- Module bundling strategy (Webpack, Rollup, Vite)
- Browser compatibility requirements
- Polyfill strategy for older browsers

## CSS/Styling Standards

### Universal Styling Principles
- **BEM Methodology**: Use Block-Element-Modifier naming convention
- **Mobile-First Design**: Start with mobile styles, enhance for larger screens
- **CSS Custom Properties**: Use CSS variables for theming and consistency
- **Component Scoping**: Avoid global styles, scope to components
- **Performance**: Minimize CSS bundle size and unused styles

```css
/* BEM Example */
.card {
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card__title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.card--featured {
  border: 2px solid var(--primary-color);
}
```

### Project-Specific Styling Instructions
**Create in project root**: `style-guide.md` or **in `.clinerules/`**: `styling-standards.md`
Include:
- Color palette and design tokens
- Typography scale and font choices
- Spacing system (4px, 8px, 16px grid)
- Component style patterns
- Animation and transition guidelines
- Dark mode / light mode strategy

## Build Process and Tooling

### Universal Build Principles
- **Hot Module Replacement**: Enable fast development feedback
- **Code Splitting**: Split bundles for optimal loading
- **Asset Optimization**: Compress images, minify CSS/JS
- **Source Maps**: Enable debugging in development
- **Environment Configuration**: Separate dev/staging/production configs

### Project-Specific Tooling Instructions
**Create in project root**: `build-configuration.md`
Include:
- Bundler choice and configuration (Webpack, Vite, Rollup)
- Development server setup and proxy configuration
- Linting and formatting tool configuration
- Testing framework setup and configuration
- Deployment build process and optimization

## API Integration Standards

### Frontend API Patterns
```javascript
// Centralized API client pattern
class ApiClient {
  constructor(baseURL, defaultHeaders = {}) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      ...defaultHeaders
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: { ...this.defaultHeaders, ...options.headers },
      ...options
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(response.status, errorData.message || 'Request failed');
      }
      
      return await response.json();
    } catch (error) {
      if (error instanceof ApiError) throw error;
      throw new ApiError(0, 'Network error or request failed');
    }
  }
}

class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}
```

### Project-Specific API Integration
**Create in project `.clinerules/`**: `api-integration.md`
Include:
- Backend API endpoint documentation
- Authentication token handling strategy
- Error handling and user feedback patterns
- Loading states and optimistic updates
- Caching strategy for API responses

## State Management Standards

### Universal State Principles
- **Single Source of Truth**: Centralize application state
- **Predictable Updates**: Use clear patterns for state changes
- **Immutable Updates**: Avoid direct state mutation
- **Local vs Global State**: Use local state when possible, global when needed
- **State Normalization**: Structure complex state efficiently

### Project-Specific State Management
**Create in project `.clinerules/`**: `state-management.md`
Include:
- State management library choice (Redux, Zustand, Pinia, Context API)
- State structure and organization patterns
- Action/mutation naming conventions
- Async state handling patterns
- Dev tools integration and debugging

## Performance Optimization

### Universal Performance Standards
- **Bundle Size Monitoring**: Track and limit JavaScript bundle sizes
- **Lazy Loading**: Load components and routes on demand
- **Image Optimization**: Use appropriate formats and sizes
- **Caching Strategy**: Implement effective browser and application caching
- **Critical Path Optimization**: Prioritize above-the-fold content

### Project-Specific Performance Instructions
**Create in project `.clinerules/`**: `performance-standards.md`
Include:
- Performance budget targets (bundle size, load time)
- Monitoring and measurement tools setup
- Critical performance metrics to track
- Optimization strategies for specific features
- Performance testing procedures

## Testing Standards

### Universal Testing Principles
- **Test Pyramid**: More unit tests, fewer integration/E2E tests
- **User-Centric Testing**: Test behavior, not implementation details
- **Accessibility Testing**: Include a11y testing in test suites
- **Visual Testing**: Test UI components across browsers/devices
- **Performance Testing**: Include performance regression testing

### Project-Specific Testing Instructions
**Create in project `.clinerules/`**: `frontend-testing.md`
Include:
- Testing framework choice (Jest, Vitest, Cypress, Playwright)
- Component testing patterns and utilities
- Mock strategies for API calls and external dependencies
- E2E testing scenarios and setup
- Testing CI/CD integration

## Security Standards

### Frontend Security Principles
- **Input Sanitization**: Sanitize user inputs before display
- **XSS Prevention**: Use framework protections, validate dynamic content
- **CSRF Protection**: Implement proper token handling
- **Secure Headers**: Configure Content Security Policy
- **Dependency Security**: Regularly audit and update dependencies

### Project-Specific Security Instructions
**Create in project `.clinerules/`**: `frontend-security.md`
Include:
- Content Security Policy configuration
- Authentication flow implementation
- Session management on frontend
- Sensitive data handling patterns
- Security testing procedures

## Browser Compatibility

### Universal Compatibility Standards
- **Progressive Enhancement**: Ensure core functionality works everywhere
- **Graceful Degradation**: Handle missing features elegantly
- **Polyfill Strategy**: Include necessary polyfills for target browsers
- **Feature Detection**: Use feature detection over browser detection
- **Testing Matrix**: Test on supported browsers and devices

### Project-Specific Compatibility Instructions
**Create in project `.clinerules/`**: `browser-support.md`
Include:
- Supported browser versions and market share thresholds
- Polyfill requirements and loading strategy
- Feature compatibility matrix
- Testing procedures for target browsers
- Fallback strategies for unsupported features

## Development Workflow

### Universal Workflow Principles
- **Component-Driven Development**: Build and test components in isolation
- **Style Guide Integration**: Maintain living style guides/component libraries
- **Code Review Focus**: Review for accessibility, performance, and maintainability
- **Continuous Integration**: Automate testing and quality checks
- **Documentation**: Maintain component documentation and usage examples

### Project-Specific Workflow Instructions
**Create in project `.clinerules/`**: `frontend-workflow.md`
Include:
- Local development setup and commands
- Code review checklist and standards
- Deployment process and environments
- Design system integration and updates
- Collaboration tools and processes

## Quality Checklist

Before deploying frontend code, ensure:
- [ ] Code follows project coding standards
- [ ] Components are responsive and accessible
- [ ] Performance budgets are met
- [ ] Cross-browser testing completed
- [ ] Security best practices implemented
- [ ] Tests pass and coverage meets requirements
- [ ] Documentation updated
- [ ] Design system guidelines followed
- [ ] User experience tested and validated
- [ ] Error handling and loading states implemented
