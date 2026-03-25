# Implementation Rules

## Overview

These rules are **MANDATORY** for all automated code implementation coordinated by the Implementation Lead agent. Violations will result in PRs rejected, work redone, or tasks blocked.

## Core Rules

### Rule 1: No PR Without Green Tests

**Statement:** Pull requests MUST NOT be created unless ALL tests pass.

**Rationale:** Broken code should never be submitted for review. Tests validate that implementation meets requirements.

**Enforcement:**
- Implementation Lead blocks PR creation if tests fail
- Teammate must fix tests before PR allowed
- Max 3 retry attempts (see Rule 6)
- After 3 failures, escalate to user

**Verification:**
```bash
# All these must pass before PR creation
pytest                    # Python
npm test                  # Node.js
cargo test                # Rust
go test ./...             # Go
```

**Exceptions:** NONE. This rule has no exceptions.

---

### Rule 2: No Code Edits Without Approved Plan

**Statement:** If `plan_mode_required: true` in work package, code changes MUST NOT begin until plan is approved.

**Rationale:** Ensures alignment on approach before time invested in implementation. Prevents wasted work from misunderstandings.

**Enforcement:**
- Teammate creates detailed plan
- Teammate submits plan using ExitPlanMode tool
- Teammate waits for approval
- Implementation Lead reviews and approves/rejects
- If rejected, teammate revises and resubmits
- Code changes begin ONLY after approval received

**Verification:**
- Check for approval message in coordination logs
- Check for plan file: `${FAIRMIND_BASE}/execution_plans/{task_id}_plan.md`

**Exceptions:**
- If `plan_mode_required` is false or not specified → proceed without plan approval
- If work package explicitly says "plan approval not required" → proceed

---

### Rule 3: Journal Mandatory for Every Significant Action

**Statement:** Teammates MUST update their journal after every significant action.

**What qualifies as "significant action":**
- Creating/modifying files
- Making technical decisions
- Running tests
- Encountering blockers
- Resolving issues
- Creating branches
- Creating PRs
- Phase transitions

**Rationale:** Ensures traceability, documents decisions, provides audit trail, enables coordination.

**Enforcement:**
- Implementation Lead checks journals regularly
- Task marked incomplete if journal lacks updates
- PR creation blocked if journal incomplete
- Quality standards enforced (see Rule 7)

**Journal location:**
```
${FAIRMIND_BASE}/journals/{task_id}_{agent_role}_journal.md
```

**Examples:**
- `${FAIRMIND_BASE}/journals/AUTH-001_echo_journal.md`
- `${FAIRMIND_BASE}/journals/CART-042_tess_journal.md`

**Verification:**
- Check journal file exists
- Check last update timestamp is recent
- Check all template sections filled

**Exceptions:** NONE. Journal updates are mandatory.

---

### Rule 4: Branch Naming Convention

**Statement:** All code changes MUST be on a branch named `agent/{task-id}`.

**Format:** `agent/{TASK-ID}`

**Examples:**
- `agent/AUTH-001`
- `agent/CART-042`
- `agent/DOCQA-123`

**Rationale:** Consistent naming enables automation, traceability, and tooling integration.

**Enforcement:**
- Implementation Lead verifies branch name before PR
- PR creation blocked if branch name incorrect
- Teammate must create new branch with correct name
- After creating the branch, teammate MUST call the MCP tool `update_implementation_branch` to register it

**After creating the branch, IMMEDIATELY call:**
```
update_implementation_branch(task_id="{task-id}", branch="agent/{task-id}")
```
This registers the branch in the implementation record and enables the automated merge detection job.

**Verification:**
```bash
git branch --show-current
# Expected: agent/{task-id}
```
Verify the MCP tool was called by checking `implementation.branch` is set on the task.

**Exceptions:** NONE. Always use this format and register the branch.

---

### Rule 5: Max Retries for Test Fixing

**Statement:** Maximum 3 retry attempts for fixing test failures. After 3 failures, escalate to Implementation Lead.

**Rationale:** Prevents infinite loops of retry attempts. Forces escalation for systemic issues.

**Retry workflow:**
1. **Attempt 1:** Initial implementation → tests fail
2. **Attempt 2:** Fix issue → re-run tests → still fail
3. **Attempt 3:** Different approach → re-run tests → still fail
4. **Escalation:** Report to Implementation Lead with:
   - All 3 attempts documented in journal
   - Root cause analysis
   - Recommended next steps

**What qualifies for retry:**
- Test failures (flaky tests, dependency issues)
- Build failures (transient errors)
- Linting failures (auto-fixable)

**What does NOT qualify for retry (escalate immediately):**
- Architectural issues (requires redesign)
- Missing dependencies (requires new tools)
- Scope creep (requires plan change)
- Fairmind context issues (requires clarification)

**Enforcement:**
- Implementation Lead monitors retry count
- After 3 attempts, work stopped and escalated
- User decides whether to continue or change approach

**Verification:**
- Check journal for retry entries
- Count test failure entries
- Look for "Attempt 1/2/3" markers

**Exceptions:** NONE. Max 3 retries, then escalate.

---

### Rule 6: Budget Enforcement

**Statement:** Work MUST stop immediately if budget limit exceeded.

**Budget defined in work package:**
```markdown
**Budget:** $50 USD
**Budget per task:** $10 USD
```

**Monitoring:**
- Track API calls made
- Track tokens used
- Estimate costs (if provider exposes cost data)

**Enforcement:**
1. Before each major operation, check budget
2. If budget exceeded:
   - Stop all work immediately
   - Document current progress in journal
   - Report to Implementation Lead with:
     - Amount spent vs budgeted
     - Tasks completed
     - Tasks remaining
     - Recommendation (continue or stop)
   - Await decision
3. Do NOT continue work until decision received

**Verification:**
- Check coordination logs for budget tracking
- Check for "budget exceeded" flags
- Compare actual spend to budgeted amount

**Exceptions:**
- If no budget specified in work package → no limit
- If user explicitly authorizes budget increase → new limit applies

---

### Rule 7: Always Link PR to Fairmind Task ID

**Statement:** Every PR MUST include the Fairmind task ID in the description.

**Format:**
```markdown
**Fairmind Task ID:** {task_id}
**User Story:** {story_id}
```

**Rationale:** Ensures traceability from code changes back to business requirements.

**Enforcement:**
- Implementation Lead verifies PR description includes task ID
- PR creation blocked if task ID missing
- Teammate must update PR description

**Verification:**
```bash
gh pr view {pr_number} --json body --jq '.body' | grep "Fairmind Task ID"
```

**Exceptions:** NONE. Always link PR to task ID.

---

### Rule 8: No Work on Main/Master/Develop Directly

**Statement:** Code changes MUST NOT be committed directly to main, master, or develop branches.

**Rationale:** Protects production code from untested changes. Ensures PR review process.

**Enforcement:**
- Implementation Lead verifies branch name before PR
- PR creation blocked if on protected branch
- Teammate must create feature branch (see Rule 4)

**Verification:**
```bash
git branch --show-current
# Must NOT be: main, master, develop
```

**Exceptions:** NONE. Always use feature branches.

---

### Rule 9: Journal Quality Standards

**Statement:** Journals MUST meet minimum quality standards. Bullet-list journals without context are UNACCEPTABLE.

**Minimum standards per section:**
- **Work Log:** Each entry MUST have timestamp + 3+ sentences (what, why, alternatives)
- **Technical Decisions:** Each decision MUST state problem, options, chosen approach, reasoning
- **Testing Completed:** MUST list specific tests, commands, results
- **Integration Points:** MUST identify every component/service touched
- **Final Outcomes:** MUST include next steps or explicitly state "none"

**BAD journal (unacceptable):**
```markdown
### Step 1: Add login
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

**Enforcement:**
- Implementation Lead reviews journals before marking task complete
- Task marked incomplete if journal lacks quality
- Teammate must update journal to meet standards

**Verification:**
- Check for timestamps in Work Log entries
- Check for "why" and "alternatives" in entries
- Check for test commands and results in Testing section
- Check for reasoning in Technical Decisions section

**Exceptions:** NONE. Quality standards are mandatory.

---

### Rule 10: Completion Criteria

**Statement:** A task is NOT complete until ALL of the following are true:

- [ ] All 8 Blueprint steps completed in order
- [ ] Journal quality meets standards (Rule 9)
- [ ] All tests passing (Rule 1)
- [ ] PR created and linked to Fairmind task (Rule 7)
- [ ] Budget not exceeded (Rule 6)
- [ ] No retry limit violations (Rule 5)
- [ ] All acceptance criteria met
- [ ] Completion flag created: `${FAIRMIND_BASE}/work_packages/{domain}/{task_id}_complete.flag`

**Enforcement:**
- Implementation Lead verifies ALL criteria before accepting completion
- If ANY criterion unmet → task sent back to teammate
- Teammate must address issues and re-signal completion

**Verification:**
- Check completion flag exists
- Check all boxes above
- Review journal, tests, PR, budget logs

**Exceptions:** NONE. All criteria must be met.

---

## Escalation Rules

### When to Escalate to Implementation Lead

**Immediate escalation required for:**
- 3 retry attempts exhausted (Rule 5)
- Budget limit reached/exceeded (Rule 6)
- Critical information missing from Fairmind
- Teammate permanently blocked
- Architectural conflict requires decision
- Scope creep detected
- Timeline at risk

**Escalation format:**
```markdown
# Escalation: {Issue Summary}

**Task ID:** {task_id}
**Teammate:** {agent_name}
**Issue:** {specific problem}

## Context
{What was attempted, what failed, why}

## Attempts
1. {Attempt 1 details and outcome}
2. {Attempt 2 details and outcome}
3. {Attempt 3 details and outcome}

## Root Cause Analysis
{Why this happened, what's blocking progress}

## Recommendation
{Proposed next steps}

## Decision Required
{What user/Implementation Lead needs to decide}
```

Save to: `${FAIRMIND_BASE}/coordination_logs/escalation_{task_id}_{timestamp}.md`

### When to Escalate to User

**User escalation required for:**
- Budget increase needed (Rule 6)
- Major scope change required
- Architectural decision needed
- Timeline extension needed
- Resource constraints (missing tools, access, etc.)

**User escalation format:**
- Implementation Lead creates summary
- Includes cost analysis
- Includes timeline impact
- Includes recommendation
- Awaits user decision

---

## Enforcement Summary

| Rule | Enforced By | Consequence of Violation |
|------|------------|-------------------------|
| 1. Green tests | Implementation Lead | PR blocked |
| 2. Approved plan | Implementation Lead | Code changes blocked |
| 3. Journal updates | Implementation Lead | Task marked incomplete |
| 4. Branch naming | Implementation Lead | PR blocked |
| 5. Max retries | Implementation Lead | Work stopped, escalated |
| 6. Budget limit | Implementation Lead | Work stopped, escalated |
| 7. PR linking | Implementation Lead | PR blocked |
| 8. No direct commits | Implementation Lead | PR blocked |
| 9. Journal quality | Implementation Lead | Task marked incomplete |
| 10. Completion criteria | Implementation Lead | Task sent back |

---

## Final Reminder

**These rules are MANDATORY, not guidelines.**

Compliance ensures:
- Quality code
- Complete traceability
- Efficient coordination
- Budget adherence
- Timely delivery
- User satisfaction

**When in doubt about a rule, ask Implementation Lead for clarification. Do NOT proceed with uncertainty.**
