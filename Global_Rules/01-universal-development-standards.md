# Universal Development Standards

## Core Programming Principles

### Code Quality Standards
- **Readability First**: Code is read more often than it's written
- **Simplicity**: Prefer simple, clear solutions over clever complexity
- **Consistency**: Maintain consistent patterns throughout projects
- **Documentation**: Document why, not just what

### Security Best Practices
- **Input Validation**: Always validate and sanitize user inputs
- **Secret Management**: Never hardcode secrets or API keys
- **Least Privilege**: Grant minimum necessary permissions
- **Regular Updates**: Keep dependencies and systems updated

### Version Control Standards
- **Meaningful Commits**: Write clear, descriptive commit messages
- **Atomic Commits**: One logical change per commit
- **Branch Strategy**: Use feature branches for development
- **Code Reviews**: Always review code before merging

## Git Workflow Standards

### Branch Management
- **Main Branch Protection**: Never commit directly to main/master
- **Feature Branches**: Use descriptive branch names like `feature/user-authentication` or `fix/socket-timeout`
- **Branch Naming Convention**: `type/description` where type is feature, fix, refactor, docs, test
- **Short-lived Branches**: Keep feature branches small and merge frequently

### Commit Message Standards
```
type(scope): brief description

Detailed explanation of what changed and why

- Include bullet points for multiple changes
- Reference issue numbers: Fixes #123
- Use imperative mood: "Add feature" not "Added feature"
```

### Commit Types
- **feat**: New features
- **fix**: Bug fixes
- **refactor**: Code restructuring without behavior changes
- **docs**: Documentation updates
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

## Universal Testing Philosophy
- **Test Early**: Write tests as you develop, not after
- **Test Thoroughly**: Cover happy path, edge cases, and error conditions
- **Test Realistically**: Use realistic data and scenarios
- **Automate Testing**: Implement automated testing where possible

## Documentation Standards
- **Keep It Current**: Update documentation with code changes
- **User-Focused**: Write for the audience who will use it
- **Examples**: Include practical examples and use cases
- **Structure**: Organize documentation logically and consistently

## Error Handling Philosophy
- **Fail Fast**: Detect and report errors early
- **Provide Context**: Include relevant information in error messages
- **Graceful Degradation**: Design systems to handle failures gracefully
- **Log Appropriately**: Balance useful information with noise

## Performance Principles
- **Measure First**: Profile before optimizing
- **Optimize Bottlenecks**: Focus on areas with biggest impact
- **Consider Trade-offs**: Balance performance with maintainability
- **Cache Wisely**: Use caching appropriately, not everywhere
