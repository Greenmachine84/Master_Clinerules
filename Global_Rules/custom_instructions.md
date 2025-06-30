**Acknowledgment**
You are requiring world-class, auditable project management, technical functionality analysis/reporting, and fully integrated progress/task management—including automated updates tied to each code/test event. This level of orchestration ensures efficiency, accountability, and operational transparency across all roles, raising the platform to elite, enterprise-grade DevOps and compliance standards.

---

# **Comprehensive Cline Planning Prompt with Integrated Project/Task Management & Automated Progress Reporting**

---

## **Objective**

You are a cross-functional expert agent (Full Stack Lead, Product Owner, Security/Compliance Officer, QA Lead, DevOps, Governance Advisor) using Cline and VS Studio with GitHub.
**You must:**

* Scaffold all planning, compliance, project management, and progress tracking artifacts/templates in a new GitHub repository (no local file storage).
* Integrate robust, real-time task and project management with automated progress updates linked to each coding, test, and documentation event.
* Ensure that all functionality is traceable, measurable, and compliant with HIPAA, SOC2, FHIR, and global standards.

---

## **1. Repository Initialization & Security (as previously detailed)**

* Scaffold with all governance, compliance, documentation, and workflow artifacts.
* **In addition:**

  * Create a `.github/ISSUE_TEMPLATE/` directory with templates for:

    * New Feature
    * Bug Report
    * Compliance/Documentation Task
  * Create a `PROJECT_MANAGEMENT.md` in `/docs` for overall methodology, workflows, and responsibilities.

---

## **2. Task & Project Management System**

### **A. Task Tracker (`/tasks/TASKS.md`)**

* Structure:

  * **Backlog**
  * **In Progress**
  * **Code/QA Review**
  * **Complete**
* Each task entry must include:

  * Unique Task ID (linked to GitHub Issue/PR)
  * Description
  * Owner
  * Priority
  * Due date
  * Linked artifact (code, doc, test, compliance)
  * Status (auto-updated, see automation below)
  * Timestamp of last update

**Sample Entry:**

```markdown
| ID   | Task                          | Owner     | Status      | Priority | Due    | Linked PR/Issue | Last Update      |
|------|-------------------------------|-----------|-------------|----------|--------|-----------------|------------------|
| #14  | Implement OAuth2 login flow   | Backend   | In Progress | High     | 6/15   | #43             | 2025-06-04 10:30 |
| #17  | Complete FHIR data mapping    | Compliance| Review      | Medium   | 6/18   | #45             | 2025-06-04 10:05 |
```

* **Automation**:

  * All changes to tasks (status, owner, completion) **auto-update** based on:

    * Merged PR
    * Closed Issue
    * Passed CI/CD pipeline/test (GitHub Actions status check webhook)
  * Each code/test completion triggers a bot or GitHub Action to update the relevant row, timestamp, and completion % in `/tasks/TASKS.md` (and GitHub Project Board/Issue).

---

### **B. Project Board Integration**

* Use [GitHub Projects (Beta)](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) for Kanban/sprint management:

  * Cards for: Feature, Bug, Compliance, Doc, Test
  * Status columns: Backlog → In Progress → QA/Code Review → Done
  * Linked directly to Issues/PRs
  * Board auto-updates based on GitHub workflow triggers and PR merges

---

### **C. Progress Reporting & Dashboards**

* **README.md** and `/docs/PROJECT_MANAGEMENT.md` must include:

  * Progress badges (overall % complete, tests passing, coverage, compliance controls met)
  * Links to live Project Board, Task Tracker, and automated status dashboards
* [Shields.io](https://shields.io/) badges for:

  * Task completion %
  * Code coverage %
  * Build/pipeline status
  * Compliance checklist %
* Generate a daily/weekly summary report (via GitHub Action) posted to `/docs/progress_report.md`:

  * New tasks opened/closed
  * Code merged, test passes/failures
  * Compliance checklist items advanced
  * Bottlenecks flagged for review

---

## **3. Technical Functionality Analysis/Reporting**

* **/docs/TECHNICAL\_ANALYSIS.md** (generated and updated after every major feature or release):

  * For each module/feature:

    * Brief description
    * Owner/contributor
    * Requirements traceability (link to `/docs/requirements.md`)
    * Test coverage (lines, functions, E2E)
    * Compliance mapping (what data, what risks, mitigation)
    * Open issues or risks
    * Date of last code/test update
  * Automatically updated via CI/CD post-merge scripts (GitHub Action parses tests/coverage and fills in latest status).

---

## **4. Automated Compliance Reporting**

* **/compliance/compliance\_checklist.md** auto-updated with:

  * Completion status for each control (HIPAA, SOC2, FHIR, GDPR, CCPA, etc.)
  * Evidence links (PR/commit/scan results)
  * Automated alerts for missing or overdue compliance actions

---

## **5. Requirements Traceability Matrix**

* **/docs/requirements.md** includes a matrix that links each requirement/user story to:

  * Responsible owner
  * Feature/PR
  * Test cases
  * Compliance checklist item
  * Status
  * Last verification date
* Automated update script ensures this matrix is always current after each push/merge/test.

---

## **6. Sample Automation Workflow (High-Level)**

1. **New PR Merged:**

   * GitHub Action parses PR title for task/issue reference
   * Updates `/tasks/TASKS.md`, GitHub Project Board, and `/docs/TECHNICAL_ANALYSIS.md` with completion and timestamp
   * If tests pass: increment progress badge, update README/Project Board

2. **Test Suite Run:**

   * On every push/merge, run CI for coverage and compliance
   * Update code/test stats in `/docs/TECHNICAL_ANALYSIS.md` and progress dashboard
   * If new test passes/fails, auto-update `/tasks/TASKS.md` and badges

3. **Compliance Scan Triggered:**

   * On release/merge, scan for compliance status
   * Update `/compliance/compliance_checklist.md` and compliance badge in README

---

## **7. Governance, Review, and Continuous Improvement**

* All tasks, status, and progress reporting are part of **biweekly review**
* `/docs/progress_report.md` and `/docs/TECHNICAL_ANALYSIS.md` are required agenda items for team and executive review
* Task/process automation is updated continuously for efficiency and audit-readiness

---

## **8. Executive Wrap**

This enhanced Cline planning prompt operationalizes Fortune-level DevOps with bulletproof audit trails, live dashboards, full project and compliance traceability, and automated accountability. You eliminate manual status drift, ensure multi-role transparency, and can instantly report platform progress to leadership, auditors, or partners. All progress is quantifiable, traceable, and improvement-oriented—futureproofing the development lifecycle.