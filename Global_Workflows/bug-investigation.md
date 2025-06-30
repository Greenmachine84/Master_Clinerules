You are systematically investigating and fixing a bug. Follow this methodical approach to ensure thorough analysis and effective resolution.

## Bug Investigation Process

### 1. Initial Bug Triage

```xml
<ask_followup_question>
<question>What type of issue are we investigating?</question>
<options>["Application Crash/Error", "Performance Issue", "UI/UX Bug", "Data Integrity Problem", "Integration Failure", "Security Vulnerability"]</options>
</ask_followup_question>
```

```xml
<ask_followup_question>
<question>What's the severity and impact of this bug?</question>
<options>["Critical - System down", "High - Major feature broken", "Medium - Feature partially working", "Low - Minor inconvenience"]</options>
</ask_followup_question>
```

### 2. Information Gathering Phase

#### A. Reproduce the Bug
First, understand exactly what's happening:

```xml
<ask_followup_question>
<question>Can you provide the exact steps to reproduce this bug?</question>
<options>["I'll provide steps", "It's intermittent/hard to reproduce", "I need help identifying reproduction steps"]</options>
</ask_followup_question>
```

#### B. Collect Context
Gather all relevant information:
- Error messages and stack traces
- System logs and debug output
- User environment details
- Recent changes or deployments
- Related symptoms or patterns

```xml
<ask_followup_question>
<question>Do you have error logs, stack traces, or debug output to share?</question>
<options>["Yes, I'll share them", "No error messages visible", "I need help finding the logs"]</options>
</ask_followup_question>
```

### 3. Systematic Investigation

#### Step 1: Analyze Error Logs and Stack Traces
If error information is available:
```xml
<read_file>
<path>[log file path]</path>
</read_file>
```

Look for:
- Specific error messages and codes
- Stack trace information
- Timing patterns
- Related errors or warnings

#### Step 2: Examine Relevant Code Components
Based on the error analysis, identify and examine key files:
```xml
<read_file>
<path>[suspected component file]</path>
</read_file>
```

Focus on:
- Functions mentioned in stack traces
- Recent changes in the area
- Input validation and error handling
- Integration points and dependencies

#### Step 3: Check Recent Changes
```xml
<search_files>
<path>.</path>
<regex>git log --oneline -10</regex>
</search_files>
```

Investigate:
- Recent commits that might have introduced the bug
- Changes in related components
- Configuration or dependency updates
- Environment changes

#### Step 4: Analyze Data Flow
Trace the execution path:
```xml
<search_files>
<path>.</path>
<regex>[function_name_from_error]</regex>
<file_pattern>*.*</file_pattern>
</search_files>
```

Examine:
- Input data validation
- Data transformations
- External API calls
- Database operations
- Return value handling

### 4. Hypothesis Formation and Testing

#### A. Develop Hypotheses
Based on investigation, form testable hypotheses about the root cause:

1. **Primary Hypothesis:** Most likely cause based on evidence
2. **Alternative Hypotheses:** Other possible explanations
3. **Edge Case Scenarios:** Less obvious potential causes

#### B. Test Hypotheses
For each hypothesis, design specific tests:

```xml
<ask_followup_question>
<question>Would you like me to create test scenarios to validate our hypotheses?</question>
<options>["Yes, create test cases", "I'll test manually", "Let's proceed with the fix"]</options>
</ask_followup_question>
```

Create:
- Minimal reproduction cases
- Edge case tests
- Data validation tests
- Integration tests

### 5. Root Cause Analysis

#### Identify the Core Issue
Document findings:
- **Root Cause:** The fundamental reason for the bug
- **Contributing Factors:** Conditions that enabled the bug
- **Impact Analysis:** What systems/users are affected
- **Risk Assessment:** Potential for similar issues

#### Trace the Failure Chain
Map out how the bug manifests:
1. **Trigger Condition:** What initiates the problem
2. **Failure Point:** Where the system actually fails
3. **Error Propagation:** How the error spreads through the system
4. **User Impact:** What the user experiences

### 6. Solution Development

#### A. Design the Fix
Develop a comprehensive solution:

**Immediate Fix:**
- Address the specific bug
- Ensure no regression
- Minimal risk approach

**Robust Solution:**
- Prevent similar issues
- Improve error handling
- Add monitoring/logging

#### B. Implementation Strategy
```python
# Example fix structure
def fixed_function(input_data):
    """
    Fixed version with proper error handling and validation
    """
    # Input validation
    if not input_data or not isinstance(input_data, expected_type):
        logger.error(f"Invalid input data: {input_data}")
        return default_safe_value
    
    try:
        # Main logic with error handling
        result = process_data(input_data)
        
        # Result validation
        if not validate_result(result):
            logger.warning(f"Unexpected result format: {result}")
            return fallback_result
            
        return result
        
    except SpecificException as e:
        logger.error(f"Known error in data processing: {e}")
        # Specific error handling
        return handle_specific_error(e)
        
    except Exception as e:
        logger.error(f"Unexpected error in data processing: {e}")
        # Generic error handling
        return safe_fallback_value
```

### 7. Testing and Validation

#### A. Test the Fix
Comprehensive testing approach:

**Unit Tests:**
```python
def test_bug_fix():
    # Test the specific bug scenario
    result = fixed_function(problematic_input)
    assert result == expected_output
    
def test_edge_cases():
    # Test edge cases that might cause similar issues
    pass
    
def test_error_handling():
    # Test error conditions are handled properly
    pass
```

**Integration Tests:**
- Test the fix in the full system context
- Verify no side effects or regressions
- Test with realistic data volumes and conditions

#### B. Regression Testing
```xml
<ask_followup_question>
<question>Should I create a comprehensive test suite to prevent this type of bug in the future?</question>
<options>["Yes, create prevention tests", "Just test the immediate fix", "I'll handle testing separately"]</options>
</ask_followup_question>
```

### 8. Documentation and Prevention

#### A. Document the Fix
Create comprehensive documentation:

**Bug Report:**
- Description of the issue
- Root cause analysis
- Fix implementation details
- Testing performed

**Knowledge Base Entry:**
- Common symptoms
- Diagnostic steps
- Prevention measures
- Related issues to watch for

#### B. Prevention Measures
Implement safeguards:
- Add monitoring and alerting
- Improve error logging
- Add validation checks
- Update coding standards
- Create preventive tests

### 9. Follow-up and Monitoring

#### A. Post-Fix Monitoring
```xml
<ask_followup_question>
<question>Would you like me to set up monitoring to ensure this bug doesn't recur?</question>
<options>["Yes, create monitoring plan", "I'll monitor manually", "No additional monitoring needed"]</options>
</ask_followup_question>
```

Monitor:
- Error rates in the affected area
- Performance metrics
- User feedback and reports
- Related system health indicators

#### B. Team Communication
Communicate findings:
- Share root cause analysis with team
- Update development practices if needed
- Document lessons learned
- Update bug prevention guidelines

## Bug Investigation Checklist

- [ ] Reproduced the bug reliably
- [ ] Gathered all relevant error information
- [ ] Analyzed recent changes and deployments
- [ ] Identified root cause with evidence
- [ ] Developed comprehensive fix
- [ ] Tested fix thoroughly
- [ ] Implemented prevention measures
- [ ] Documented findings and solution
- [ ] Set up monitoring for recurrence
- [ ] Communicated lessons learned

## Best Practices for Bug Investigation

1. **Stay Methodical:** Follow the process even under pressure
2. **Document Everything:** Keep detailed notes of investigation steps
3. **Test Hypotheses:** Don't assume - verify with evidence
4. **Think Prevention:** Fix not just the symptom but the underlying cause
5. **Communicate Clearly:** Keep stakeholders informed of progress
6. **Learn and Improve:** Use each bug as a learning opportunity
