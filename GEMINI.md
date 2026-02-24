# FairMind Integration Extension for Gemini CLI

This extension provides team collaboration with 6 role-based agents and 9 technology-specific skills for FairMind-powered development workflows.

## Agents

| Agent | Role | When to Use |
|-------|------|-------------|
| Atlas (Tech Lead) | Orchestration & coordination | Start of any FairMind task |
| Echo (Software Engineer) | Implementation | All coding work |
| Tess (QA Test Executor) | Test execution | After implementation |
| Echo (Code Reviewer) | Code quality review | After implementation |
| Debug Detective | Bug investigation | Complex debugging |
| Shield (Cybersecurity) | Security validation | Final validation gate |

## Skills (Auto-discovered)

Skills are loaded dynamically by agents. Available skills:
- `fairmind-context` — Context gathering foundation
- `fairmind-tdd` — Test-driven development with FairMind alignment
- `fairmind-code-review` — 3-layer code review
- `frontend-react-nextjs` — React, NextJS, TypeScript, Tailwind, Shadcn UI
- `backend-nextjs` — NextJS API routes, MongoDB, authentication
- `backend-python` — FastAPI, Pydantic, async patterns
- `backend-langchain` — LangChain, LangGraph, RAG systems
- `qa-playwright` — Playwright test patterns and automation
- `ai-ml-systems` — AI/ML architecture and optimization

## MCP Server Setup

Configure the FairMind MCP server in your `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "Fairmind": {
      "url": "https://project-context.mindstream.fairmind.ai/mcp/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_FAIRMIND_API_KEY"
      }
    }
  }
}
```

## Key Conventions

- All agent work is tracked in `.fairmind/journals/`
- Work packages are distributed via `.fairmind/work_packages/`
- Validation results go to `.fairmind/validation_results/`
- Atlas never implements code — only orchestrates
- Every agent must maintain a journal (mandatory)
