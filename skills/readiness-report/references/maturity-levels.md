# Maturity Levels Framework

This document defines the five-tier progression system for repository maturity, describing what each level represents and the agent capabilities it enables.

## Progression Rules

1. **80% threshold**: Pass >=80% of criteria at a level to unlock it
2. **Cumulative requirement**: All previous levels must also meet 80%
3. **Binary scoring**: Criteria are pass/fail with no partial credit
4. **Skipped criteria excluded**: Inapplicable criteria don't count toward totals

## Level Overview

| Level | Name | Criteria | Agent Capability |
|-------|------|----------|------------------|
| L1 | Initial | 10 | Manual assistance only |
| L2 | Managed | 21 | Simple, well-defined tasks |
| L3 | Standardized | 26 | Routine maintenance |
| L4 | Measured | 16 | Complex features |
| L5 | Optimized | 7 | End-to-end development |

---

## Level 1: Initial

**Focus**: Basic version control and code quality tooling

### Requirements (10 criteria)
- Formatter configured
- Linter configured
- Type checking enabled
- README exists
- Build commands documented
- Dependencies pinned
- VCS CLI authenticated
- Unit tests exist
- Test commands documented
- Comprehensive .gitignore

### Agent Capability
At L1, agents can:
- Read and understand code
- Make simple edits
- All changes require manual verification

### Key Gaps at L1
- No feedback loops (manual testing)
- No CI/CD automation
- Limited documentation

---

## Level 2: Managed

**Focus**: CI/CD automation and basic documentation

### Requirements (21 criteria)
All L1 criteria plus:
- Strict typing enabled
- Pre-commit hooks configured
- Naming conventions enforced
- Large file detection
- CI workflow configured
- Single-command setup documented
- Release automation
- Regular deployment frequency
- AGENTS.md exists
- Documentation freshness
- Environment template
- Structured logging
- Code quality metrics
- Secrets management
- CODEOWNERS configured
- Branch protection
- Issue templates
- Issue labeling system
- PR templates
- Test naming conventions
- Test isolation/parallelism

### Agent Capability
At L2, agents can:
- Handle simple, well-defined tasks
- Get rapid feedback from CI
- Execute tests independently
- Create PRs that pass basic checks

### Key Gaps at L2
- No integration/E2E testing
- Limited observability
- No security automation

---

## Level 3: Standardized

**Focus**: Production-ready automation

### Requirements (26 criteria)
All L1-L2 criteria plus:
- Code modularization enforced
- Cyclomatic complexity checked
- Dead code detection
- Duplicate code detection
- Release notes automation
- AI agent commits evident
- Automated PR review
- Feature flag infrastructure
- Integration tests exist
- Test coverage thresholds
- API schema documentation
- Automated doc generation
- Architecture documented
- Skills directory exists
- Devcontainer configured
- Devcontainer runnable
- Database schema managed
- Local services setup
- Error tracking configured
- Distributed tracing
- Metrics collection
- Health checks implemented
- Dependency update automation
- Log scrubbing
- PII handling
- Contributing guidelines

### Agent Capability
At L3, agents can:
- Handle routine maintenance
- Perform dependency upgrades
- Execute bug fixes and routine tasks
- Implement features with clear specifications
- Work on multiple related files

### Key Gaps at L3
- Performance optimization blind spots
- Security automation limited
- Advanced debugging tools missing

---

## Level 4: Measured

**Focus**: Advanced tooling and comprehensive automation

### Requirements (16 criteria)
All L1-L3 criteria plus:
- Tech debt tracking
- N+1 query detection
- Build performance tracking
- Heavy dependency detection
- Unused dependency detection
- Dead feature flag detection
- Monorepo tooling (if applicable)
- Version drift detection (if applicable)
- Flaky test detection
- Test performance tracking
- AGENTS.md validation
- Profiling instrumentation
- Alerting configured
- Deployment observability
- Runbooks documented
- Automated security review
- Secret scanning

### Agent Capability
At L4, agents can:
- Handle complex multi-file refactors
- Optimize performance bottlenecks
- Implement architectural improvements
- Navigate complex codebases efficiently
- Self-diagnose issues with observability tools

### Key Gaps at L4
- Production deployment autonomy
- Privacy/compliance automation
- Circuit breaker patterns

---

## Level 5: Optimized

**Focus**: Full autonomous development capability

### Requirements (7 criteria)
All L1-L4 criteria plus:
- Progressive rollout
- Rollback automation
- Circuit breakers
- DAST scanning
- Privacy compliance documented
- Error-to-insight pipeline
- Product analytics instrumentation

### Agent Capability
At L5, agents can:
- Handle end-to-end development
- Deploy to production autonomously
- Respond to incidents automatically
- Drive product improvements from analytics
- Maintain continuous compliance

### Characteristics
This level is rarely achieved and represents mature, well-instrumented systems where AI agents can operate with minimal human oversight.

---

## Strategic Improvement Path

### Priority Order

1. **Fix L1 gaps first**: These block basic agent operation
2. **Establish L2 feedback loops**: Fast CI enables iteration
3. **Target L3 as baseline**: This is the "production-ready" target
4. **L4+ as optimization**: Advanced tooling for complex work

### Common Progression Blockers

| Blocker | Impact | Solution |
|---------|--------|----------|
| No AGENTS.md | Agents lack context | Document commands and architecture |
| No pre-commit | Slow feedback | Configure hooks for fast checks |
| No tests | Can't verify changes | Add unit tests for critical paths |
| No CI | Manual verification | Set up basic workflow |
| No devcontainer | "Works on my machine" | Define reproducible environment |

### Organization-Level Assessment

For multi-repo organizations:
- **Repo Score**: (passed criteria / applicable criteria) × 100%
- **Org Level**: floor(average repository levels)
- **Key Metric**: % of active repos at L3+

Target: 80% of repositories at L3+ for production-ready agent capability across the organization.

---

## Score Calculation Example

```
Repository: my-web-app
Type: application
Languages: TypeScript

L1 Criteria: 10 total, 8 passed = 80% ✓
L2 Criteria: 21 total, 18 passed = 86% ✓
L3 Criteria: 26 total, 19 passed = 73% ✗
L4 Criteria: 16 total, 5 passed = 31%
L5 Criteria: 7 total, 0 passed = 0%

Achieved Level: L2
Overall Pass Rate: 50/80 = 62.5%

To reach L3: Need 2 more L3 criteria (73% → 80%)
Priority: integration_tests_exist, test_coverage_thresholds
```
