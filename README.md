# Master Cline Rules Organization

This folder contains all Cline rules organized into two categories that align with Cline's actual structure.

## Folder Structure

### 📁 Global_Rules
Rules that apply to **ALL projects** across your development work. These should be copied to Cline's global rules location: `C:\Users\devin\Documents\Cline\Rules\`

**Core Standards:**
- `01-universal-development-standards.md` - Core programming principles, Git workflow, testing philosophy
- `02-communication-preferences.md` - How you prefer Cline to communicate and respond
- `03-security-privacy-standards.md` - Security and privacy standards for all projects
- `04-python-development-standards.md` - Python-specific standards and patterns
- `05-performance-optimization-standards.md` - Database optimization, caching, async processing
- `06-security-standards.md` - Security implementation and best practices

**Full Stack Development Standards:**
- `07-frontend-development-standards.md` - JavaScript/TypeScript, React/Vue, CSS, API integration
- `08-database-design-standards.md` - Schema design, migrations, indexing, monitoring
- `09-devops-deployment-standards.md` - CI/CD, containerization, infrastructure as code
- `10-api-design-standards.md` - REST/GraphQL/WebSocket APIs, authentication, documentation

**AI Development Standards:**
- `11-ethical-ai-development-standards.md` - Values integration, bias prevention, explainable AI
- `12-ai-safety-robustness-standards.md` - Safety protocols, uncertainty quantification, monitoring
- `13-ai-character-auditing-preservation-standards.md` - Character integrity, evolution governance, cross-AI validation
- `14-ai-lifecycle-management-standards.md` - Complete AI development lifecycle with ethical gates
- `15-ai-psychological-safety-standards.md` - Mental health safeguards and relationship health monitoring

### 📁 Global_Workflows
Universal workflows that apply to all development projects across different technologies and domains.

**Available Workflows:**
- `feature-development.md` - Comprehensive 8-phase feature development process
- `full-stack-integration-workflow.md` - Frontend/backend integration procedures
- `ai-system-testing-workflow.md` - Comprehensive AI system testing methodology
- `comprehensive-ai-risk-assessment-workflow.md` - Multi-dimensional AI risk assessment and self-evaluation
- `api-development-workflow.md` - RESTful API development workflow
- `python-testing-workflow.md` - Python testing strategy with pytest
- `project-onboarding-workflow.md` - New team member onboarding
- `monitoring-observability-workflow.md` - Application monitoring setup
- `database-migration-workflow.md` - Safe database migration procedures
- `bug-investigation.md` - Systematic debugging and issue resolution
- `code-review.md` - Code review process and standards

### 📁 Global_Scripts
Scripts that can be used to enforce and audit the global rules across all projects.

**Available Scripts:**
- `audit_python_project.py` - A Python script to audit a project for compliance with dependency, and code quality standards.

### 📁 Workspace_Rules
Project-specific rules that go in each project's `.clinerules` folder. Choose the appropriate template(s) for each project.

**Template Files:**
- `python-development-template.md` - Python-specific standards and patterns
- `flask-application-template.md` - Flask web application best practices
- `ai-application-template.md` - AI application development patterns
- `advanced-ai-system-template.md` - Advanced AI systems with ethics, safety, and learning
- `full-stack-integration-template.md` - Full stack application standards
- `ada-project-specific.md` - Specific rules for your ADA project

### 📁 Workspace_Workflows
Project-specific workflows that combine global workflows with project-specific procedures.

## How to Use

### Setting Up Global Rules
Copy all files from `Global_Rules/` to your Cline global rules directory:
```powershell
Copy-Item "c:\Users\devin\Documents\GitHub\Master_Clinerules\Global_Rules\*" "C:\Users\devin\Documents\Cline\Rules\"
```

### Setting Up Workspace Rules for ADA Project
Copy relevant files to your project's `.clinerules` folder:
```powershell
# For your ADA project
Copy-Item "c:\Users\devin\Documents\GitHub\Master_Clinerules\Workspace_Rules\ada-project-specific.md" "c:\Users\devin\Documents\GitHub\ada_app\server\.clinerules\"
Copy-Item "c:\Users\devin\Documents\GitHub\Master_Clinerules\Workspace_Rules\python-development-template.md" "c:\Users\devin\Documents\GitHub\ada_app\server\.clinerules\"
Copy-Item "c:\Users\devin\Documents\GitHub\Master_Clinerules\Workspace_Rules\flask-application-template.md" "c:\Users\devin\Documents\GitHub\ada_app\server\.clinerules\"
Copy-Item "c:\Users\devin\Documents\GitHub\Master_Clinerules\Workspace_Rules\ai-application-template.md" "c:\Users\devin\Documents\GitHub\ada_app\server\.clinerules\"
```

### For Future Projects
1. Copy appropriate templates from `Workspace_Rules/` to your new project's `.clinerules/` folder
2. Customize the templates for project-specific requirements
3. Global rules remain the same across all projects

## Rule Categories Explained

### Global Rules (Universal)
- Apply to every conversation with Cline
- Stored in Cline's global settings
- Include communication style, universal coding standards, security principles

### Workspace Rules (Project-Specific)
- Apply only when working in that specific project
- Stored in project's `.clinerules/` folder
- Include project architecture, specific frameworks, project requirements

This organization ensures Cline always has the right context and guidance for any project while maintaining consistency across all your development work.
