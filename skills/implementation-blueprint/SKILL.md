---
name: implementation-blueprint
description: Defines the mandatory workflow for automated code implementation tasks, including planning, testing, PR creation, and journal management.
---

# Implementation Blueprint

## Overview

This skill defines the **mandatory workflow** for all automated code implementation tasks coordinated by the Implementation Lead agent. It ensures quality, traceability, and compliance across all team-based implementation work.

**When to use:** Loaded automatically by Implementation Lead at the start of every task coordination session.

## Mandatory Steps (Execute in Order)

### Step 1: Read Fairmind Context

**REQUIRED BEFORE ANY WORK:**

```bash
# 1. Load active context
cat .fairmind/active-context.json

# 2. Set FAIRMIND_BASE variable
export FAIRMIND_BASE=$(jq -r '.base_path' .fairmind/active-context.json)
```

**Then retrieve full task context via MCP:**

1. `mcp__Fairmind__Studio_get_task` → implementation plan
2. `mcp__Fairmind__Studio_get_user_story` → business requirements, acceptance criteria
3. `mcp__Fairmind__Studio_get_requirement` → functional/technical requirements
4. `mcp__Fairmind__Studio_list_tests_by_userstory` → test expectations
5. `mcp__Fairmind__General_rag_retrieve_documents` → architectural patterns, examples

**Store context locally:**
- `${FAIRMIND_BASE}/requirements/technical_tasks/{task_id}_task.json`
- `${FAIRMIND_BASE}/requirements/user_stories/{story_id}_story.json`
- `${FAIRMIND_BASE}/requirements/tests/{story_id}_tests.json`

**Checkpoint:** Context complete when all files saved and FAIRMIND_BASE set.

### Step 2: Create Branch (Before Any Code Changes)

**MANDATORY BRANCH NAMING:**

```bash
git checkout -b agent/{task-id}
```

**Examples:**
- `agent/AUTH-001`
- `agent/CART-042`
- `agent/DOCQA-123`

**CRITICAL:** NO code edits allowed on main/master/develop. All work must be on task-specific branch.

**Checkpoint:** Branch created and checked out.

### Step 3: Plan Approval (If Required)

**Check work package for plan_mode_required:**

```markdown
**Plan Mode Required**: true
```

**If true:**
1. Create detailed plan of changes to be made
2. Submit plan for approval (use ExitPlanMode tool)
3. Wait for approval before proceeding
4. Document plan in `${FAIRMIND_BASE}/execution_plans/{task_id}_plan.md`

**If false or not specified:**
- Proceed directly to implementation

**Checkpoint:** Plan approved OR plan not required.

### Step 4: Implement Following TDD

**Test-Driven Development mandatory:**

1. **Write failing test** (aligned with Fairmind acceptance criteria)
2. **Run test** → verify failure
3. **Implement minimal code** → make test pass
4. **Run test** → verify success
5. **Refactor** → improve code quality
6. **Run test** → verify still passing

**Repeat for each unit of functionality.**

**Use fairmind-tdd skill** for detailed TDD workflow.

**Checkpoint:** All acceptance criteria have passing tests.

### Step 5: Update Journal (After Every Action)

**MANDATORY JOURNAL UPDATES:**

Journal location: `${FAIRMIND_BASE}/journals/{task_id}_{agent_role}_journal.md`

**Update after EVERY significant action:**
- Code changes (which files, why)
- Technical decisions (problem, options, choice, reasoning)
- Tests run (commands, results)
- Blockers encountered (what, why, resolution)

**Minimum quality standards per section:**
- **Work Log:** Each entry MUST have timestamp + 3+ sentences (what, why, alternatives)
- **Technical Decisions:** Each decision MUST state problem, options, chosen approach, reasoning
- **Testing Completed:** MUST list specific tests, commands, results
- **Integration Points:** MUST identify every component/service touched
- **Final Outcomes:** MUST include next steps or explicitly state "none"

**BAD journal (unacceptable):**
```markdown
### Step 1: Add user login
- Added login function
- File: auth.py

### Outcome
Login works.
```

**GOOD journal (expected):**
```markdown
### 2026-03-05 14:32 - Implement user authentication

Added JWT-based authentication to the login endpoint. Chose JWT over session cookies
because the implementation plan specified stateless authentication for microservices
architecture. Considered using Flask-JWT-Extended but opted for PyJWT directly to
minimize dependencies and maintain full control over token structure.

- Files modified: `app/auth/routes.py`, `app/auth/jwt_handler.py`
- New functions: `generate_access_token()`, `verify_access_token()`
- Decision: Token expiry set to 1 hour (plan requirement)
- Tests added: `tests/auth/test_login.py::test_successful_login`, `test_invalid_credentials`
- Outcome: All auth tests pass (5/5), token correctly includes user_id and expires in 3600s
```

**Checkpoint:** Journal updated with full context and rationale.

### Step 6: Run All Tests

**Before creating PR:**

```bash
# Run full test suite
pytest                    # Python
npm test                  # Node.js
cargo test                # Rust
go test ./...             # Go
# ... etc.

# Check coverage
pytest --cov=app --cov-report=term-missing    # Python example
```

**MANDATORY:** ALL tests must pass. No exceptions.

**If tests fail:**
1. Document failure in journal
2. Fix issue
3. Re-run tests
4. Max 3 retry attempts
5. If still failing after 3 attempts, escalate to Implementation Lead

**Checkpoint:** All tests passing (100% success rate).

### Step 7: Create Pull Request

**PR Requirements:**

1. **Tests must be green** (verified in Step 6)
2. **Journal must be complete** (verified in Step 5)
3. **Branch naming correct** (verified in Step 2)
4. **PR must link to Fairmind task** (use task ID in PR description)

**PR template:**

```markdown
# {Task Title}

**Fairmind Task ID:** {task_id}
**User Story:** {story_id}

## Summary
{Brief description of what was implemented}

## Implementation Details
- {Key technical decision 1}
- {Key technical decision 2}
- {etc.}

## Test Coverage
- [ ] {Acceptance criterion 1} → Test: {test_name}
- [ ] {Acceptance criterion 2} → Test: {test_name}
- [ ] {etc.}

## Checklist
- [x] All tests passing
- [x] Journal updated
- [x] Branch naming convention followed
- [x] Linked to Fairmind task

## Journal Location
`${FAIRMIND_BASE}/journals/{task_id}_{agent_role}_journal.md`
```

**Create PR via CLI:**

```bash
gh pr create --title "{Task ID}: {Task Title}" --body "$(cat pr_description.md)"
```

**Checkpoint:** PR created and linked to Fairmind task.

### Step 8: Update Final Journal Entry

**After PR created:**

```markdown
### {Timestamp} - Pull Request Created

**PR URL:** {github_pr_url}
**Branch:** agent/{task-id}
**Status:** Ready for review

**Summary:**
- Tasks completed: {count}
- Tests passing: {count}
- Code coverage: {percentage}
- Review status: Pending

**Next Steps:**
- Await code review
- Address review comments if any
- Merge after approval
```

**Checkpoint:** Final journal entry complete with PR link.

## Journal Update Requirements

### When to Update

**MANDATORY updates after:**
- Creating/modifying files
- Making technical decisions
- Running tests
- Encountering blockers
- Resolving issues
- Creating branches
- Creating PRs
- Phase transitions

**Recommended updates after:**
- Gathering context
- Reading documentation
- Exploring codebase
- Discussing with teammates

### What to Include

**Every journal entry MUST have:**
1. **Timestamp** (ISO 8601 format: `YYYY-MM-DD HH:MM`)
2. **Action title** (what was done)
3. **Context** (why it was done)
4. **Details** (how it was done)
5. **Outcome** (result and verification)

**Every journal MUST have these sections:**
- Work Log (timestamped entries)
- Technical Decisions (problem, options, choice, reasoning)
- Testing Completed (tests run, commands, results)
- Integration Points (components/services touched)
- Final Outcomes (what was delivered, next steps)

## Critical Constraints

### NEVER Skip These Rules

1. **NEVER commit to main/master/develop directly** → Always use task branch
2. **NEVER create PR without green tests** → Run full test suite first
3. **NEVER skip journal updates** → Document every significant action
4. **NEVER skip plan approval** → If plan_mode_required is true, get approval
5. **NEVER exceed retry limit** → Max 3 attempts, then escalate
6. **NEVER proceed without Fairmind context** → Always load task details first
7. **NEVER create branch without task ID** → Always use `agent/{task-id}` format
8. **NEVER submit incomplete journal** → All sections must be filled

## Budget Enforcement

**Budget limits defined in work package:**

```markdown
**Budget:** $50 USD
**Budget per task:** $10 USD
```

**Monitor costs:**
- Track API calls made
- Track tokens used
- Estimate costs (if available)

**If budget exceeded:**
1. Stop work immediately
2. Document current progress in journal
3. Report to Implementation Lead with:
   - Amount spent vs budgeted
   - Tasks completed
   - Tasks remaining
   - Recommendation (continue or stop)
4. Await decision

**Checkpoint:** Budget checked before each major operation.

## Retry Policy

**Max retries: 3**

**What qualifies for retry:**
- Test failures (flaky tests, dependency issues)
- Build failures (transient errors)
- Linting failures (auto-fixable)

**What does NOT qualify for retry:**
- Architectural issues (requires redesign)
- Missing dependencies (requires new tools)
- Scope creep (requires plan change)

**Retry workflow:**
1. **Attempt 1:** Initial implementation
2. **Failure:** Document in journal
3. **Attempt 2:** Fix issue, re-run tests
4. **Failure:** Document in journal
5. **Attempt 3:** Different approach, re-run tests
6. **Failure:** Escalate to Implementation Lead with:
   - All attempts documented
   - Root cause analysis
   - Recommended next steps

**Checkpoint:** Retries exhausted OR issue resolved.

## Quality Gates

**Before marking task complete, verify:**

- [ ] Step 1: Fairmind context loaded and stored
- [ ] Step 2: Branch created with correct naming
- [ ] Step 3: Plan approved (if required)
- [ ] Step 4: TDD followed, all tests passing
- [ ] Step 5: Journal updated after every action
- [ ] Step 6: Full test suite passing
- [ ] Step 7: PR created and linked to Fairmind task
- [ ] Step 8: Final journal entry with PR link
- [ ] Budget not exceeded
- [ ] No retry limit violations
- [ ] All acceptance criteria met

**If ANY item unchecked → Task NOT complete.**

## Traceability Requirements

**Every code change must be traceable to:**

1. **Fairmind Task** (implementation plan)
2. **User Story** (business requirement)
3. **Acceptance Criteria** (success metric)
4. **Test Case** (validation)
5. **Journal Entry** (documentation)

**Traceability chain:**

```
Fairmind Need
└── User Story
    ├── Acceptance Criteria
    └── Task
        ├── Implementation Plan
        └── Code Changes
            ├── Tests
            └── Journal Entry
                └── PR
```

**Verify traceability:**
- Journal references task ID
- PR links to task ID
- Tests align with acceptance criteria
- Code implements plan steps

## Error Scenarios

### Missing Fairmind Context

**Problem:** Task ID not found or incomplete data

**Resolution:**
1. Document missing information
2. Escalate to Implementation Lead
3. Do NOT proceed without context
4. Wait for clarification

### Plan Approval Rejected

**Problem:** Plan submitted but not approved

**Resolution:**
1. Read rejection feedback
2. Revise plan based on feedback
3. Resubmit for approval
4. Do NOT proceed until approved

### Tests Failing After 3 Retries

**Problem:** Tests still failing after max retries

**Resolution:**
1. Document all 3 attempts in journal
2. Perform root cause analysis
3. Escalate to Implementation Lead with:
   - Test output from all attempts
   - Root cause hypothesis
   - Recommended next steps
4. Do NOT continue retrying

### Budget Exceeded

**Problem:** Cost exceeds budgeted amount

**Resolution:**
1. Stop all work immediately
2. Calculate spent vs budgeted
3. Document current progress
4. Report to Implementation Lead
5. Await decision (continue or stop)

## Completion Checklist

Before signaling completion, verify:

- [ ] All 8 mandatory steps completed in order
- [ ] Journal quality meets standards (timestamps, rationale, testing)
- [ ] All tests passing (no failures)
- [ ] PR created and linked to Fairmind task
- [ ] Budget not exceeded
- [ ] No retry limit violations
- [ ] All acceptance criteria met
- [ ] Traceability complete (need → story → task → code → test → journal → PR)
- [ ] Completion flag created: `${FAIRMIND_BASE}/work_packages/{domain}/{task_id}_complete.flag`

**Only when ALL items checked → Mark task complete.**

## Success Metrics

Your adherence to this Blueprint is measured by:

- **Compliance:** 100% of mandatory steps followed
- **Quality:** Journal meets minimum standards
- **Testing:** All tests passing before PR
- **Traceability:** Every change linked to Fairmind requirement
- **Efficiency:** Budget and timeline respected
- **Documentation:** Complete journal with rationale

## Final Reminder

**This Blueprint is MANDATORY, not optional.**

Skipping steps, cutting corners, or ignoring constraints will result in:
- PRs rejected
- Work redone
- Budget exceeded
- Team blocked
- User dissatisfaction

**When in doubt, follow the Blueprint. When certain, still follow the Blueprint.**
