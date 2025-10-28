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
