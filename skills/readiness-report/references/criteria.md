# Agent Readiness Criteria

This document defines the 81 binary criteria evaluated across nine technical pillars. Each criterion has an ID, maturity level (1-5), and describes what signals it detects and the impact of failure.

## Evaluation Rules

- **Binary scoring**: Each criterion is pass/fail with no partial credit
- **Context-aware skipping**: Criteria are skipped when not applicable to the repository type
- **Level gating**: To achieve a level, pass >=80% of that level's criteria AND all previous levels

---

## Pillar 1: Style & Validation (13 criteria)

Automated tooling that catches bugs and enforces consistency. Without them, agents waste cycles on syntax errors and style drift.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `formatter` | L1 | Prettier, Black, Ruff, gofmt config exists | Agent produces inconsistent formatting |
| `lint_config` | L1 | ESLint, Pylint, golangci-lint config exists | Bugs slip through that linter would catch |
| `type_check` | L1 | tsconfig.json, mypy config, or statically typed language | Runtime type errors in production |
| `strict_typing` | L2 | `strict: true` in tsconfig or mypy config | Partial type safety leaves gaps |
| `pre_commit_hooks` | L2 | .pre-commit-config.yaml or .husky exists | Style issues reach CI, slow feedback |
| `naming_consistency` | L2 | Naming conventions in linter or AGENTS.md | Inconsistent naming confuses agents |
| `large_file_detection` | L2 | .gitattributes, .lfsconfig, or pre-commit check | Binary bloat in repository |
| `code_modularization` | L3 | import-linter, nx, or Bazel boundaries | Circular dependencies, tight coupling |
| `cyclomatic_complexity` | L3 | gocyclo, mccabe, radon in config | Complex functions that are hard to modify |
| `dead_code_detection` | L3 | vulture, knip, or deadcode in CI | Unused code accumulates |
| `duplicate_code_detection` | L3 | jscpd, PMD CPD, or SonarQube in CI | DRY violations accumulate |
| `tech_debt_tracking` | L4 | TODO/FIXME tracking in CI | Technical debt not visible |
| `n_plus_one_detection` | L4 | nplusone, bullet, query-analyzer in deps | Performance issues from ORM misuse |

---

## Pillar 2: Build System (19 criteria)

Fast, reliable builds that enable rapid iteration. Slow CI kills agent productivity.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `build_cmd_doc` | L1 | Build commands in README or AGENTS.md | Agent doesn't know how to build |
| `deps_pinned` | L1 | Lockfile exists (package-lock, poetry.lock, etc.) | Non-reproducible builds |
| `vcs_cli_tools` | L1 | gh/glab auth status succeeds | Agent can't interact with VCS |
| `fast_ci_feedback` | L2 | CI workflow configuration exists | Slow feedback slows iteration |
| `single_command_setup` | L2 | Setup command documented | Manual setup steps fail |
| `release_automation` | L2 | Release/publish workflow exists | Manual release process |
| `deployment_frequency` | L2 | Evidence of regular deployments | Infrequent releases increase risk |
| `release_notes_automation` | L3 | Changelog automation in CI | Manual release notes |
| `agentic_development` | L3 | AI agent co-author commits found | No agent contribution history |
| `automated_pr_review` | L3 | Danger.js or PR review automation | Manual PR review bottleneck |
| `feature_flag_infrastructure` | L3 | Feature flag service in deps | Features coupled to deployments |
| `build_performance_tracking` | L4 | Turbo, Nx build caching | Slow builds, no optimization |
| `heavy_dependency_detection` | L4 | Bundle analyzer, size-limit in deps | Large bundles, slow loads |
| `unused_dependencies_detection` | L4 | depcheck, deptry in CI | Bloated dependencies |
| `dead_feature_flag_detection` | L4 | Stale flag detection | Dead flags accumulate |
| `monorepo_tooling` | L4 | Lerna, Nx, Turbo, pnpm workspaces | No monorepo coordination |
| `version_drift_detection` | L4 | Dependency version consistency | Inconsistent package versions |
| `progressive_rollout` | L5 | Canary/gradual rollout config | All-or-nothing deployments |
| `rollback_automation` | L5 | Automated rollback mechanism | Manual incident response |

---

## Pillar 3: Testing (8 criteria)

Automated tests that verify correctness. Without them, agents can't validate their own work.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `unit_tests_exist` | L1 | Test files exist (tests/, spec/, etc.) | No automated verification |
| `unit_tests_runnable` | L1 | Test command documented | Agent can't run tests |
| `test_naming_conventions` | L2 | pytest, jest config or Go conventions | Inconsistent test organization |
| `test_isolation` | L2 | Parallel test support (xdist, matrix) | Slow test runs, flaky tests |
| `integration_tests_exist` | L3 | e2e/, integration/, cypress/, playwright config | Integration issues not caught |
| `test_coverage_thresholds` | L3 | Coverage reporting in CI | Regression risk unknown |
| `flaky_test_detection` | L4 | Retry/quarantine logic in CI | Flaky tests block CI |
| `test_performance_tracking` | L4 | Test duration tracking | Slow tests not identified |

---

## Pillar 4: Documentation (8 criteria)

Knowledge that guides the agent. Missing docs mean wasted exploration.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `readme` | L1 | README.md exists | No project overview |
| `agents_md` | L2 | AGENTS.md or CLAUDE.md exists | No agent-specific guidance |
| `documentation_freshness` | L2 | Recent README commits | Stale documentation |
| `api_schema_docs` | L3 | OpenAPI, GraphQL schema, API docs | API contracts unclear |
| `automated_doc_generation` | L3 | Docs generation in CI | Manual doc maintenance |
| `service_flow_documented` | L3 | Architecture diagrams or mermaid files | System design unclear |
| `skills` | L3 | .claude/skills or similar exists | No reusable agent workflows |
| `agents_md_validation` | L4 | AGENTS.md validation in CI | Docs drift from reality |

---

## Pillar 5: Dev Environment (5 criteria)

Reproducible environments that prevent "works on my machine" issues.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `env_template` | L2 | .env.example or env docs exist | Missing environment variables |
| `devcontainer` | L3 | .devcontainer/devcontainer.json exists | Non-reproducible dev setup |
| `devcontainer_runnable` | L3 | Devcontainer has valid image | Broken devcontainer |
| `database_schema` | L3 | Migrations directory exists | Schema changes not tracked |
| `local_services_setup` | L3 | docker-compose.yml exists | External deps not runnable locally |

---

## Pillar 6: Debugging & Observability (11 criteria)

Runtime visibility for diagnosing issues. Without them, agents can't debug effectively.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `structured_logging` | L2 | Logging library in deps | Unstructured logs hard to parse |
| `code_quality_metrics` | L2 | Coverage/quality in CI | Code quality not tracked |
| `error_tracking_contextualized` | L3 | Sentry, Bugsnag, etc. in deps | Errors not captured |
| `distributed_tracing` | L3 | OpenTelemetry, Jaeger, etc. in deps | Cross-service issues hard to trace |
| `metrics_collection` | L3 | Prometheus, Datadog, etc. in deps | Performance not monitored |
| `health_checks` | L3 | Health/ready/alive endpoints found | Service status unknown |
| `profiling_instrumentation` | L4 | Profiler in deps | Performance bottlenecks invisible |
| `alerting_configured` | L4 | Alert rules or alertmanager config | Issues not proactively detected |
| `deployment_observability` | L4 | Deploy notifications in CI | Deployment impact unknown |
| `runbooks_documented` | L4 | runbooks/ directory exists | Incident response unclear |
| `circuit_breakers` | L5 | Resilience library in deps | Cascading failures possible |

---

## Pillar 7: Security (11 criteria)

Protections for the codebase and data.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `gitignore_comprehensive` | L1 | .gitignore covers common patterns | Secrets or junk committed |
| `secrets_management` | L2 | secrets.* used in workflows | Hardcoded secrets |
| `codeowners` | L2 | CODEOWNERS file exists | No code ownership |
| `branch_protection` | L2 | Branch protection config | Unreviewed code merged |
| `dependency_update_automation` | L3 | Dependabot or Renovate config | Vulnerable deps not updated |
| `log_scrubbing` | L3 | Redaction in logging config | PII in logs |
| `pii_handling` | L3 | Redact/sanitize patterns in code | PII exposure risk |
| `automated_security_review` | L4 | CodeQL, Snyk, etc. in CI | Vulnerabilities not detected |
| `secret_scanning` | L4 | gitleaks, trufflehog in CI | Committed secrets not detected |
| `dast_scanning` | L5 | OWASP ZAP, DAST in CI | Runtime vulnerabilities not tested |
| `privacy_compliance` | L5 | Privacy documentation exists | Compliance gaps |

---

## Pillar 8: Task Discovery (4 criteria)

Structured task management that helps agents find work.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `issue_templates` | L2 | .github/ISSUE_TEMPLATE exists | Inconsistent issue format |
| `issue_labeling_system` | L2 | Labels in issue templates | No issue categorization |
| `pr_templates` | L2 | Pull request template exists | Inconsistent PR format |
| `backlog_health` | L3 | CONTRIBUTING.md exists | Contribution process unclear |

---

## Pillar 9: Product & Analytics (2 criteria)

User behavior insights that connect failures to improvements.

| ID | Level | Detection | Failure Impact |
|----|-------|-----------|----------------|
| `error_to_insight_pipeline` | L5 | Error-to-issue automation | Errors don't become tasks |
| `product_analytics_instrumentation` | L5 | Analytics SDK in deps | User behavior unknown |

---

## Context-Aware Skipping

Criteria are skipped when not applicable:

**Libraries** skip:
- health_checks, progressive_rollout, rollback_automation
- dast_scanning, alerting_configured, deployment_observability
- metrics_collection, profiling_instrumentation, circuit_breakers
- distributed_tracing, local_services_setup, database_schema
- n_plus_one_detection, privacy_compliance, pii_handling

**CLI Tools** skip:
- dast_scanning, health_checks, progressive_rollout

**Database Projects** skip:
- n_plus_one_detection, dast_scanning

**Non-Monorepos** skip:
- monorepo_tooling, version_drift_detection

**Prerequisite Dependencies**:
- devcontainer_runnable requires devcontainer
- agents_md_validation requires agents_md
- dead_feature_flag_detection requires feature_flag_infrastructure
