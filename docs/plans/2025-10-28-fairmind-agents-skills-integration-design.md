# Fairmind Agents & Skills Integration Design

**Date:** 2025-10-28
**Status:** Approved
**Use Case:** Team collaboration with Fairmind platform integration

## Executive Summary

This design outlines a two-phase approach to integrate Fairmind MCP tools into the existing 12 agents and create standalone Fairmind-aware skills for software development workflows. The focus is on team collaboration with full traceability from implementation plans to code review.

## Requirements

- **Use case:** Team collaboration (consistency, clear handoffs between agents)
- **Priority:** Agent updates first, then skills creation
- **Skill philosophy:** Standalone Fairmind skills (purpose-built, not wrappers)
- **Key insight:** Fairmind tasks contain implementation plans that Atlas adapts for specialized agents

## Architecture Overview

### Fairmind MCP Tools (40 total)

**General Tools (13):**
- Project/session management: `list_projects`, `list_work_sessions`, `list_input_sources_by_session`
- Document access: `list_user_attachments_by_project`, `get_document_content`
- RAG retrieval: `rag_retrieve_documents`, `rag_retrieve_specific_documents` (+ session variants)
- Cross-project support for integration scenarios

**Studio Tools (21):**
- Needs: `list_needs_by_project`, `list_needs_by_session`, `get_need`
- User Stories: `list_user_stories_by_project`, `list_user_stories_by_need`, `list_user_stories_by_session`, `list_user_stories_by_role`, `get_user_story`, `get_related_user_stories`
- Tasks: `list_tasks_by_project`, `list_tasks_by_session`, `list_development_tasks_by_session`, `get_task`
- Requirements: `list_requirements_by_project`, `list_functional_requirements_by_session`, `list_technical_requirements_by_session`, `get_requirement`
- Tests: `list_tests_by_userstory`, `list_tests_by_project`

**Code Tools (6):**
- Purpose: **Cross-repository access** (not current repository - use local file tools for that)
- Tools: `list_repositories`, `search`, `cat`, `tree`, `grep`, `find_usages`
- Use cases: Debug cross-service integrations, understand API contracts, troubleshoot dependencies

### Agent-to-Skill Workflow

```
1. Tech Lead (Atlas)
   ├─ get_task → Retrieve Fairmind implementation plans
   ├─ Analyze agent capabilities vs plan requirements
   ├─ Adapt/translate plans into specialized work packages
   └─ Write to fairmind/work_packages/{role}/

2. Specialized Dev Agent (AI/Backend/Frontend Engineer)
   ├─ Read work package from Atlas
   ├─ Use fairmind-context skill → Gather full context
   ├─ Use fairmind-tdd skill → Implement following plan
   └─ Update fairmind/journals/{role}/ → Document work

3. Code Reviewer (Echo)
   ├─ Use fairmind-code-review skill
   ├─ Verify: Plan → Journal → Code traceability
   └─ Validate against requirements/acceptance criteria
```

## Phase A: Agent Updates (Role-Based Grouping)

### Batch 1: Development Agents
**Agents:** AI Engineer, Backend Engineer, Frontend Engineer

**MCP Tools to Add:**
- **Studio:** `get_user_story`, `get_task`, `get_requirement`, `list_tests_by_userstory`
- **Code:** `list_repositories`, `search`, `cat`, `tree`, `grep`, `find_usages` (for cross-repo integrations)
- **General:** `rag_retrieve_documents`, `get_document_content`

**New Workflows:**
1. **Start of work:** Check `get_task` for Atlas's adapted plan, `get_user_story` for context
2. **During development:**
   - Follow implementation plan from `get_task`
   - Query `rag_retrieve_documents` for patterns/examples
   - Update `fairmind/journals/{role}/` with progress
3. **Cross-service integration:** Use `Code_search` to understand other services' APIs
4. **Before completion:** Verify against `get_requirement` acceptance criteria

**Parallel Execution:** All three can be updated simultaneously (similar patterns)

---

### Batch 2: Validation Agents

**QA Engineer (Tess)**

**MCP Tools:**
- **Studio:** `list_tests_by_userstory`, `list_tests_by_project`, `get_user_story`
- **General:** `get_document_content` (test plans/specifications)
- **Code:** Optional - only if testing cross-service integrations

**Workflow:**
- Retrieve test expectations from Fairmind before creating tests
- Validate test coverage against acceptance criteria

---

**Code Reviewer (Echo)**

**MCP Tools:**
- **Studio:** `get_user_story`, `get_requirement`, `get_task`
- **Code:** Full suite (for cross-repo integration verification)
- **General:** Access to journals via file system

**Workflow:**
1. Get implementation plan from `get_task`
2. Read agent journal from `fairmind/journals/{role}/`
3. Compare plan → journal → code for traceability
4. Validate against requirements and acceptance criteria
5. Check cross-repo API contracts if integration work

---

**Cybersecurity (Shield)**

**MCP Tools:**
- **Studio:** `list_requirements_by_project`, `list_technical_requirements_by_session`
- **General:** `rag_retrieve_documents` (security patterns/vulnerabilities)
- **Code:** Full suite (analyze attack surfaces across services)

**Workflow:**
- Query security requirements before review
- Build security checklist from Fairmind requirements
- Validate implementation against OWASP + Fairmind security requirements

---

### Batch 3: Utility Agents

**Debug Detective**
- **Add:** Code tools (cross-service debugging), `rag_retrieve_documents` (similar issues)
- **Add:** `get_user_story` (bug context)

**Backend/Frontend Issue Fixers**
- **Add:** `get_user_story` only (minimal context)
- **Philosophy:** Keep lightweight, targeted fixes

**Playwright Issue Analyzer & PR Diff Documenter**
- **No changes needed** (already specialized, no Fairmind context required)

---

### Batch 4: Orchestration (Most Critical)

**Tech Lead (Atlas)**

**MCP Tools:** ALL 40 Fairmind tools (General + Studio + Code)

**Major Transformation - Plan Adaptation:**

**Old workflow:** Coordinate only, never implement
**New workflow:** Coordinate + Adapt plans for agents

**Enhanced Workflow:**
1. `get_task` → Retrieve Fairmind implementation plan (generic)
2. **Analyze plan requirements:**
   - What technologies? (determines AI/Backend/Frontend agent)
   - What integrations? (requires Code tools for cross-repo)
   - What complexity? (might need multiple agents)
3. **Decompose and adapt:**
   - Break generic plan into agent-specific instructions
   - Add agent-specific context (file paths, dependencies, patterns)
   - Consider agent capabilities and constraints
4. **Create work packages:**
   - Write to `fairmind/work_packages/{role}/`
   - Include: adapted plan, relevant context, success criteria
5. **Monitor execution:**
   - Track journal updates
   - Coordinate handoffs between agents
   - Escalate blockers

**Critical Principle:** Atlas translates between Fairmind's project plans and agent-specific capabilities. NEVER implements code, ALWAYS adapts plans.

---

## Phase B: Skills Creation (Standalone)

### Skill 1: fairmind-context (Foundation)

**Purpose:** Reusable context gathering for any Fairmind development work

**Inputs:**
- `project_id` (optional - can detect from environment or query)
- `user_story_id` (optional)
- `task_id` (optional)
- `target_project_id` (optional - for cross-project integrations)

**Process:**
1. Identify current project (via `General_list_projects` or from parameter)
2. Retrieve active work session (via `General_list_work_sessions`)
3. Gather context based on available IDs:
   - User story: `Studio_get_user_story`
   - Task with implementation plan: `Studio_get_task`
   - Requirements: `Studio_get_requirement`
   - Test expectations: `Studio_list_tests_by_userstory`
   - Related documentation: `General_rag_retrieve_documents`
4. If cross-project work: query target project context as well

**Outputs:**
```json
{
  "project": { "id": "...", "name": "..." },
  "session": { "id": "...", "status": "active" },
  "user_story": { "id": "...", "title": "...", "acceptance_criteria": [...] },
  "task": { "id": "...", "implementation_plan": "...", "status": "..." },
  "requirements": [...],
  "tests": [...],
  "documentation": [...]
}
```

**Invoked by:** All other Fairmind skills as first step

---

### Skill 2: fairmind-tdd (Test-Driven Development)

**Purpose:** TDD workflow aligned with Fairmind test plans and acceptance criteria

**Process:**

**SETUP PHASE:**
1. Invoke `fairmind-context` → Get full context
2. Get implementation plan → `Studio_get_task`
3. Understand WHAT to build from plan
4. Check test expectations → `Studio_list_tests_by_userstory`

**RED PHASE:**
5. Write failing test aligned with:
   - Implementation plan scope
   - Fairmind acceptance criteria
   - Expected test coverage from `list_tests_by_userstory`
6. Run test → Verify it fails (no false positives)

**GREEN PHASE:**
7. Implement minimal code following implementation plan
8. Run test → Verify it passes

**REFACTOR PHASE:**
9. Clean up code (maintain test passage)
10. Ensure code quality standards

**DOCUMENTATION PHASE:**
11. Update `fairmind/journals/{role}/` with:
    - What was implemented
    - Which plan items completed
    - Test coverage achieved
12. Validate: Test coverage matches Fairmind acceptance criteria

**Key Difference from Generic TDD:**
- Tests are **aligned with Fairmind acceptance criteria** (not invented)
- Implementation follows **plan from `get_task`** (not free-form)
- Journal provides **traceability** for code review

---

### Skill 3: fairmind-code-review (Code Review)

**Purpose:** Systematic code review with plan-journal-code traceability

**Process:**

**LAYER 1: PLAN VERIFICATION**
1. Get implementation plan → `Studio_get_task`
2. Read agent journal → `fairmind/journals/{role}/`
3. Compare plan vs journal:
   - Are all planned items addressed?
   - Are journal entries aligned with plan?
   - **Flag discrepancies** (scope creep, missing items)

**LAYER 2: REQUIREMENTS VERIFICATION**
4. Invoke `fairmind-context` → Get requirements, user story, acceptance criteria
5. Build checklist from:
   - User story acceptance criteria
   - Functional requirements (`Studio_get_requirement`)
   - Technical requirements
   - Test coverage expectations
6. Review code against checklist

**LAYER 3: CROSS-REPOSITORY VERIFICATION** (if integration)
7. Identify integration points from implementation plan
8. Use `Code_search` to verify API contracts in other repositories
9. Check for breaking changes
10. Validate integration patterns

**OUTPUT STRUCTURE:**
```markdown
## Plan Compliance
- ✓ Implemented feature X (journal: "Added X in file.ts:42")
- ✓ Implemented feature Y (journal: "Completed Y with tests")
- ✗ Missing feature Z from plan
- ⚠ Journal entry for W not in original plan (scope creep?)

## Requirements Compliance
- ✓ Acceptance criteria 1: Users can login
- ✓ Functional requirement FR-123: Session timeout
- ✗ Technical requirement TR-456: Input validation missing

## Integration Check
- ✓ API contract with auth-service maintained
- ⚠ New dependency on payment-service (not in plan)

## Recommendations
1. Address missing feature Z
2. Add input validation for TR-456
3. Clarify payment-service dependency with Atlas
```

**Key Difference from Generic Code Review:**
- Three-layer verification (plan → journal → code)
- Requirements from Fairmind (not generic best practices)
- Cross-repo integration checks using Code tools

---

## Implementation Sequence

### Phase A: Agent Updates

**Batch 1: Development Agents** (Parallel)
1. Update `ai-engineer.md`
2. Update `backend-engineer.md`
3. Update `frontend-engineer.md`

**Batch 2: Validation Agents** (Parallel)
4. Update `qa-engineer.md`
5. Update `code-reviewer.md`
6. Update `cybersec-engineer.md`

**Batch 3: Utility Agents** (Parallel)
7. Update `debug-detective.md`
8. Update `backend-issue-fixer.md`
9. Update `frontend-issue-fixer.md`
10. No changes: `playwright-issue-analyzer.md`, `pr-diff-documenter.md`

**Batch 4: Orchestration** (Sequential - most critical)
11. Update `tech-lead-software-architect.md`

### Phase B: Skills Creation

**Step 1: Foundation** (Sequential)
1. Create `fairmind-context.md`

**Step 2: Core Skills** (Parallel - both depend on fairmind-context)
2. Create `fairmind-tdd.md`
3. Create `fairmind-code-review.md`

**Step 3: Integration Testing**
4. Test full workflow: Atlas → Dev agent (using fairmind-tdd) → Code Review (using fairmind-code-review)

---

## Success Criteria

**Agent Updates:**
- ✓ All agents reference current Fairmind MCP tools (no old "FairMind Platform" references)
- ✓ Role-appropriate tool distribution (dev vs validation vs utility vs orchestration)
- ✓ Clear workflows documented in each agent file
- ✓ Atlas has plan adaptation capabilities

**Skills:**
- ✓ fairmind-context successfully gathers multi-project context
- ✓ fairmind-tdd aligns tests with acceptance criteria and implementation plans
- ✓ fairmind-code-review provides plan→journal→code traceability
- ✓ Skills are standalone (no superpowers dependencies)

**Team Workflow:**
- ✓ Clear handoffs: Atlas → Dev → Code Review
- ✓ Full traceability from Fairmind plan to code
- ✓ Cross-repository integration support
- ✓ Journal-based progress tracking

---

## Future Enhancements (Out of Scope)

- Additional skills: fairmind-debugging, fairmind-planning, fairmind-deployment
- Integration with CI/CD pipelines
- Automated journal generation
- Multi-agent parallel execution for complex tasks
- Skills for project managers and product owners

---

## Notes

- **Code tools are for cross-repo access only** - use local file tools (Read, Glob, Grep) for current repository
- **Journals are critical** - provide traceability chain from plan to implementation
- **Atlas is a translator** - adapts generic Fairmind plans for specialized agent capabilities
- **Skills are composable** - fairmind-context is foundation for all other skills
