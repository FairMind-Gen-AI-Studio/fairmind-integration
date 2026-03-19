# FairMind Integration — OpenAI Codex Port

Porting plan for adapting the FairMind Claude Code plugin to OpenAI Codex CLI.

## Architecture Mapping

| Claude Code | Codex CLI | Notes |
|---|---|---|
| `CLAUDE.md` | `AGENTS.md` | Custom instructions, same Markdown format |
| `agents/*.md` | `.codex/agents/*.toml` | Role-based agents → TOML custom agents |
| `skills/*/SKILL.md` | `skills/*/SKILL.md` | Same format, natively supported by Codex |
| `hooks/hooks.json` | `config.toml` + sandbox rules | Different mechanism, needs adaptation |
| `commands/*.md` | Skills or prompt templates | Slash commands → Codex skills |
| `plugin.json` | `config.toml` metadata | Plugin metadata → Codex config |

## Agents to Port (6)

Each Claude Code agent `.md` file maps to a Codex `.toml` custom agent under `.codex/agents/`:

| Agent | Claude File | Codex File | Model Hint |
|---|---|---|---|
| Atlas (Tech Lead) | `agents/tech-lead.md` | `.codex/agents/atlas.toml` | High capability |
| Echo (Software Engineer) | `agents/software-engineer.md` | `.codex/agents/echo.toml` | High capability |
| Tess (QA Engineer) | `agents/qa-engineer.md` | `.codex/agents/tess.toml` | Medium capability |
| Code Reviewer | `agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` | High capability |
| Debug Detective | `agents/debug-detective.md` | `.codex/agents/debug-detective.toml` | High capability |
| Shield (Cybersecurity) | `agents/cybersec-engineer.md` | `.codex/agents/shield.toml` | High capability |

### TOML Agent Format

```toml
name = "atlas"
description = "Tech Lead and Software Architect. Orchestrates work, creates work packages, delegates to specialized agents."

[developer_instructions]
text = """
... (ported from agents/tech-lead.md)
"""

model = "o3"
sandbox_mode = "workspace-write"

nickname_candidates = ["Atlas", "Architect", "Lead"]
```

## Skills to Port (9)

Skills use the same `SKILL.md` format in both platforms — minimal changes needed:

1. `fairmind-context` — Context gathering from FairMind MCP
2. `fairmind-tdd` — TDD workflow aligned with FairMind acceptance criteria
3. `fairmind-code-review` — Three-layer code review
4. `frontend-react-nextjs` — React/NextJS/TypeScript/Tailwind patterns
5. `backend-nextjs` — NextJS API routes/MongoDB patterns
6. `backend-python` — FastAPI/Pydantic patterns
7. `backend-langchain` — LangChain/LangGraph/RAG patterns
8. `qa-playwright` — Playwright E2E testing
9. `ai-ml-systems` — Multi-agent architecture/LLM optimization

## Hooks Adaptation

| Claude Hook | Codex Equivalent |
|---|---|
| `PreToolUse(Write\|Edit)` path validation | Sandbox rules in `config.toml` + `AGENTS.md` instructions |
| `PreToolUse(Task)` context injection | Custom agent `developer_instructions` + startup script |
| `Stop` journal enforcement | `AGENTS.md` instructions + post-task validation skill |

## Commands to Port (20)

Slash commands can be ported as Codex Skills (directory with `SKILL.md`):

Priority P0 (core workflow):
- `/fix-issue`, `/gh-commit`, `/gh-review-pr`, `/pr-review`

Priority P1 (development):
- `/make-tests`, `/fix-frontend-issue`, `/gh-address-pr-comments`, `/gh-fix-ci`

Priority P2 (utilities):
- `/docs`, `/de-slop`, `/report`, `/ultra-think`

Priority P3 (specialized):
- `/security-audit`, `/performance-audit`, `/sonarqube-fix`, etc.

## Key Differences to Handle

1. **Tool names**: Claude `Task` → Codex `spawn_agent` / `wait_agent`
2. **MCP integration**: Both support MCP servers, config syntax differs
3. **Sandbox model**: Codex has `read-only` / `workspace-write` / `full-auto`
4. **Model references**: Claude models → OpenAI models (o3, gpt-5.3-codex, etc.)
5. **Subagent orchestration**: Claude uses `Task` tool, Codex uses explicit `spawn_agent`

## Implementation Order

1. **Phase 1**: Create `AGENTS.md` (port from `CLAUDE.md`)
2. **Phase 2**: Port 6 agents to `.codex/agents/*.toml`
3. **Phase 3**: Adapt 9 skills (mostly copy, adjust tool references)
4. **Phase 4**: Port P0 commands as Codex skills
5. **Phase 5**: Adapt hooks to Codex sandbox + instructions
6. **Phase 6**: Port remaining commands (P1-P3)
7. **Phase 7**: Integration testing with FairMind MCP server
