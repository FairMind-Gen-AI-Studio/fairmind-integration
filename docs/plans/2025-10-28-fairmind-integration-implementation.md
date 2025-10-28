# Fairmind Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate Fairmind MCP tools into 12 existing agents and create 3 standalone Fairmind-aware skills for team collaboration workflows.

**Architecture:** Two-phase approach - (A) Update agent files with role-appropriate Fairmind MCP tools and workflows, (B) Create standalone skills for context gathering, TDD, and code review with full traceability.

**Tech Stack:** Markdown agent definitions, Fairmind MCP tools (40 total), skill system integration

---

## Phase A: Agent Updates

### Task 1: Update AI Engineer Agent

**Files:**
- Modify: `agents/ai-engineer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Update the `tools:` line in frontmatter to add Fairmind Studio and General tools after existing tools:

```yaml
tools: Task, Bash, Glob, Grep, LS, ExitPlanMode, Read, Edit, MultiEdit, Write, NotebookRead, NotebookEdit, WebFetch, TodoWrite, WebSearch, mcp__memory__create_entities, mcp__memory__create_relations, mcp__memory__add_observations, mcp__memory__delete_entities, mcp__memory__delete_observations, mcp__memory__delete_relations, mcp__memory__read_graph, mcp__memory__search_nodes, mcp__memory__open_nodes, mcp__sequential-thinking__sequentialthinking, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__MongoDB__list-collections, mcp__MongoDB__list-databases, mcp__MongoDB__collection-indexes, mcp__MongoDB__collection-schema, mcp__MongoDB__find, mcp__MongoDB__collection-storage-size, mcp__MongoDB__count, mcp__MongoDB__db-stats, mcp__MongoDB__aggregate, mcp__MongoDB__explain, mcp__MongoDB__mongodb-logs, mcp__Fairmind__Studio_get_user_story, mcp__Fairmind__Studio_get_task, mcp__Fairmind__Studio_get_requirement, mcp__Fairmind__Studio_list_tests_by_userstory, mcp__Fairmind__Code_list_repositories, mcp__Fairmind__Code_search, mcp__Fairmind__Code_cat, mcp__Fairmind__Code_tree, mcp__Fairmind__Code_grep, mcp__Fairmind__Code_find_usages, mcp__Fairmind__General_rag_retrieve_documents, mcp__Fairmind__General_get_document_content
```

**Step 2: Update workflow section to include Fairmind context gathering**

Insert after line 26 (before "### Development Process"):

```markdown
## Fairmind Integration

### Starting Work
Before implementing any task:
1. Check `fairmind/work_packages/ai/{task_id}_ai_workpackage.md` for Atlas's adapted implementation plan
2. Use `mcp__Fairmind__Studio_get_task` to retrieve the original Fairmind task with full context
3. Use `mcp__Fairmind__Studio_get_user_story` to understand the business context and acceptance criteria
4. Query `mcp__Fairmind__General_rag_retrieve_documents` for AI patterns and similar implementations

### During Development
1. Follow the implementation plan from the work package (adapted by Atlas for AI work)
2. Document progress in `fairmind/journals/ai/{task_id}_echo-aiengineer_journal.md`
3. For cross-service integrations: Use `mcp__Fairmind__Code_search` to understand other repositories' APIs
4. Query RAG for prompt templates, LLM configurations, and AI architectural patterns

### Before Completion
1. Verify implementation against acceptance criteria from `mcp__Fairmind__Studio_get_requirement`
2. Validate test coverage expectations from `mcp__Fairmind__Studio_list_tests_by_userstory`
3. Ensure journal provides full traceability: plan → implementation → outcomes
4. Create completion flag: `fairmind/work_packages/ai/{task_id}_ai_complete.flag`

### Cross-Repository Integration
When your AI components need to integrate with other services:
- Use `mcp__Fairmind__Code_list_repositories` to see available services
- Use `mcp__Fairmind__Code_search` to find API endpoints and integration patterns
- Use `mcp__Fairmind__Code_cat` to read API documentation or interface definitions
- Use `mcp__Fairmind__Code_grep` to find usage examples across repositories

```

**Step 3: Verify the changes**

Run: `head -10 agents/ai-engineer.md | grep "mcp__Fairmind"`
Expected: Should show Fairmind tools in the tools list

**Step 4: Commit AI Engineer update**

```bash
git add agents/ai-engineer.md
git commit -m "feat(agents): integrate Fairmind MCP tools into AI Engineer

- Add Studio tools for task/user story/requirement retrieval
- Add Code tools for cross-repository integration discovery
- Add General tools for RAG-based pattern/example retrieval
- Document workflows for context gathering and journal updates

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Update Backend Engineer Agent

**Files:**
- Modify: `agents/backend-engineer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Read the current frontmatter and append Fairmind tools to the tools list:

```yaml
mcp__Fairmind__Studio_get_user_story, mcp__Fairmind__Studio_get_task, mcp__Fairmind__Studio_get_requirement, mcp__Fairmind__Studio_list_tests_by_userstory, mcp__Fairmind__Code_list_repositories, mcp__Fairmind__Code_search, mcp__Fairmind__Code_cat, mcp__Fairmind__Code_tree, mcp__Fairmind__Code_grep, mcp__Fairmind__Code_find_usages, mcp__Fairmind__General_rag_retrieve_documents, mcp__Fairmind__General_get_document_content
```

**Step 2: Add Fairmind Integration section**

Insert a "## Fairmind Integration" section following the same pattern as AI Engineer, adapted for backend work:

```markdown
## Fairmind Integration

### Starting Work
Before implementing any task:
1. Check `fairmind/work_packages/backend/{task_id}_backend_workpackage.md` for Atlas's adapted implementation plan
2. Use `mcp__Fairmind__Studio_get_task` to retrieve the original Fairmind task with full context
3. Use `mcp__Fairmind__Studio_get_user_story` to understand the business requirements and acceptance criteria
4. Query `mcp__Fairmind__General_rag_retrieve_documents` for backend patterns, API designs, and similar implementations

### During Development
1. Follow the implementation plan from the work package (adapted by Atlas for backend work)
2. Document progress in `fairmind/journals/backend/{task_id}_backend-engineer_journal.md`
3. For cross-service integrations: Use `mcp__Fairmind__Code_search` to understand service contracts and APIs
4. Query RAG for architectural patterns, database schemas, and service integration examples

### Before Completion
1. Verify implementation against acceptance criteria from `mcp__Fairmind__Studio_get_requirement`
2. Validate test coverage expectations from `mcp__Fairmind__Studio_list_tests_by_userstory`
3. Ensure journal provides full traceability: plan → implementation → outcomes
4. Create completion flag: `fairmind/work_packages/backend/{task_id}_backend_complete.flag`

### Cross-Repository Integration
When your backend services need to integrate with other services:
- Use `mcp__Fairmind__Code_list_repositories` to see available services
- Use `mcp__Fairmind__Code_search` to find API endpoints, service contracts, and integration patterns
- Use `mcp__Fairmind__Code_cat` to read API documentation, OpenAPI specs, or GraphQL schemas
- Use `mcp__Fairmind__Code_grep` to find usage examples and integration tests across repositories

```

**Step 3: Verify the changes**

Run: `grep -c "mcp__Fairmind" agents/backend-engineer.md`
Expected: Should return a count > 0

**Step 4: Commit Backend Engineer update**

```bash
git add agents/backend-engineer.md
git commit -m "feat(agents): integrate Fairmind MCP tools into Backend Engineer

- Add Studio tools for task/user story/requirement retrieval
- Add Code tools for cross-service API discovery
- Add General tools for RAG-based pattern retrieval
- Document workflows for backend development with Fairmind

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Update Frontend Engineer Agent

**Files:**
- Modify: `agents/frontend-engineer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Append Fairmind tools to the tools list (same tools as AI and Backend engineers).

**Step 2: Add Fairmind Integration section**

Insert adapted for frontend work:

```markdown
## Fairmind Integration

### Starting Work
Before implementing any task:
1. Check `fairmind/work_packages/frontend/{task_id}_frontend_workpackage.md` for Atlas's adapted implementation plan
2. Use `mcp__Fairmind__Studio_get_task` to retrieve the original Fairmind task with full context
3. Use `mcp__Fairmind__Studio_get_user_story` to understand UI/UX requirements and acceptance criteria
4. Query `mcp__Fairmind__General_rag_retrieve_documents` for component patterns, UI libraries, and similar implementations

### During Development
1. Follow the implementation plan from the work package (adapted by Atlas for frontend work)
2. Document progress in `fairmind/journals/frontend/{task_id}_frontend-engineer_journal.md`
3. For backend API integrations: Use `mcp__Fairmind__Code_search` to understand API contracts and endpoints
4. Query RAG for UI patterns, component libraries, state management approaches, and accessibility guidelines

### Before Completion
1. Verify implementation against acceptance criteria from `mcp__Fairmind__Studio_get_requirement`
2. Validate test coverage expectations from `mcp__Fairmind__Studio_list_tests_by_userstory`
3. Ensure journal provides full traceability: plan → implementation → outcomes
4. Create completion flag: `fairmind/work_packages/frontend/{task_id}_frontend_complete.flag`

### Cross-Repository Integration
When your frontend needs to integrate with backend services or shared components:
- Use `mcp__Fairmind__Code_list_repositories` to see available backend services and component libraries
- Use `mcp__Fairmind__Code_search` to find API client code, type definitions, and integration patterns
- Use `mcp__Fairmind__Code_cat` to read API documentation, component interfaces, or shared type definitions
- Use `mcp__Fairmind__Code_grep` to find usage examples and integration tests across repositories

```

**Step 3: Verify the changes**

Run: `grep "mcp__Fairmind__Studio_get_user_story" agents/frontend-engineer.md`
Expected: Should show the tool in the tools list

**Step 4: Commit Frontend Engineer update**

```bash
git add agents/frontend-engineer.md
git commit -m "feat(agents): integrate Fairmind MCP tools into Frontend Engineer

- Add Studio tools for task/user story/requirement retrieval
- Add Code tools for backend API and component discovery
- Add General tools for RAG-based UI pattern retrieval
- Document workflows for frontend development with Fairmind

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: Update QA Engineer Agent

**Files:**
- Modify: `agents/qa-engineer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Append these specific tools for QA work:

```yaml
mcp__Fairmind__Studio_list_tests_by_userstory, mcp__Fairmind__Studio_list_tests_by_project, mcp__Fairmind__Studio_get_user_story, mcp__Fairmind__General_get_document_content
```

**Step 2: Add Fairmind Integration section**

Insert adapted for QA work:

```markdown
## Fairmind Integration

### Starting Test Development
Before creating any tests:
1. Use `mcp__Fairmind__Studio_get_user_story` to retrieve acceptance criteria and business requirements
2. Use `mcp__Fairmind__Studio_list_tests_by_userstory` to understand expected test coverage
3. Use `mcp__Fairmind__General_get_document_content` to access test plans, specifications, and test scenarios

### During Test Creation
1. Align test cases with Fairmind acceptance criteria (not invented test scenarios)
2. Document test approach in `fairmind/journals/qa/{task_id}_qa-engineer_journal.md`
3. Ensure test coverage matches expectations from `list_tests_by_userstory`

### Test Validation
1. Verify all acceptance criteria have corresponding test cases
2. Validate test coverage against Fairmind requirements
3. Create test completion report in journal with coverage metrics

### Cross-Service Testing
When testing integrations (optional - only if needed):
- Use `mcp__Fairmind__Code_search` to understand integration points
- Verify API contracts match test expectations
- Document integration test approach in journal

```

**Step 3: Verify the changes**

Run: `grep "list_tests_by_userstory" agents/qa-engineer.md`
Expected: Should show the tool in the tools list and usage in content

**Step 4: Commit QA Engineer update**

```bash
git add agents/qa-engineer.md
git commit -m "feat(agents): integrate Fairmind MCP tools into QA Engineer

- Add Studio tools for test expectations and user story retrieval
- Add General tools for test plan document access
- Document workflow for aligning tests with acceptance criteria
- Add optional Code tools for integration testing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: Update Code Reviewer Agent

**Files:**
- Modify: `agents/code-reviewer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Append comprehensive toolset for code review:

```yaml
mcp__Fairmind__Studio_get_user_story, mcp__Fairmind__Studio_get_requirement, mcp__Fairmind__Studio_get_task, mcp__Fairmind__Code_list_repositories, mcp__Fairmind__Code_search, mcp__Fairmind__Code_cat, mcp__Fairmind__Code_tree, mcp__Fairmind__Code_grep, mcp__Fairmind__Code_find_usages
```

**Step 2: Add Fairmind Integration section**

Insert comprehensive code review workflow:

```markdown
## Fairmind Integration

### Code Review Process

#### LAYER 1: Plan Verification
1. Use `mcp__Fairmind__Studio_get_task` to retrieve the implementation plan
2. Read agent journal from `fairmind/journals/{role}/{task_id}_*_journal.md`
3. Compare plan vs journal:
   - ✓ Are all planned items addressed?
   - ✓ Are journal entries aligned with plan steps?
   - ✗ Flag discrepancies (scope creep, missing items)

#### LAYER 2: Requirements Verification
4. Use `mcp__Fairmind__Studio_get_user_story` to get acceptance criteria
5. Use `mcp__Fairmind__Studio_get_requirement` to get functional/technical requirements
6. Build verification checklist:
   - User story acceptance criteria
   - Functional requirements
   - Technical requirements
   - Test coverage expectations
7. Review code against checklist

#### LAYER 3: Cross-Repository Verification (if integration work)
8. Identify integration points from implementation plan
9. Use `mcp__Fairmind__Code_list_repositories` to identify target services
10. Use `mcp__Fairmind__Code_search` to verify API contracts in other repositories
11. Check for breaking changes using `mcp__Fairmind__Code_find_usages`
12. Validate integration patterns match documented contracts

### Review Output Format

Document findings in this structure:

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

```

**Step 3: Verify the changes**

Run: `grep "LAYER 1: Plan Verification" agents/code-reviewer.md`
Expected: Should find the new section

**Step 4: Commit Code Reviewer update**

```bash
git add agents/code-reviewer.md
git commit -m "feat(agents): integrate Fairmind MCP tools into Code Reviewer

- Add three-layer verification workflow (plan→journal→code)
- Add Studio tools for plan/requirements retrieval
- Add Code tools for cross-repository integration verification
- Document structured review output format with traceability

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 6: Update Cybersecurity Engineer Agent

**Files:**
- Modify: `agents/cybersec-engineer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Append security-focused toolset:

```yaml
mcp__Fairmind__Studio_list_requirements_by_project, mcp__Fairmind__Studio_list_technical_requirements_by_session, mcp__Fairmind__General_rag_retrieve_documents, mcp__Fairmind__Code_list_repositories, mcp__Fairmind__Code_search, mcp__Fairmind__Code_cat, mcp__Fairmind__Code_tree, mcp__Fairmind__Code_grep, mcp__Fairmind__Code_find_usages
```

**Step 2: Add Fairmind Integration section**

Insert security-focused workflow:

```markdown
## Fairmind Integration

### Security Review Process

#### Starting Security Review
1. Use `mcp__Fairmind__Studio_list_requirements_by_project` to retrieve all project requirements
2. Use `mcp__Fairmind__Studio_list_technical_requirements_by_session` for session-specific security requirements
3. Use `mcp__Fairmind__General_rag_retrieve_documents` to query:
   - Known security vulnerabilities in similar implementations
   - OWASP best practices for the technology stack
   - Security patterns and anti-patterns
   - Previous security incidents and resolutions

#### Building Security Checklist
4. Extract security requirements from Fairmind requirements
5. Combine with OWASP Top 10 and industry standards
6. Create comprehensive security checklist covering:
   - Authentication and authorization
   - Input validation and sanitization
   - Data encryption (at rest and in transit)
   - Secrets management
   - API security
   - Dependency vulnerabilities

#### Cross-Service Security Analysis
When reviewing integrations:
- Use `mcp__Fairmind__Code_list_repositories` to identify all services in the ecosystem
- Use `mcp__Fairmind__Code_search` to analyze attack surfaces across services
- Use `mcp__Fairmind__Code_find_usages` to trace data flow and identify exposure points
- Use `mcp__Fairmind__Code_grep` to find security-sensitive code patterns

#### Security Review Output
Document findings with:
- ✓ Security requirements met
- ✗ Security requirements violated
- ⚠ Potential vulnerabilities identified
- 🔥 Critical security issues requiring immediate attention
- Recommendations with priority levels

```

**Step 3: Verify the changes**

Run: `grep "Security Review Process" agents/cybersec-engineer.md`
Expected: Should find the new section

**Step 4: Commit Cybersecurity Engineer update**

```bash
git add agents/cybersec-engineer.md
git commit -m "feat(agents): integrate Fairmind MCP tools into Cybersecurity Engineer

- Add Studio tools for security requirements retrieval
- Add RAG-based vulnerability and pattern discovery
- Add Code tools for cross-service attack surface analysis
- Document security checklist building from Fairmind requirements

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 7: Update Debug Detective Agent

**Files:**
- Modify: `agents/debug-detective.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Append debugging-focused toolset:

```yaml
mcp__Fairmind__Studio_get_user_story, mcp__Fairmind__Code_list_repositories, mcp__Fairmind__Code_search, mcp__Fairmind__Code_cat, mcp__Fairmind__Code_grep, mcp__Fairmind__Code_find_usages, mcp__Fairmind__General_rag_retrieve_documents
```

**Step 2: Add Fairmind Integration section**

```markdown
## Fairmind Integration

### Debugging with Context

#### Starting Investigation
1. Use `mcp__Fairmind__Studio_get_user_story` to understand the feature context where the bug occurs
2. Use `mcp__Fairmind__General_rag_retrieve_documents` to search for:
   - Similar bugs and their resolutions
   - Known issues in related components
   - Debugging patterns for the technology stack

#### Cross-Service Debugging
When debugging integration issues:
- Use `mcp__Fairmind__Code_list_repositories` to identify involved services
- Use `mcp__Fairmind__Code_search` to understand data flow across services
- Use `mcp__Fairmind__Code_find_usages` to trace function calls and dependencies
- Use `mcp__Fairmind__Code_grep` to find error handling and logging patterns

#### Root Cause Documentation
Document findings in `fairmind/journals/debug/{bug_id}_debug_journal.md`:
- Bug context from user story
- Investigation steps taken
- Cross-service dependencies analyzed
- Root cause identified
- Fix recommendations

```

**Step 3: Verify the changes**

Run: `grep "Cross-Service Debugging" agents/debug-detective.md`
Expected: Should find the new section

**Step 4: Commit Debug Detective update**

```bash
git add agents/debug-detective.md
git commit -m "feat(agents): integrate Fairmind MCP tools into Debug Detective

- Add Studio tools for bug context via user stories
- Add Code tools for cross-service debugging
- Add RAG-based similar issue discovery
- Document debugging workflow with journal tracking

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 8: Update Backend Issue Fixer Agent

**Files:**
- Modify: `agents/backend-issue-fixer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Append minimal toolset (lightweight agent):

```yaml
mcp__Fairmind__Studio_get_user_story
```

**Step 2: Add Fairmind Integration section**

```markdown
## Fairmind Integration

### Quick Fix Context
Before applying fixes:
1. Use `mcp__Fairmind__Studio_get_user_story` to understand the feature context
2. Verify the fix aligns with acceptance criteria
3. Keep fixes targeted and minimal (agent philosophy)

```

**Step 3: Verify the changes**

Run: `grep "mcp__Fairmind__Studio_get_user_story" agents/backend-issue-fixer.md`
Expected: Should find the tool

**Step 4: Commit Backend Issue Fixer update**

```bash
git add agents/backend-issue-fixer.md
git commit -m "feat(agents): add minimal Fairmind integration to Backend Issue Fixer

- Add Studio get_user_story for feature context
- Keep agent lightweight and targeted
- Verify fixes align with acceptance criteria

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 9: Update Frontend Issue Fixer Agent

**Files:**
- Modify: `agents/frontend-issue-fixer.md`

**Step 1: Add Fairmind MCP tools to frontmatter**

Append minimal toolset (lightweight agent):

```yaml
mcp__Fairmind__Studio_get_user_story
```

**Step 2: Add Fairmind Integration section**

```markdown
## Fairmind Integration

### Quick Fix Context
Before applying fixes:
1. Use `mcp__Fairmind__Studio_get_user_story` to understand the UI feature context
2. Verify the fix aligns with acceptance criteria
3. Keep fixes targeted and minimal (agent philosophy)

```

**Step 3: Verify the changes**

Run: `grep "mcp__Fairmind__Studio_get_user_story" agents/frontend-issue-fixer.md`
Expected: Should find the tool

**Step 4: Commit Frontend Issue Fixer update**

```bash
git add agents/frontend-issue-fixer.md
git commit -m "feat(agents): add minimal Fairmind integration to Frontend Issue Fixer

- Add Studio get_user_story for UI feature context
- Keep agent lightweight and targeted
- Verify fixes align with acceptance criteria

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 10: Update Tech Lead (Atlas) Agent

**Files:**
- Modify: `agents/tech-lead-software-architect.md`

**Step 1: Add ALL Fairmind MCP tools to frontmatter**

Append comprehensive toolset (all 40 tools):

```yaml
mcp__Fairmind__General_list_projects, mcp__Fairmind__General_list_work_sessions, mcp__Fairmind__General_list_input_sources_by_session, mcp__Fairmind__General_list_user_attachments_by_project, mcp__Fairmind__General_get_document_content, mcp__Fairmind__General_rag_retrieve_documents, mcp__Fairmind__General_rag_retrieve_documents_for_session, mcp__Fairmind__General_rag_retrieve_specific_documents, mcp__Fairmind__General_rag_retrieve_specific_documents_for_session, mcp__Fairmind__Studio_list_needs_by_project, mcp__Fairmind__Studio_list_needs_by_session, mcp__Fairmind__Studio_get_need, mcp__Fairmind__Studio_list_user_stories_by_project, mcp__Fairmind__Studio_list_user_stories_by_need, mcp__Fairmind__Studio_list_user_stories_by_session, mcp__Fairmind__Studio_list_user_stories_by_role, mcp__Fairmind__Studio_get_user_story, mcp__Fairmind__Studio_get_related_user_stories, mcp__Fairmind__Studio_list_tasks_by_project, mcp__Fairmind__Studio_list_tasks_by_session, mcp__Fairmind__Studio_list_development_tasks_by_session, mcp__Fairmind__Studio_get_task, mcp__Fairmind__Studio_list_requirements_by_project, mcp__Fairmind__Studio_list_functional_requirements_by_session, mcp__Fairmind__Studio_list_technical_requirements_by_session, mcp__Fairmind__Studio_get_requirement, mcp__Fairmind__Studio_list_tests_by_userstory, mcp__Fairmind__Studio_list_tests_by_project, mcp__Fairmind__Code_list_repositories, mcp__Fairmind__Code_search, mcp__Fairmind__Code_cat, mcp__Fairmind__Code_tree, mcp__Fairmind__Code_grep, mcp__Fairmind__Code_find_usages
```

**Step 2: Add comprehensive Fairmind Plan Adaptation workflow**

Insert major transformation section:

```markdown
## Fairmind Plan Adaptation (Core Responsibility)

### Philosophy
Atlas is a **translator** between Fairmind's project-level implementation plans and specialized agent capabilities. NEVER implements code, ALWAYS adapts plans for agents.

### Workflow: From Fairmind Task to Agent Work Package

#### Step 1: Retrieve Fairmind Context
1. Use `mcp__Fairmind__Studio_get_task` to retrieve the implementation plan
2. Use `mcp__Fairmind__Studio_get_user_story` to understand business requirements
3. Use `mcp__Fairmind__Studio_get_requirement` to get functional/technical requirements
4. Use `mcp__Fairmind__Studio_list_tests_by_userstory` to understand test expectations

#### Step 2: Analyze Plan Requirements
Ask these questions:
- **Technology stack?** → Determines agent assignment (AI/Backend/Frontend)
- **Cross-service integrations?** → Requires Code tools, cross-repo context
- **Complexity level?** → Might need task decomposition across multiple agents
- **Dependencies?** → Determines execution order and handoffs

#### Step 3: Decompose and Adapt
Transform generic Fairmind plan into agent-specific instructions:

**For AI Engineer:**
- Extract AI/LLM-specific requirements
- Identify prompt engineering needs
- Specify framework choices (LangChain/LangGraph/etc)
- Include model selection criteria
- Add performance/cost optimization guidance

**For Backend Engineer:**
- Extract API design requirements
- Identify database schema needs
- Specify service integration points
- Include authentication/authorization patterns
- Add scalability considerations

**For Frontend Engineer:**
- Extract UI/UX requirements
- Identify component architecture
- Specify state management approach
- Include accessibility requirements
- Add responsive design guidance

**General Adaptations:**
- Convert abstract steps to concrete file paths
- Add technology-specific implementation details
- Include agent-appropriate context and examples
- Consider agent capabilities and constraints
- Add verification steps specific to the agent's role

#### Step 4: Create Work Package
Write to `fairmind/work_packages/{role}/{task_id}_{role}_workpackage.md`:

```markdown
# Work Package: {Task ID}

**Agent**: {AI Engineer / Backend Engineer / Frontend Engineer}
**User Story**: {ID and title from Fairmind}
**Original Plan**: Retrieved from Fairmind task {task_id}

## Context
{Business requirements from user story}
{Technical requirements}
{Integration points with other services}

## Adapted Implementation Plan
{Step-by-step instructions adapted for this specific agent}
{Concrete file paths}
{Technology-specific guidance}
{Code examples where helpful}

## Success Criteria
{Acceptance criteria from user story}
{Test coverage expectations}
{Performance/quality requirements}

## Integration Requirements
{Cross-service APIs to use (with repository references)}
{Data contracts to maintain}
{Dependencies on other agents' work}

## Resources
{Relevant documentation from RAG}
{Similar implementations to reference}
{Architectural patterns to follow}
```

#### Step 5: Monitor Execution
1. Track journal updates in `fairmind/journals/{role}/`
2. Watch for completion flags: `fairmind/work_packages/{role}/{task_id}_{role}_complete.flag`
3. Coordinate handoffs between agents (e.g., Backend → Frontend)
4. Escalate blockers to project stakeholders
5. Update Fairmind task status when work is complete

### Cross-Project Coordination
Use General tools for multi-project scenarios:
- `mcp__Fairmind__General_list_projects` to see all projects
- `mcp__Fairmind__General_list_work_sessions` to track active work
- `mcp__Fairmind__General_rag_retrieve_documents` for cross-project patterns

### Critical Principle
**Atlas NEVER writes code.** Atlas translates, coordinates, and adapts—but delegates all implementation to specialized agents.

```

**Step 3: Verify the changes**

Run: `grep "Plan Adaptation" agents/tech-lead-software-architect.md`
Expected: Should find the new section

**Step 4: Commit Tech Lead update**

```bash
git add agents/tech-lead-software-architect.md
git commit -m "feat(agents): transform Atlas into Fairmind plan adapter

- Add all 40 Fairmind MCP tools (General + Studio + Code)
- Document plan adaptation workflow (generic → agent-specific)
- Add work package creation and format specification
- Add execution monitoring and coordination workflows
- Emphasize translation role (never implements code)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Phase B: Skills Creation

### Task 11: Create Skills Directory Structure

**Files:**
- Create: `skills/README.md`

**Step 1: Create skills directory**

```bash
mkdir -p skills
```

**Step 2: Create README.md**

Write: `skills/README.md`

```markdown
# Fairmind Skills

This directory contains standalone skills for Fairmind-aware development workflows.

## Available Skills

### 1. fairmind-context
**Purpose:** Reusable context gathering for any Fairmind development work
**Use when:** Starting any Fairmind-related development task
**Provides:** Project, session, user story, task, requirements, tests, and documentation context

### 2. fairmind-tdd
**Purpose:** Test-Driven Development aligned with Fairmind test plans and acceptance criteria
**Use when:** Implementing features with Fairmind acceptance criteria
**Requires:** fairmind-context as foundation

### 3. fairmind-code-review
**Purpose:** Systematic code review with plan→journal→code traceability
**Use when:** Reviewing implementation work done by development agents
**Requires:** fairmind-context as foundation

## Skill Philosophy

These skills are **standalone** and **purpose-built** for Fairmind workflows:
- Not wrappers around Fairmind tools (use tools directly when appropriate)
- Composable (fairmind-context is foundation for others)
- Focused on team collaboration and traceability
- Designed for agent-to-agent handoffs

## Usage Pattern

1. Development agents use `fairmind-context` + `fairmind-tdd` during implementation
2. Code reviewer uses `fairmind-code-review` to verify work
3. All agents update journals for traceability

```

**Step 3: Verify directory creation**

Run: `ls -la skills/`
Expected: Should show README.md

**Step 4: Commit skills directory**

```bash
git add skills/
git commit -m "feat(skills): create skills directory structure

- Add skills/ directory for Fairmind-aware skills
- Add README documenting skill philosophy and usage
- Prepare for fairmind-context, fairmind-tdd, fairmind-code-review

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 12: Create fairmind-context Skill

**Files:**
- Create: `skills/fairmind-context.md`

**Step 1: Write skill frontmatter and overview**

```markdown
---
name: fairmind-context
description: Use when starting any Fairmind development work - gathers full context including project, session, user story, task implementation plan, requirements, test expectations, and relevant documentation
---

# Fairmind Context Gathering

## Overview

Reusable context gathering for any Fairmind development work. This skill is the **foundation** for all other Fairmind skills.

**Announce at start:** "I'm using the fairmind-context skill to gather full context for this work."

## When to Use

Use this skill when:
- Starting any development task linked to Fairmind
- You have a task_id, user_story_id, or project_id
- You need to understand requirements and acceptance criteria
- You're preparing for implementation or code review

## Context Gathering Process

### Step 1: Identify Current Project

**If project_id provided:** Skip to Step 2

**If project_id not provided:**
1. Use `mcp__Fairmind__General_list_projects` to list available projects
2. Ask user which project (if ambiguous) or infer from current work context
3. Store project_id for subsequent calls

### Step 2: Identify Active Session

1. Use `mcp__Fairmind__General_list_work_sessions` with the project_id
2. Filter for active sessions (`is_active: true`)
3. If multiple active sessions, ask user to clarify
4. Store session_id for subsequent calls

### Step 3: Gather Task Context (if task_id available)

1. Use `mcp__Fairmind__Studio_get_task` with task_id
2. Extract:
   - Implementation plan
   - Task status
   - Assigned agent role
   - Dependencies

### Step 4: Gather User Story Context (if user_story_id available)

1. Use `mcp__Fairmind__Studio_get_user_story` with user_story_id
2. Extract:
   - Title and description
   - Acceptance criteria
   - Business requirements
3. Use `mcp__Fairmind__Studio_get_related_user_stories` to identify dependencies

### Step 5: Gather Requirements

1. If user_story_id available:
   - Use `mcp__Fairmind__Studio_list_functional_requirements_by_session`
   - Use `mcp__Fairmind__Studio_list_technical_requirements_by_session`
2. Alternative: Use `mcp__Fairmind__Studio_list_requirements_by_project` for project-wide requirements

### Step 6: Gather Test Expectations (if user_story_id available)

1. Use `mcp__Fairmind__Studio_list_tests_by_userstory`
2. Extract expected test coverage and test scenarios

### Step 7: Gather Documentation

1. Use `mcp__Fairmind__General_rag_retrieve_documents` with relevant queries:
   - Similar implementations
   - Architectural patterns
   - Technology-specific best practices
2. Use `mcp__Fairmind__General_get_document_content` for specific documents if needed

### Step 8: Cross-Project Context (if applicable)

If the work involves integration with another project:
1. Repeat Steps 1-7 for the target project
2. Use `mcp__Fairmind__Code_list_repositories` to identify target repositories
3. Use `mcp__Fairmind__Code_search` to understand integration points

## Output Structure

Present gathered context in this format:

```markdown
# Context for {Task/User Story}

## Project
- **ID**: {project_id}
- **Name**: {project_name}

## Session
- **ID**: {session_id}
- **Status**: {active/inactive}

## User Story
- **ID**: {user_story_id}
- **Title**: {title}
- **Description**: {description}
- **Acceptance Criteria**:
  1. {criterion_1}
  2. {criterion_2}
- **Related Stories**: {list of related story IDs}

## Task
- **ID**: {task_id}
- **Status**: {status}
- **Implementation Plan**:
  ```
  {plan details}
  ```

## Requirements
### Functional Requirements
- {FR-1}: {description}
- {FR-2}: {description}

### Technical Requirements
- {TR-1}: {description}
- {TR-2}: {description}

## Test Expectations
- {Test scenario 1}
- {Test scenario 2}
- Expected coverage: {percentage or scope}

## Documentation
- {Document 1}: {summary}
- {Document 2}: {summary}

## Integration Points (if cross-project)
- Target project: {name}
- Repositories: {list}
- API endpoints: {list}
```

## Next Steps

After gathering context:
- **For implementation**: Use `fairmind-tdd` skill
- **For code review**: Use `fairmind-code-review` skill
- **For debugging**: Use gathered context with debugging workflows

## Error Handling

**If project_id not found:**
- Ask user to provide project name or ID
- List available projects for selection

**If session not active:**
- Warn user that session may be ended
- Proceed with project-level context only

**If task_id or user_story_id not found:**
- Gather whatever context is available
- Inform user of missing context elements

```

**Step 2: Verify the skill file**

Run: `cat skills/fairmind-context.md | head -20`
Expected: Should show frontmatter and overview

**Step 3: Commit fairmind-context skill**

```bash
git add skills/fairmind-context.md
git commit -m "feat(skills): create fairmind-context skill

- Foundation skill for gathering Fairmind development context
- Gathers project, session, user story, task, requirements, tests
- Supports cross-project integration scenarios
- Structured output format for downstream skills
- Error handling for missing context elements

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 13: Create fairmind-tdd Skill

**Files:**
- Create: `skills/fairmind-tdd.md`

**Step 1: Write skill content**

```markdown
---
name: fairmind-tdd
description: Use when implementing features with Fairmind acceptance criteria - TDD workflow aligned with Fairmind test plans, implementation plans, and journal-based traceability
---

# Fairmind Test-Driven Development

## Overview

Test-Driven Development workflow aligned with Fairmind test plans and acceptance criteria. This skill ensures tests are **aligned with Fairmind acceptance criteria** (not invented) and implementation follows **plans from get_task** (not free-form).

**Announce at start:** "I'm using the fairmind-tdd skill to implement this feature with test-driven development."

**Dependencies:** Requires `fairmind-context` skill as foundation

## When to Use

Use this skill when:
- Implementing features with Fairmind acceptance criteria
- You have an implementation plan from Atlas or Fairmind
- You want to ensure test coverage matches expectations
- You need traceability from plan to implementation

## TDD Process with Fairmind

### SETUP PHASE

**Step 1: Gather context**

1. **REQUIRED SUB-SKILL:** Use `fairmind-context` skill to gather full context
2. Verify you have:
   - Implementation plan (from `Studio_get_task`)
   - Acceptance criteria (from user story)
   - Test expectations (from `Studio_list_tests_by_userstory`)

**Step 2: Understand what to build**

1. Read implementation plan carefully
2. Identify the **first** small unit of functionality
3. Check acceptance criteria alignment
4. Check test expectations from Fairmind

### RED PHASE

**Step 3: Write the failing test**

Write a test that:
- ✓ Aligns with Fairmind acceptance criteria (not invented)
- ✓ Follows implementation plan scope (no scope creep)
- ✓ Matches expected test coverage from `list_tests_by_userstory`
- ✓ Tests one small behavior (not multiple things)

Example:
```python
def test_user_can_login_with_valid_credentials():
    # Acceptance criterion: "Users can log in with email and password"
    result = login("user@example.com", "password123")
    assert result.success == True
    assert result.user_id is not None
```

**Step 4: Run test to verify it fails**

Run the test and verify:
- ✗ Test fails (no false positives)
- Failure message is clear (e.g., "function login not defined")

Document in terminal:
```
FAILED: test_user_can_login_with_valid_credentials
Expected failure: login function not yet implemented
```

### GREEN PHASE

**Step 5: Implement minimal code**

Write the **minimal** code to make the test pass:
- Follow the implementation plan
- Don't add extra features
- Don't over-engineer
- Just make the test green

Example:
```python
def login(email, password):
    # Minimal implementation to pass test
    if email and password:
        return LoginResult(success=True, user_id=1)
    return LoginResult(success=False, user_id=None)
```

**Step 6: Run test to verify it passes**

Run the test and verify:
- ✓ Test passes
- No other tests broken

Document in terminal:
```
PASSED: test_user_can_login_with_valid_credentials
All tests passing: 1/1
```

### REFACTOR PHASE

**Step 7: Clean up code**

Improve code quality while maintaining test passage:
- Remove duplication (DRY principle)
- Improve naming
- Extract functions/classes as needed
- Improve error handling
- **Keep tests green**

**Step 8: Run tests again**

Verify all tests still pass after refactoring.

### DOCUMENTATION PHASE

**Step 9: Update journal**

Update `fairmind/journals/{role}/{task_id}_*_journal.md` with:

```markdown
### {Timestamp} - Implemented {Feature Name}

**Implementation Plan Item**: {Which item from plan was completed}

**Test Added**:
- File: `{test_file_path}`
- Test name: `{test_name}`
- Aligned with acceptance criterion: "{criterion text}"

**Code Added**:
- File: `{implementation_file_path}`
- Function/class: `{name}`
- Lines: {start_line}-{end_line}

**Test Coverage**:
- ✓ Acceptance criterion X covered
- Test result: PASSED

**Next Steps**: {What's next from the plan}
```

**Step 10: Validate against Fairmind expectations**

Cross-check:
- ✓ Test aligns with acceptance criteria from user story?
- ✓ Implementation follows plan from `get_task`?
- ✓ Test coverage matches expectations from `list_tests_by_userstory`?
- ✓ Journal provides traceability (plan → test → code)?

### REPEAT FOR NEXT FEATURE

**Step 11: Continue with next unit**

Return to RED PHASE (Step 3) for the next small unit of functionality from the implementation plan.

## Key Differences from Generic TDD

| Generic TDD | Fairmind TDD |
|-------------|--------------|
| Invent test scenarios | Align with Fairmind acceptance criteria |
| Free-form implementation | Follow plan from `get_task` |
| No traceability requirement | Journal provides plan→test→code traceability |
| Test coverage subjective | Test coverage from `list_tests_by_userstory` |

## Completion Checklist

Before marking work complete, verify:

- [ ] All acceptance criteria have tests
- [ ] All tests pass
- [ ] Implementation follows plan
- [ ] Journal documents: plan items → tests → code
- [ ] Test coverage matches Fairmind expectations
- [ ] Code is refactored and clean
- [ ] No scope creep (only planned features implemented)

## Error Scenarios

**If acceptance criteria unclear:**
- Use `fairmind-context` to gather more details
- Ask Atlas for clarification
- Document ambiguity in journal

**If implementation plan missing:**
- Check work package from Atlas
- Ask Atlas to provide adapted plan
- Don't proceed without plan (prevents scope creep)

**If test expectations unavailable:**
- Use acceptance criteria as test guide
- Document assumption in journal
- Proceed with standard test coverage practices

```

**Step 2: Verify the skill file**

Run: `grep "RED PHASE" skills/fairmind-tdd.md`
Expected: Should find the section

**Step 3: Commit fairmind-tdd skill**

```bash
git add skills/fairmind-tdd.md
git commit -m "feat(skills): create fairmind-tdd skill

- TDD workflow aligned with Fairmind acceptance criteria
- RED-GREEN-REFACTOR cycle with Fairmind plan alignment
- Journal documentation for traceability
- Requires fairmind-context as foundation
- Prevents scope creep via plan adherence

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 14: Create fairmind-code-review Skill

**Files:**
- Create: `skills/fairmind-code-review.md`

**Step 1: Write skill content**

```markdown
---
name: fairmind-code-review
description: Use when reviewing implementation work - systematic code review with plan→journal→code traceability, requirements verification, and cross-repository integration checks
---

# Fairmind Code Review

## Overview

Systematic code review with three-layer verification: plan→journal→code traceability, requirements compliance, and cross-repository integration validation.

**Announce at start:** "I'm using the fairmind-code-review skill to review this implementation."

**Dependencies:** Requires `fairmind-context` skill as foundation

## When to Use

Use this skill when:
- Reviewing implementation work by development agents
- Verifying work aligns with Fairmind plans and requirements
- Checking for scope creep or missing features
- Validating cross-repository integrations

## Three-Layer Review Process

### LAYER 1: Plan Verification

**Step 1: Retrieve implementation plan**

1. Use `mcp__Fairmind__Studio_get_task` to get the original implementation plan
2. Note: If Atlas adapted the plan, also check `fairmind/work_packages/{role}/{task_id}_*_workpackage.md`

**Step 2: Read agent journal**

1. Read `fairmind/journals/{role}/{task_id}_*_journal.md`
2. Extract:
   - What was implemented
   - Which plan items were addressed
   - What files were modified
   - What decisions were made

**Step 3: Compare plan vs journal**

Create comparison checklist:

```markdown
## Plan Compliance

### Planned Features
- ✓ Feature X from plan → Journal entry: "Implemented X in file.ts:42"
- ✓ Feature Y from plan → Journal entry: "Completed Y with tests in test.ts:15"
- ✗ Feature Z from plan → **Missing from journal** (not implemented)
- ⚠ Feature W in journal → **Not in original plan** (scope creep?)

### Assessment
- Planned items completed: X/Y (percentage)
- Missing items: {list}
- Extra items (scope creep): {list}
```

**If discrepancies found:**
- Flag missing planned items
- Question extra unplanned items
- Ask agent or Atlas for clarification

### LAYER 2: Requirements Verification

**Step 4: Gather requirements and acceptance criteria**

1. **REQUIRED SUB-SKILL:** Use `fairmind-context` to gather:
   - User story acceptance criteria
   - Functional requirements
   - Technical requirements
   - Test coverage expectations

**Step 5: Build verification checklist**

Create checklist from gathered context:

```markdown
## Requirements Compliance

### User Story Acceptance Criteria
- ✓ AC-1: Users can log in with email and password
  - Verified in: `auth.ts:login()` + test `test_login.ts`
- ✗ AC-2: Users receive error message for invalid credentials
  - **Missing**: No error handling implemented
- ✓ AC-3: Users are redirected to dashboard after login
  - Verified in: `auth.ts:handleLoginSuccess()`

### Functional Requirements
- ✓ FR-123: Session timeout after 30 minutes
  - Verified in: `session.ts:startTimeout()`
- ✗ FR-456: Input validation for email format
  - **Missing**: No email validation found

### Technical Requirements
- ✓ TR-789: Use bcrypt for password hashing
  - Verified in: `auth.ts:hashPassword()`
- ⚠ TR-012: Log authentication attempts
  - **Partially implemented**: Logging only for failures, not successes

### Test Coverage
- ✓ Test scenarios from `list_tests_by_userstory` covered
- Test count: 8/10 expected tests present
- **Missing tests**: Invalid email format, session timeout edge cases
```

**Step 6: Review code against checklist**

For each checklist item:
1. Find corresponding code implementation
2. Verify it meets the requirement
3. Check for edge cases and error handling
4. Mark as ✓ (complete), ✗ (missing), or ⚠ (partial)

### LAYER 3: Cross-Repository Verification

**Step 7: Identify integration points**

From implementation plan and journal:
1. Identify services/repositories being integrated
2. List API endpoints being called
3. Note data contracts being used

**If no integrations:** Skip to Step 11

**Step 8: List target repositories**

Use `mcp__Fairmind__Code_list_repositories` to identify target services

**Step 9: Verify API contracts**

For each integration point:
1. Use `mcp__Fairmind__Code_search` to find API endpoint definitions
2. Use `mcp__Fairmind__Code_cat` to read API documentation or interface definitions
3. Compare implementation vs contract:
   - Request format matches?
   - Response handling correct?
   - Error handling appropriate?

**Step 10: Check for breaking changes**

1. Use `mcp__Fairmind__Code_find_usages` to see how the API is used elsewhere
2. Verify changes don't break existing integrations
3. Check API versioning if applicable

Example verification:

```markdown
## Integration Check

### Auth Service Integration
- **API endpoint**: `POST /auth/login`
- **Contract location**: `auth-service/src/api/auth.ts:42`
- ✓ Request format matches contract
- ✓ Response handling correct
- ⚠ Error handling missing for 429 (rate limit) response

### Payment Service Integration
- **API endpoint**: `GET /payments/user/{id}`
- ⚠ **New dependency not in original plan**
- Need to verify with Atlas: Was this approved?
- Contract verified: Correctly implemented

### Shared Library
- **Library**: `@company/ui-components`
- ✓ Using correct version (v2.3.1)
- ✓ Component API usage matches documentation
```

## Review Output

**Step 11: Compile review report**

Present findings in structured format:

```markdown
# Code Review: {Task ID}

**Reviewer**: {Your name/agent}
**Date**: {review_date}
**Agent reviewed**: {AI/Backend/Frontend Engineer}
**Status**: {APPROVED / CHANGES REQUESTED / BLOCKED}

---

## Executive Summary
{1-2 sentence overview of review findings}

## Plan Compliance
{From Layer 1: Step 3 output}

## Requirements Compliance
{From Layer 2: Step 5 output}

## Integration Check
{From Layer 3: Step 10 output, if applicable}

---

## Critical Issues (Must Fix)
1. {Missing acceptance criterion AC-2: error handling}
2. {Missing functional requirement FR-456: input validation}
3. {Breaking change in payment service integration}

## Warnings (Should Fix)
1. {Partial technical requirement TR-012: incomplete logging}
2. {Unplanned payment service dependency needs approval}

## Recommendations
1. Implement missing acceptance criteria before merging
2. Add missing functional requirements
3. Clarify payment service integration with Atlas
4. Complete logging implementation per TR-012
5. Add missing test cases for edge scenarios

---

## Approval Status

**Decision**: CHANGES REQUESTED

**Reasoning**:
- Critical acceptance criteria missing (AC-2)
- Functional requirement missing (FR-456)
- Unplanned dependency needs architectural review

**Next Steps**:
1. Agent to address critical issues
2. Atlas to review payment service integration
3. Re-review after changes implemented
```

**Step 12: Communicate findings**

Share review report with:
- The agent who did the work
- Atlas (for architectural concerns)
- Project stakeholders (if critical issues found)

## Key Differences from Generic Code Review

| Generic Code Review | Fairmind Code Review |
|---------------------|---------------------|
| Subjective quality checks | Three-layer verification (plan→journal→code) |
| Generic best practices | Requirements from Fairmind |
| Manual integration checks | Cross-repo verification with Code tools |
| No traceability requirement | Full traceability via journal |

## Review Decision Criteria

**APPROVED:**
- ✓ All planned features implemented
- ✓ All acceptance criteria met
- ✓ All requirements satisfied
- ✓ Test coverage complete
- ✓ No critical issues
- ✓ Integrations verified

**CHANGES REQUESTED:**
- Missing planned features
- Missing acceptance criteria
- Missing requirements
- Incomplete test coverage
- Critical issues found
- Integration issues detected

**BLOCKED:**
- Architectural concerns require Atlas review
- Unplanned major changes need approval
- Breaking changes detected in integrations
- Security vulnerabilities found

## Error Scenarios

**If implementation plan missing:**
- Request plan from Atlas
- Use generic code review practices
- Document lack of plan in review report

**If journal missing or incomplete:**
- Flag to agent: journal is required for traceability
- Request journal update before continuing review
- Cannot verify plan compliance without journal

**If requirements unclear:**
- Use `fairmind-context` to gather more details
- Ask Atlas for requirement clarification
- Document ambiguity in review report

```

**Step 2: Verify the skill file**

Run: `grep "LAYER 1: Plan Verification" skills/fairmind-code-review.md`
Expected: Should find the section

**Step 3: Commit fairmind-code-review skill**

```bash
git add skills/fairmind-code-review.md
git commit -m "feat(skills): create fairmind-code-review skill

- Three-layer verification (plan→journal→code)
- Requirements compliance checking against Fairmind
- Cross-repository integration verification using Code tools
- Structured review output with approval criteria
- Requires fairmind-context as foundation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 15: Integration Testing

**Files:**
- Create: `docs/testing/integration-test-fairmind-workflow.md`

**Step 1: Write integration test plan**

```markdown
# Fairmind Integration Test Plan

## Purpose
Verify the complete workflow: Atlas → Dev Agent (using fairmind-tdd) → Code Review (using fairmind-code-review)

## Test Scenario

### Simulated Fairmind Task
Create a mock Fairmind task with:
- User story with acceptance criteria
- Implementation plan
- Functional and technical requirements
- Test expectations

### Workflow Steps

#### Step 1: Atlas Adapts Plan
1. Atlas retrieves mock Fairmind task
2. Atlas analyzes requirements
3. Atlas creates work package for Backend Engineer
4. Atlas writes to `fairmind/work_packages/backend/TEST-001_backend_workpackage.md`

**Verification:**
- [ ] Work package file created
- [ ] Work package contains adapted plan
- [ ] Work package includes file paths and tech-specific guidance

#### Step 2: Backend Engineer Implements (using fairmind-tdd)
1. Backend Engineer reads work package
2. Backend Engineer uses `fairmind-context` skill to gather context
3. Backend Engineer uses `fairmind-tdd` skill to implement
4. Backend Engineer updates journal throughout
5. Backend Engineer creates completion flag

**Verification:**
- [ ] Context gathered successfully
- [ ] RED-GREEN-REFACTOR cycle followed
- [ ] Tests written aligned with acceptance criteria
- [ ] Implementation follows plan
- [ ] Journal documents traceability
- [ ] Completion flag created

#### Step 3: Code Reviewer Reviews (using fairmind-code-review)
1. Code Reviewer uses `fairmind-code-review` skill
2. Code Reviewer performs three-layer verification
3. Code Reviewer compiles review report
4. Code Reviewer decides: APPROVED / CHANGES REQUESTED / BLOCKED

**Verification:**
- [ ] Plan compliance verified
- [ ] Requirements compliance checked
- [ ] Journal→code traceability validated
- [ ] Review report generated
- [ ] Approval decision documented

## Success Criteria

- ✓ Complete workflow executes without errors
- ✓ Each agent follows appropriate skill
- ✓ Traceability maintained: plan → journal → code → review
- ✓ All Fairmind MCP tools accessed successfully
- ✓ Skills compose correctly (fairmind-context → fairmind-tdd/fairmind-code-review)

## Test Data

Create mock files in `docs/testing/mock-fairmind-data/`:
- `mock-user-story.json`
- `mock-task.json`
- `mock-requirements.json`
- `mock-test-expectations.json`

## Execution

Run test manually with three separate agent sessions:
1. Session 1: Atlas (Tech Lead agent)
2. Session 2: Backend Engineer agent
3. Session 3: Code Reviewer agent

Document results in `docs/testing/integration-test-results.md`

```

**Step 2: Create mock test data directory**

```bash
mkdir -p docs/testing/mock-fairmind-data
```

**Step 3: Verify integration test plan**

Run: `cat docs/testing/integration-test-fairmind-workflow.md | head -10`
Expected: Should show the plan header

**Step 4: Commit integration test plan**

```bash
git add docs/testing/
git commit -m "feat(testing): add Fairmind integration test plan

- Document complete workflow test (Atlas → Dev → Code Review)
- Specify verification steps for each workflow stage
- Include success criteria and test data structure
- Enable manual testing of agent-to-agent handoffs

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Verification & Completion

### Task 16: Final Verification

**Step 1: Verify all agent files updated**

Run:
```bash
for agent in ai-engineer backend-engineer frontend-engineer qa-engineer code-reviewer cybersec-engineer debug-detective backend-issue-fixer frontend-issue-fixer tech-lead-software-architect; do
  echo "=== $agent ==="
  grep -c "mcp__Fairmind" "agents/$agent.md" || echo "MISSING Fairmind tools"
done
```

Expected: Each agent shows count > 0 (except playwright-issue-analyzer and pr-diff-documenter which weren't changed)

**Step 2: Verify all skills created**

Run:
```bash
ls -la skills/*.md
```

Expected: Should show:
- fairmind-context.md
- fairmind-tdd.md
- fairmind-code-review.md

**Step 3: Verify documentation structure**

Run:
```bash
tree docs/ -L 2
```

Expected: Should show:
- docs/plans/ (with design and implementation plan)
- docs/testing/ (with integration test plan)

**Step 4: Run git status**

Run:
```bash
git status
```

Expected: Working tree clean (all changes committed)

**Step 5: Review commit history**

Run:
```bash
git log --oneline --graph -n 20
```

Expected: Should show all 16 commits from this implementation

---

## Plan Complete

This plan provides bite-sized tasks for:
- **Phase A**: Updating 12 agents with Fairmind MCP tools (Tasks 1-10)
- **Phase B**: Creating 3 standalone Fairmind skills (Tasks 11-14)
- **Integration Testing**: Testing the complete workflow (Task 15)
- **Verification**: Ensuring all changes are complete (Task 16)

Each task includes:
- Exact file paths
- Step-by-step instructions
- Verification commands with expected output
- Commit messages following conventions

Total estimated time: 4-6 hours for complete implementation and testing.
