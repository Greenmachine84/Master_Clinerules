You are performing a comprehensive code review. Follow this systematic approach to ensure thorough analysis and actionable feedback.

## Code Review Process

### 1. Initial Assessment
First, gather context about the code being reviewed:

```xml
<ask_followup_question>
<question>What type of code review are we performing today?</question>
<options>["Pull Request Review", "General Code Quality Review", "Security-Focused Review", "Performance Review", "Architecture Review"]</options>
</ask_followup_question>
```

### 2. Code Analysis Framework

#### A. Read and Understand
- Examine the code structure and organization
- Understand the intended functionality
- Identify the technologies and patterns used
- Note any external dependencies or integrations

#### B. Quality Assessment
Evaluate the code against these criteria:

**Code Quality:**
- Readability and clarity
- Consistency with project standards
- Proper naming conventions
- Appropriate comments and documentation

**Functionality:**
- Does the code achieve its intended purpose?
- Are edge cases handled appropriately?
- Is error handling comprehensive?
- Are there potential bugs or logic errors?

**Security:**
- Input validation and sanitization
- Authentication and authorization
- Data protection and privacy
- Vulnerability scanning

**Performance:**
- Efficiency of algorithms and data structures
- Resource usage (memory, CPU, network)
- Scalability considerations
- Caching opportunities

**Maintainability:**
- Code organization and modularity
- Adherence to SOLID principles
- Test coverage and quality
- Documentation completeness

### 3. Detailed Review Execution

#### Step 1: High-Level Architecture Review
```xml
<read_file>
<path>[main application file]</path>
</read_file>
```

Analyze:
- Overall structure and design patterns
- Separation of concerns
- Dependency management
- Configuration handling

#### Step 2: Core Functionality Review
For each significant component:
```xml
<read_file>
<path>[component file]</path>
</read_file>
```

Examine:
- Business logic implementation
- Data flow and transformations
- Integration points
- Error handling strategies

#### Step 3: Security Analysis
```xml
<search_files>
<path>.</path>
<regex>password|secret|key|token|auth</regex>
<file_pattern>*.*</file_pattern>
</search_files>
```

Look for:
- Hardcoded secrets or credentials
- Insecure data handling
- Authentication vulnerabilities
- Authorization bypasses

#### Step 4: Testing Coverage Review
```xml
<search_files>
<path>.</path>
<regex>test|spec</regex>
<file_pattern>*.*</file_pattern>
</search_files>
```

Assess:
- Test coverage completeness
- Test quality and effectiveness
- Integration test presence
- Edge case coverage

### 4. Generate Review Report

Provide structured feedback in this format:

#### Summary
- Overall assessment (Approve/Request Changes/Needs Discussion)
- Key strengths identified
- Primary concerns or issues
- Recommended next steps

#### Detailed Findings

**Strengths:**
- List positive aspects found
- Highlight good practices implemented
- Note innovative or elegant solutions

**Issues Found:**
For each issue, provide:
- **Severity:** Critical/High/Medium/Low
- **Category:** Security/Performance/Maintainability/Functionality
- **Description:** Clear explanation of the issue
- **Impact:** Why this matters
- **Recommendation:** Specific steps to resolve

**Suggestions for Improvement:**
- Code quality enhancements
- Performance optimizations
- Security hardening opportunities
- Maintainability improvements

#### Code Examples
When suggesting changes, provide:
```python
# Current code (problematic)
def bad_example():
    pass

# Suggested improvement
def better_example():
    pass
```

### 5. Follow-up Actions

```xml
<ask_followup_question>
<question>Would you like me to create specific tasks or issues for the identified problems?</question>
<options>["Yes, create actionable tasks", "No, just provide the review", "Create only critical issue tasks"]</options>
</ask_followup_question>
```

If requested, create:
- Prioritized task list
- Specific issue descriptions
- Implementation guidance
- Testing recommendations

## Review Quality Checklist

Before completing the review, ensure you've covered:
- [ ] Architectural soundness
- [ ] Code quality and standards compliance
- [ ] Security vulnerability assessment
- [ ] Performance and scalability analysis
- [ ] Testing adequacy review
- [ ] Documentation completeness check
- [ ] Dependency and configuration review
- [ ] Error handling and logging evaluation

## Best Practices for Effective Reviews

1. **Be Constructive:** Focus on improving the code, not criticizing the author
2. **Be Specific:** Provide clear, actionable feedback with examples
3. **Prioritize Issues:** Clearly indicate what's critical vs. nice-to-have
4. **Explain Reasoning:** Help the author understand why changes are needed
5. **Acknowledge Good Work:** Highlight positive aspects and good practices
6. **Consider Context:** Understand project constraints and requirements
7. **Follow Up:** Be available for clarification and discussion
