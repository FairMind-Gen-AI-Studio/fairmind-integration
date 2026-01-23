#!/usr/bin/env python3
"""
Repository Readiness Analyzer

Analyzes a repository across eight technical pillars to determine
agent readiness. Outputs a JSON file with detailed criteria evaluation.

Usage:
    python analyze_repo.py --repo-path /path/to/repo
    python analyze_repo.py --repo-path . --output /tmp/analysis.json
"""

import argparse
import json
import os
import re
import subprocess
from datetime import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
from enum import Enum


class CriterionStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


@dataclass
class AppInfo:
    """Information about a detected application in a monorepo."""
    name: str          # directory name
    path: Path         # absolute path
    languages: list[str] = field(default_factory=list)


@dataclass
class CriterionResult:
    id: str
    pillar: str
    level: int
    status: CriterionStatus
    score: str  # "1/1", "0/1", "3/4", or "—/—"
    reason: str
    scope: str = "repo"  # "repo" or "app"
    app_results: dict[str, bool] = field(default_factory=dict)  # {"web": True, "api": False}


@dataclass
class PillarResult:
    name: str
    passed: int
    total: int
    criteria: list[CriterionResult] = field(default_factory=list)

    @property
    def percentage(self) -> int:
        if self.total == 0:
            return 100
        return int((self.passed / self.total) * 100)


@dataclass
class AnalysisResult:
    repo_path: str
    repo_name: str
    pillars: dict[str, PillarResult] = field(default_factory=dict)
    level_scores: dict[int, float] = field(default_factory=dict)
    achieved_level: int = 1
    pass_rate: float = 0.0
    total_passed: int = 0
    total_criteria: int = 0
    repo_type: str = "application"  # library, cli, database, monorepo, application
    languages: list[str] = field(default_factory=list)
    detected_apps: list[AppInfo] = field(default_factory=list)
    undetected_app_folders: list[str] = field(default_factory=list)  # folders without manifests


# Scope constants: criteria evaluated once per repo vs per-app in monorepos
APP_SCOPED_CRITERIA = {
    "formatter", "lint_config", "type_check", "strict_typing",
    "unit_tests_exist", "unit_tests_runnable", "test_naming_conventions", "test_isolation",
    "integration_tests_exist", "test_coverage_thresholds",
    "deps_pinned", "build_cmd_doc", "dockerfile_exists",
    "structured_logging", "health_checks", "error_tracking_contextualized",
}


class RepoAnalyzer:
    """Analyzes repository for agent readiness criteria."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self.result = AnalysisResult(
            repo_path=str(self.repo_path),
            repo_name=self.repo_path.name
        )
        self._file_cache: dict[str, bool] = {}
        self._content_cache: dict[str, str] = {}

    def analyze(self) -> AnalysisResult:
        """Run full analysis and return results."""
        self._detect_repo_type()
        self._detect_languages()
        self._detect_apps()
        self._evaluate_all_pillars()
        self._calculate_levels()
        return self.result

    def _file_exists(self, *patterns: str) -> bool:
        """Check if any of the given file patterns exist."""
        for pattern in patterns:
            cache_key = f"exists:{pattern}"
            if cache_key in self._file_cache:
                if self._file_cache[cache_key]:
                    return True
                continue

            # Handle glob patterns
            if "*" in pattern:
                matches = list(self.repo_path.glob(pattern))
                exists = len(matches) > 0
            else:
                exists = (self.repo_path / pattern).exists()

            self._file_cache[cache_key] = exists
            if exists:
                return True
        return False

    def _read_file(self, path: str) -> Optional[str]:
        """Read file content, with caching."""
        if path in self._content_cache:
            return self._content_cache[path]

        full_path = self.repo_path / path
        if not full_path.exists():
            return None

        try:
            content = full_path.read_text(errors='ignore')
            self._content_cache[path] = content
            return content
        except Exception:
            return None

    def _search_files(self, pattern: str, content_pattern: str = None) -> bool:
        """Search for files matching pattern, optionally with content."""
        matches = list(self.repo_path.glob(pattern))
        if not matches:
            return False
        if content_pattern is None:
            return True

        regex = re.compile(content_pattern, re.IGNORECASE)
        for match in matches[:10]:  # Limit for performance
            try:
                content = match.read_text(errors='ignore')
                if regex.search(content):
                    return True
            except Exception:
                continue
        return False

    def _run_command(self, cmd: list[str], timeout: int = 10) -> tuple[int, str]:
        """Run a command and return (exit_code, output)."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return -1, str(e)

    def _detect_repo_type(self):
        """Detect repository type for criterion skipping."""
        # Check for library indicators
        if self._file_exists("setup.py", "setup.cfg") and not self._file_exists("Dockerfile"):
            if "library" in str(self._read_file("setup.py") or "").lower():
                self.result.repo_type = "library"
                return

        if self._file_exists("pyproject.toml"):
            content = self._read_file("pyproject.toml") or ""
            if "[project]" in content and "Dockerfile" not in os.listdir(self.repo_path):
                # Likely a library
                readme = self._read_file("README.md") or ""
                if "pip install" in readme.lower() and "docker" not in readme.lower():
                    self.result.repo_type = "library"
                    return

        # Check for CLI tool
        if self._file_exists("**/cli.py", "**/main.py", "**/cmd/**"):
            readme = self._read_file("README.md") or ""
            if any(x in readme.lower() for x in ["command line", "cli", "usage:"]):
                self.result.repo_type = "cli"
                return

        # Check for database project
        if "database" in self.result.repo_name.lower() or "db" in self.result.repo_name.lower():
            self.result.repo_type = "database"
            return

        # Check for monorepo
        if self._file_exists("packages/*", "apps/*", "lerna.json", "pnpm-workspace.yaml"):
            self.result.repo_type = "monorepo"
            return

        self.result.repo_type = "application"

    def _detect_languages(self):
        """Detect primary programming languages."""
        languages = []

        if self._file_exists("*.py", "**/*.py", "pyproject.toml", "setup.py"):
            languages.append("Python")
        if self._file_exists("*.ts", "**/*.ts", "tsconfig.json"):
            languages.append("TypeScript")
        if self._file_exists("*.js", "**/*.js", "package.json"):
            if "TypeScript" not in languages:
                languages.append("JavaScript")
        if self._file_exists("*.go", "**/*.go", "go.mod"):
            languages.append("Go")
        if self._file_exists("*.rs", "**/*.rs", "Cargo.toml"):
            languages.append("Rust")
        if self._file_exists("*.java", "**/*.java", "pom.xml", "build.gradle"):
            languages.append("Java")
        if self._file_exists("*.rb", "**/*.rb", "Gemfile"):
            languages.append("Ruby")
        if self._file_exists("*.cpp", "*.cc", "**/*.cpp", "CMakeLists.txt"):
            languages.append("C++")

        self.result.languages = languages if languages else ["Unknown"]

    def _detect_apps(self):
        """Detect individual applications in monorepo."""
        if self.result.repo_type != "monorepo":
            return

        app_dirs = ["packages", "apps", "services", "modules"]
        manifest_files = [
            "package.json", "pyproject.toml", "setup.py",
            "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "Gemfile"
        ]

        for dir_name in app_dirs:
            dir_path = self.repo_path / dir_name
            if not dir_path.exists() or not dir_path.is_dir():
                continue

            for subdir in sorted(dir_path.iterdir()):
                if not subdir.is_dir():
                    continue
                # Skip hidden directories and common non-app folders
                if subdir.name.startswith(".") or subdir.name in ["node_modules", "__pycache__"]:
                    continue

                # Check for manifest file
                has_manifest = any((subdir / m).exists() for m in manifest_files)
                if has_manifest:
                    langs = self._detect_app_languages(subdir)
                    self.result.detected_apps.append(AppInfo(
                        name=subdir.name,
                        path=subdir,
                        languages=langs
                    ))
                else:
                    # Warn about folder without manifest
                    self.result.undetected_app_folders.append(f"{dir_name}/{subdir.name}")

    def _detect_app_languages(self, app_path: Path) -> list[str]:
        """Detect languages for a specific app directory."""
        languages = []
        if list(app_path.glob("*.py")) or (app_path / "pyproject.toml").exists():
            languages.append("Python")
        if list(app_path.glob("*.ts")) or (app_path / "tsconfig.json").exists():
            languages.append("TypeScript")
        if list(app_path.glob("*.js")) or (app_path / "package.json").exists():
            if "TypeScript" not in languages:
                languages.append("JavaScript")
        if list(app_path.glob("*.go")) or (app_path / "go.mod").exists():
            languages.append("Go")
        if list(app_path.glob("*.rs")) or (app_path / "Cargo.toml").exists():
            languages.append("Rust")
        return languages if languages else ["Unknown"]

    def _should_skip(self, criterion_id: str) -> tuple[bool, str]:
        """Determine if a criterion should be skipped based on repo type."""
        repo_type = self.result.repo_type

        skip_rules = {
            "library": [
                ("health_checks", "Library, not a deployed service"),
                ("progressive_rollout", "Not applicable for a library"),
                ("rollback_automation", "Not applicable for a library"),
                ("dast_scanning", "Library, not a web service"),
                ("alerting_configured", "Library without runtime"),
                ("deployment_observability", "Library without deployments"),
                ("metrics_collection", "Library without runtime"),
                ("profiling_instrumentation", "Library where profiling not meaningful"),
                ("circuit_breakers", "Library without external dependencies"),
                ("distributed_tracing", "Library without runtime"),
                ("local_services_setup", "Library without external dependencies"),
                ("database_schema", "Library without database"),
                ("n_plus_one_detection", "Library without database/ORM"),
                ("privacy_compliance", "Library without user data"),
                ("pii_handling", "Library without user data"),
            ],
            "database": [
                ("n_plus_one_detection", "Database project IS the database layer"),
                ("dast_scanning", "Database server, not web application"),
            ],
            "cli": [
                ("dast_scanning", "CLI tool, not web application"),
                ("health_checks", "CLI tool, not a service"),
                ("progressive_rollout", "CLI tool without deployments"),
            ],
        }

        for rule_type, rules in skip_rules.items():
            if repo_type == rule_type:
                for crit_id, reason in rules:
                    if criterion_id == crit_id:
                        return True, reason

        # Skip monorepo criteria for non-monorepos
        if repo_type != "monorepo":
            if criterion_id in ["monorepo_tooling", "version_drift_detection"]:
                return True, "Single-application repository, not a monorepo"

        # Skip prerequisites
        if criterion_id == "devcontainer_runnable":
            if not self._file_exists(".devcontainer/devcontainer.json"):
                return True, "No devcontainer to test (prerequisite failed)"

        if criterion_id == "agents_md_validation":
            if not self._file_exists("AGENTS.md", "CLAUDE.md"):
                return True, "No AGENTS.md exists (prerequisite failed)"

        if criterion_id == "dead_feature_flag_detection":
            # Check if feature flags exist first
            if not self._check_feature_flags():
                return True, "No feature flag infrastructure (prerequisite failed)"

        return False, ""

    def _check_feature_flags(self) -> bool:
        """Check if feature flag infrastructure exists."""
        # Check for common feature flag services
        patterns = [
            "launchdarkly", "statsig", "unleash", "growthbook",
            "feature.flag", "featureflag", "feature_flag"
        ]

        for pattern in ["package.json", "requirements.txt", "go.mod", "Gemfile"]:
            content = self._read_file(pattern)
            if content:
                for flag_pattern in patterns:
                    if flag_pattern in content.lower():
                        return True
        return False

    def _evaluate_all_pillars(self):
        """Evaluate all criteria across all pillars."""
        pillars = {
            "Style & Validation": self._evaluate_style_validation,
            "Build System": self._evaluate_build_system,
            "Testing": self._evaluate_testing,
            "Documentation": self._evaluate_documentation,
            "Dev Environment": self._evaluate_dev_environment,
            "Debugging & Observability": self._evaluate_observability,
            "Security": self._evaluate_security,
            "Task Discovery": self._evaluate_task_discovery,
            "Product & Analytics": self._evaluate_product_analytics,
        }

        for pillar_name, evaluate_func in pillars.items():
            criteria = evaluate_func()
            passed = sum(1 for c in criteria if c.status == CriterionStatus.PASS)
            total = sum(1 for c in criteria if c.status != CriterionStatus.SKIP)

            self.result.pillars[pillar_name] = PillarResult(
                name=pillar_name,
                passed=passed,
                total=total,
                criteria=criteria
            )

            self.result.total_passed += passed
            self.result.total_criteria += total

        if self.result.total_criteria > 0:
            self.result.pass_rate = round(
                (self.result.total_passed / self.result.total_criteria) * 100, 1
            )

    def _make_result(
        self,
        criterion_id: str,
        pillar: str,
        level: int,
        passed: bool,
        reason: str
    ) -> CriterionResult:
        """Create a criterion result, handling skips."""
        should_skip, skip_reason = self._should_skip(criterion_id)

        if should_skip:
            return CriterionResult(
                id=criterion_id,
                pillar=pillar,
                level=level,
                status=CriterionStatus.SKIP,
                score="—/—",
                reason=skip_reason
            )

        return CriterionResult(
            id=criterion_id,
            pillar=pillar,
            level=level,
            status=CriterionStatus.PASS if passed else CriterionStatus.FAIL,
            score="1/1" if passed else "0/1",
            reason=reason
        )

    def _make_app_result(
        self,
        criterion_id: str,
        pillar: str,
        level: int,
        app_results: dict[str, bool],
        pass_reason: str,
        fail_reason: str
    ) -> CriterionResult:
        """Create result for app-scoped criterion with 80% threshold."""
        should_skip, skip_reason = self._should_skip(criterion_id)
        if should_skip:
            return CriterionResult(
                id=criterion_id,
                pillar=pillar,
                level=level,
                status=CriterionStatus.SKIP,
                score="—/—",
                reason=skip_reason,
                scope="app"
            )

        # For non-monorepos or no detected apps, fall back to repo-scoped
        if self.result.repo_type != "monorepo" or not self.result.detected_apps:
            passed = app_results.get("__repo__", False)
            return CriterionResult(
                id=criterion_id,
                pillar=pillar,
                level=level,
                status=CriterionStatus.PASS if passed else CriterionStatus.FAIL,
                score="1/1" if passed else "0/1",
                reason=pass_reason if passed else fail_reason
            )

        passed_count = sum(1 for v in app_results.values() if v)
        total_count = len(app_results)
        pass_rate = passed_count / total_count if total_count > 0 else 0

        # 80% threshold for passing
        status = CriterionStatus.PASS if pass_rate >= 0.8 else CriterionStatus.FAIL

        if status == CriterionStatus.PASS:
            reason = pass_reason
        else:
            failing_apps = [name for name, passed in app_results.items() if not passed]
            reason = f"{fail_reason} (failing: {', '.join(failing_apps)})"

        return CriterionResult(
            id=criterion_id,
            pillar=pillar,
            level=level,
            status=status,
            score=f"{passed_count}/{total_count}",
            reason=reason,
            scope="app",
            app_results=app_results
        )

    def _check_file_at_path(self, path: Path, *patterns: str) -> bool:
        """Check if any file pattern exists at the given path."""
        for pattern in patterns:
            if "*" in pattern:
                if list(path.glob(pattern)):
                    return True
            else:
                if (path / pattern).exists():
                    return True
        return False

    def _check_content_at_path(self, path: Path, filename: str, pattern: str) -> bool:
        """Check if a file at path contains a pattern."""
        file_path = path / filename
        if not file_path.exists():
            return False
        try:
            content = file_path.read_text(errors='ignore')
            return pattern.lower() in content.lower()
        except Exception:
            return False

    def _check_formatter_for_path(self, path: Path) -> bool:
        """Check if formatter is configured at given path or root."""
        # Check at this path
        if self._check_file_at_path(path,
            ".prettierrc", ".prettierrc.json", ".prettierrc.js", "prettier.config.js",
            ".black.toml", "rustfmt.toml", ".rustfmt.toml"):
            return True
        if self._check_content_at_path(path, "pyproject.toml", "ruff") or \
           self._check_content_at_path(path, "pyproject.toml", "black"):
            return True
        # Check root (inheritance)
        if path != self.repo_path:
            if self._check_file_at_path(self.repo_path,
                ".prettierrc", ".prettierrc.json", ".prettierrc.js", "prettier.config.js",
                ".black.toml", "rustfmt.toml", ".rustfmt.toml"):
                return True
            if self._check_content_at_path(self.repo_path, "pyproject.toml", "ruff") or \
               self._check_content_at_path(self.repo_path, "pyproject.toml", "black"):
                return True
        return False

    def _check_linter_for_path(self, path: Path) -> bool:
        """Check if linter is configured at given path or root."""
        if self._check_file_at_path(path,
            ".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yaml",
            "eslint.config.js", "eslint.config.mjs",
            ".pylintrc", "pylintrc", "golangci.yml", ".golangci.yml"):
            return True
        if self._check_content_at_path(path, "pyproject.toml", "ruff") or \
           self._check_content_at_path(path, "pyproject.toml", "pylint"):
            return True
        # Check root
        if path != self.repo_path:
            if self._check_file_at_path(self.repo_path,
                ".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yaml",
                "eslint.config.js", "eslint.config.mjs",
                ".pylintrc", "pylintrc", "golangci.yml", ".golangci.yml"):
                return True
            if self._check_content_at_path(self.repo_path, "pyproject.toml", "ruff") or \
               self._check_content_at_path(self.repo_path, "pyproject.toml", "pylint"):
                return True
        return False

    def _check_type_check_for_path(self, path: Path, languages: list[str]) -> bool:
        """Check if type checking is configured at given path."""
        if "Go" in languages or "Rust" in languages:
            return True  # Statically typed
        if self._check_file_at_path(path, "tsconfig.json"):
            return True
        if self._check_content_at_path(path, "pyproject.toml", "mypy"):
            return True
        # Check root
        if path != self.repo_path:
            if self._check_file_at_path(self.repo_path, "tsconfig.json"):
                return True
            if self._check_content_at_path(self.repo_path, "pyproject.toml", "mypy"):
                return True
        return False

    def _check_tests_for_path(self, path: Path) -> bool:
        """Check if unit tests exist at given path."""
        return self._check_file_at_path(path,
            "tests/**/*.py", "test/**/*.py", "*_test.py", "*_test.go",
            "**/*.spec.ts", "**/*.spec.js", "**/*.test.ts", "**/*.test.js",
            "spec/**/*.rb", "tests/**/*.rs"
        )

    def _check_lockfile_for_path(self, path: Path) -> bool:
        """Check if lockfile exists at given path or root."""
        if self._check_file_at_path(path,
            "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
            "uv.lock", "poetry.lock", "Pipfile.lock",
            "go.sum", "Cargo.lock", "Gemfile.lock"):
            return True
        # Check root for shared lockfile
        if path != self.repo_path:
            if self._check_file_at_path(self.repo_path,
                "package-lock.json", "yarn.lock", "pnpm-lock.yaml"):
                return True
        return False

    def _evaluate_style_validation(self) -> list[CriterionResult]:
        """Evaluate Style & Validation pillar."""
        pillar = "Style & Validation"
        results = []

        # L1: formatter (app-scoped)
        if self.result.repo_type == "monorepo" and self.result.detected_apps:
            app_results = {app.name: self._check_formatter_for_path(app.path) for app in self.result.detected_apps}
            results.append(self._make_app_result(
                "formatter", pillar, 1, app_results,
                "Formatter configured",
                "Add .prettierrc, ruff/black in pyproject.toml"
            ))
        else:
            formatter_found = self._check_formatter_for_path(self.repo_path)
            results.append(self._make_result(
                "formatter", pillar, 1, formatter_found,
                "Formatter configured" if formatter_found else "Add .prettierrc, ruff/black in pyproject.toml, or rustfmt.toml for consistent formatting"
            ))

        # L1: lint_config (app-scoped)
        if self.result.repo_type == "monorepo" and self.result.detected_apps:
            app_results = {app.name: self._check_linter_for_path(app.path) for app in self.result.detected_apps}
            results.append(self._make_app_result(
                "lint_config", pillar, 1, app_results,
                "Linter configured",
                "Add .eslintrc.js, ruff/pylint in pyproject.toml"
            ))
        else:
            lint_found = self._check_linter_for_path(self.repo_path)
            results.append(self._make_result(
                "lint_config", pillar, 1, lint_found,
                "Linter configured" if lint_found else "Add .eslintrc.js, ruff/pylint in pyproject.toml, or .golangci.yml"
            ))

        # L1: type_check (app-scoped)
        if self.result.repo_type == "monorepo" and self.result.detected_apps:
            app_results = {app.name: self._check_type_check_for_path(app.path, app.languages) for app in self.result.detected_apps}
            results.append(self._make_app_result(
                "type_check", pillar, 1, app_results,
                "Type checking configured",
                "Add tsconfig.json or mypy in pyproject.toml"
            ))
        else:
            type_check = self._check_type_check_for_path(self.repo_path, self.result.languages)
            results.append(self._make_result(
                "type_check", pillar, 1, type_check,
                "Type checking configured" if type_check else "Add tsconfig.json for TS, or mypy in pyproject.toml for Python"
            ))

        # L2: strict_typing
        strict_typing = False
        if "Go" in self.result.languages or "Rust" in self.result.languages:
            strict_typing = True
        elif self._file_exists("tsconfig.json"):
            content = self._read_file("tsconfig.json") or ""
            strict_typing = '"strict": true' in content or '"strict":true' in content
        elif self._file_exists("pyproject.toml"):
            content = self._read_file("pyproject.toml") or ""
            strict_typing = "strict = true" in content or "strict=true" in content
        results.append(self._make_result(
            "strict_typing", pillar, 2, strict_typing,
            "Strict typing enabled" if strict_typing else "Enable 'strict: true' in tsconfig.json or mypy strict mode in pyproject.toml"
        ))

        # L2: pre_commit_hooks
        pre_commit = self._file_exists(
            ".pre-commit-config.yaml", ".pre-commit-config.yml",
            ".husky", ".husky/*"
        )
        results.append(self._make_result(
            "pre_commit_hooks", pillar, 2, pre_commit,
            "Pre-commit hooks configured" if pre_commit else "Add .pre-commit-config.yaml or .husky/ to automate checks before commits"
        ))

        # L2: naming_consistency
        naming = False
        eslint = self._read_file(".eslintrc.json") or self._read_file(".eslintrc") or ""
        if "naming" in eslint.lower() or "@typescript-eslint/naming" in eslint:
            naming = True
        agents_md = self._read_file("AGENTS.md") or self._read_file("CLAUDE.md") or ""
        if "naming" in agents_md.lower() or "convention" in agents_md.lower():
            naming = True
        # Go uses stdlib naming by default
        if "Go" in self.result.languages:
            naming = True
        results.append(self._make_result(
            "naming_consistency", pillar, 2, naming,
            "Naming conventions enforced" if naming else "Document naming conventions in AGENTS.md or enable @typescript-eslint/naming-convention"
        ))

        # L2: large_file_detection
        large_file = self._file_exists(".gitattributes", ".lfsconfig")
        if not large_file:
            pre_commit_cfg = self._read_file(".pre-commit-config.yaml") or ""
            large_file = "check-added-large-files" in pre_commit_cfg
        results.append(self._make_result(
            "large_file_detection", pillar, 2, large_file,
            "Large file detection configured" if large_file else "Add .gitattributes with Git LFS or check-added-large-files in pre-commit"
        ))

        # L3: code_modularization
        modular = self._file_exists(
            ".importlinter", "nx.json", "BUILD.bazel", "BUILD"
        )
        results.append(self._make_result(
            "code_modularization", pillar, 3, modular,
            "Module boundaries enforced" if modular else "Add import-linter, nx.json, or BUILD.bazel to enforce module boundaries"
        ))

        # L3: cyclomatic_complexity
        complexity = False
        for config in [".golangci.yml", ".golangci.yaml", "pyproject.toml"]:
            content = self._read_file(config) or ""
            if any(x in content.lower() for x in ["gocyclo", "mccabe", "complexity", "radon"]):
                complexity = True
                break
        results.append(self._make_result(
            "cyclomatic_complexity", pillar, 3, complexity,
            "Complexity analysis configured" if complexity else "Add mccabe/radon in pyproject.toml or gocyclo in .golangci.yml"
        ))

        # L3: dead_code_detection
        dead_code = False
        workflows = list(self.repo_path.glob(".github/workflows/*.yml")) + \
                   list(self.repo_path.glob(".github/workflows/*.yaml"))
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["vulture", "knip", "deadcode"]):
                dead_code = True
                break
        results.append(self._make_result(
            "dead_code_detection", pillar, 3, dead_code,
            "Dead code detection enabled" if dead_code else "Add vulture (Python), knip (JS/TS), or deadcode (Go) to CI workflow"
        ))

        # L3: duplicate_code_detection
        duplicate = False
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["jscpd", "pmd cpd", "sonarqube"]):
                duplicate = True
                break
        results.append(self._make_result(
            "duplicate_code_detection", pillar, 3, duplicate,
            "Duplicate detection enabled" if duplicate else "Add jscpd, PMD CPD, or SonarQube to CI for duplicate code detection"
        ))

        # L4: tech_debt_tracking
        tech_debt = False
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["todo", "fixme", "sonar"]):
                tech_debt = True
                break
        results.append(self._make_result(
            "tech_debt_tracking", pillar, 4, tech_debt,
            "Tech debt tracking enabled" if tech_debt else "Add TODO/FIXME scanning in CI or integrate SonarQube for tech debt tracking"
        ))

        # L4: n_plus_one_detection
        n_plus_one = False
        deps = (self._read_file("requirements.txt") or "") + \
               (self._read_file("Gemfile") or "") + \
               (self._read_file("package.json") or "")
        if any(x in deps.lower() for x in ["nplusone", "bullet", "query-analyzer"]):
            n_plus_one = True
        results.append(self._make_result(
            "n_plus_one_detection", pillar, 4, n_plus_one,
            "N+1 detection enabled" if n_plus_one else "Add nplusone (Python), bullet (Ruby), or query-analyzer for N+1 detection"
        ))

        return results

    def _evaluate_build_system(self) -> list[CriterionResult]:
        """Evaluate Build System pillar."""
        pillar = "Build System"
        results = []

        # L1: build_cmd_doc
        readme = self._read_file("README.md") or ""
        agents_md = self._read_file("AGENTS.md") or self._read_file("CLAUDE.md") or ""
        build_doc = any(x in (readme + agents_md).lower() for x in [
            "npm run", "yarn", "pnpm", "make", "cargo build", "go build",
            "pip install", "python setup.py", "gradle", "mvn"
        ])
        results.append(self._make_result(
            "build_cmd_doc", pillar, 1, build_doc,
            "Build commands documented" if build_doc else "Document build commands (npm run, make, cargo build, etc.) in README or AGENTS.md"
        ))

        # L1: deps_pinned (app-scoped)
        if self.result.repo_type == "monorepo" and self.result.detected_apps:
            app_results = {app.name: self._check_lockfile_for_path(app.path) for app in self.result.detected_apps}
            results.append(self._make_app_result(
                "deps_pinned", pillar, 1, app_results,
                "Dependencies pinned with lockfile",
                "Add package-lock.json, uv.lock, or Cargo.lock"
            ))
        else:
            lockfile = self._check_lockfile_for_path(self.repo_path)
            results.append(self._make_result(
                "deps_pinned", pillar, 1, lockfile,
                "Dependencies pinned with lockfile" if lockfile else "Add package-lock.json, uv.lock, poetry.lock, or Cargo.lock to pin dependencies"
            ))

        # L1: vcs_cli_tools
        code, output = self._run_command(["gh", "auth", "status"])
        vcs_cli = code == 0
        if not vcs_cli:
            code, output = self._run_command(["glab", "auth", "status"])
            vcs_cli = code == 0
        results.append(self._make_result(
            "vcs_cli_tools", pillar, 1, vcs_cli,
            "VCS CLI authenticated" if vcs_cli else "Run 'gh auth login' or 'glab auth login' to authenticate VCS CLI"
        ))

        # L2: fast_ci_feedback
        # Check for CI config existence as proxy
        ci_exists = self._file_exists(
            ".github/workflows/*.yml", ".github/workflows/*.yaml",
            ".gitlab-ci.yml", ".circleci/config.yml",
            "Jenkinsfile", ".travis.yml"
        )
        results.append(self._make_result(
            "fast_ci_feedback", pillar, 2, ci_exists,
            "CI workflow configured" if ci_exists else "Add .github/workflows/*.yml, .gitlab-ci.yml, or .circleci/config.yml"
        ))

        # L2: single_command_setup
        single_cmd = any(x in (readme + agents_md).lower() for x in [
            "make install", "npm install", "yarn install", "pip install -e",
            "docker-compose up", "./dev", "make setup", "just"
        ])
        results.append(self._make_result(
            "single_command_setup", pillar, 2, single_cmd,
            "Single command setup documented" if single_cmd else "Document a single setup command (make install, npm install, docker-compose up) in README"
        ))

        # L2: release_automation
        release_auto = self._search_files(
            ".github/workflows/*.yml",
            r"(release|publish|deploy)"
        ) or self._search_files(
            ".github/workflows/*.yaml",
            r"(release|publish|deploy)"
        )
        results.append(self._make_result(
            "release_automation", pillar, 2, release_auto,
            "Release automation configured" if release_auto else "Add a release/publish workflow in .github/workflows/ with semantic-release or similar"
        ))

        # L2: deployment_frequency (check for recent releases)
        release_auto_exists = release_auto  # Use same check as proxy
        results.append(self._make_result(
            "deployment_frequency", pillar, 2, release_auto_exists,
            "Regular deployments" if release_auto_exists else "Set up CI/CD pipeline for automated deployments on merge to main"
        ))

        # L3: release_notes_automation
        release_notes = self._search_files(
            ".github/workflows/*.yml",
            r"(changelog|release.notes|latest.changes)"
        )
        results.append(self._make_result(
            "release_notes_automation", pillar, 3, release_notes,
            "Release notes automated" if release_notes else "Add auto-changelog, release-please, or semantic-release for automated release notes"
        ))

        # L3: agentic_development
        code, output = self._run_command(["git", "log", "--oneline", "-50"])
        agentic = any(x in output.lower() for x in [
            "co-authored-by", "droid", "copilot", "claude", "gpt", "ai agent"
        ])
        results.append(self._make_result(
            "agentic_development", pillar, 3, agentic,
            "AI agent commits found" if agentic else "Use AI coding assistants (Claude, Copilot) with Co-Authored-By commit trailers"
        ))

        # L3: automated_pr_review
        pr_review = self._file_exists("danger.js", "dangerfile.js", "dangerfile.ts")
        if not pr_review:
            workflows = list(self.repo_path.glob(".github/workflows/*.yml"))
            for wf in workflows[:5]:
                content = wf.read_text(errors='ignore')
                if any(x in content.lower() for x in ["review", "danger", "lint-pr"]):
                    pr_review = True
                    break
        results.append(self._make_result(
            "automated_pr_review", pillar, 3, pr_review,
            "Automated PR review configured" if pr_review else "Add danger.js or a PR lint workflow for automated PR review checks"
        ))

        # L3: feature_flag_infrastructure
        feature_flags = self._check_feature_flags()
        results.append(self._make_result(
            "feature_flag_infrastructure", pillar, 3, feature_flags,
            "Feature flags configured" if feature_flags else "Add LaunchDarkly, Statsig, Unleash, or GrowthBook for feature flag management"
        ))

        # L4: build_performance_tracking
        build_perf = False
        if self._file_exists("turbo.json", "nx.json"):
            build_perf = True
        results.append(self._make_result(
            "build_performance_tracking", pillar, 4, build_perf,
            "Build caching configured" if build_perf else "Add turbo.json or nx.json for build caching and performance tracking"
        ))

        # L4: heavy_dependency_detection (for JS bundles)
        heavy_deps = False
        pkg_json = self._read_file("package.json") or ""
        if any(x in pkg_json.lower() for x in ["webpack-bundle-analyzer", "bundlesize", "size-limit"]):
            heavy_deps = True
        results.append(self._make_result(
            "heavy_dependency_detection", pillar, 4, heavy_deps,
            "Bundle size tracking configured" if heavy_deps else "Add webpack-bundle-analyzer, bundlesize, or size-limit for bundle size tracking"
        ))

        # L4: unused_dependencies_detection
        unused_deps = False
        workflows = list(self.repo_path.glob(".github/workflows/*.yml"))
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["depcheck", "deptry", "go mod tidy"]):
                unused_deps = True
                break
        results.append(self._make_result(
            "unused_dependencies_detection", pillar, 4, unused_deps,
            "Unused deps detection enabled" if unused_deps else "Add depcheck (JS), deptry (Python), or 'go mod tidy' check to CI"
        ))

        # L4: dead_feature_flag_detection
        dead_flags = False  # Requires feature flag infra first
        results.append(self._make_result(
            "dead_feature_flag_detection", pillar, 4, dead_flags,
            "Dead flag detection enabled" if dead_flags else "Add stale flag detection via feature flag provider (LaunchDarkly, Statsig)"
        ))

        # L4: monorepo_tooling
        monorepo_tools = self._file_exists("lerna.json", "nx.json", "turbo.json", "pnpm-workspace.yaml")
        results.append(self._make_result(
            "monorepo_tooling", pillar, 4, monorepo_tools,
            "Monorepo tooling configured" if monorepo_tools else "Add lerna.json, nx.json, turbo.json, or pnpm-workspace.yaml for monorepo management"
        ))

        # L4: version_drift_detection
        version_drift = False  # Complex to detect
        results.append(self._make_result(
            "version_drift_detection", pillar, 4, version_drift,
            "Version drift detection enabled" if version_drift else "Add syncpack or manypkg check to detect package version drift across workspaces"
        ))

        # L5: progressive_rollout
        progressive = False
        for pattern in ["*.yml", "*.yaml"]:
            if self._search_files(f".github/workflows/{pattern}", r"canary|gradual|rollout"):
                progressive = True
                break
        results.append(self._make_result(
            "progressive_rollout", pillar, 5, progressive,
            "Progressive rollout configured" if progressive else "Add canary deployments or gradual rollout strategy in deployment workflow"
        ))

        # L5: rollback_automation
        rollback = False
        results.append(self._make_result(
            "rollback_automation", pillar, 5, rollback,
            "Rollback automation configured" if rollback else "Add automated rollback triggers based on error rates or health checks"
        ))

        return results

    def _evaluate_testing(self) -> list[CriterionResult]:
        """Evaluate Testing pillar."""
        pillar = "Testing"
        results = []

        # L1: unit_tests_exist (app-scoped)
        if self.result.repo_type == "monorepo" and self.result.detected_apps:
            app_results = {app.name: self._check_tests_for_path(app.path) for app in self.result.detected_apps}
            results.append(self._make_app_result(
                "unit_tests_exist", pillar, 1, app_results,
                "Unit tests found",
                "Add unit tests in tests/ directory"
            ))
        else:
            tests_exist = self._check_tests_for_path(self.repo_path)
            results.append(self._make_result(
                "unit_tests_exist", pillar, 1, tests_exist,
                "Unit tests found" if tests_exist else "Add unit tests in tests/ directory with *_test.py, *.spec.ts, or *_test.go naming"
            ))

        # L1: unit_tests_runnable
        readme = self._read_file("README.md") or ""
        agents_md = self._read_file("AGENTS.md") or self._read_file("CLAUDE.md") or ""
        test_cmd = any(x in (readme + agents_md).lower() for x in [
            "pytest", "npm test", "yarn test", "go test", "cargo test",
            "make test", "rake test", "rspec", "jest"
        ])
        results.append(self._make_result(
            "unit_tests_runnable", pillar, 1, test_cmd,
            "Test commands documented" if test_cmd else "Document test command (pytest, npm test, go test, etc.) in README or AGENTS.md"
        ))

        # L2: test_naming_conventions
        naming = False
        if self._file_exists("pyproject.toml"):
            content = self._read_file("pyproject.toml") or ""
            naming = "pytest" in content.lower()
        if self._file_exists("jest.config.js", "jest.config.ts"):
            naming = True
        if "Go" in self.result.languages:
            naming = True  # Go has standard _test.go convention
        results.append(self._make_result(
            "test_naming_conventions", pillar, 2, naming,
            "Test naming conventions enforced" if naming else "Configure pytest in pyproject.toml or jest.config.js for test naming conventions"
        ))

        # L2: test_isolation
        isolation = False
        if self._file_exists("pyproject.toml"):
            content = self._read_file("pyproject.toml") or ""
            isolation = "pytest-xdist" in content or "-n auto" in content
        workflows = list(self.repo_path.glob(".github/workflows/*.yml"))
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if "matrix" in content.lower():
                isolation = True
                break
        if "Go" in self.result.languages:
            isolation = True  # Go tests run in parallel by default
        results.append(self._make_result(
            "test_isolation", pillar, 2, isolation,
            "Tests support isolation/parallelism" if isolation else "Add pytest-xdist for parallel tests or use matrix strategy in CI workflow"
        ))

        # L3: integration_tests_exist
        integration = self._file_exists(
            "tests/integration/**", "integration/**", "e2e/**",
            "tests/e2e/**", "cypress/**", "playwright.config.*"
        )
        results.append(self._make_result(
            "integration_tests_exist", pillar, 3, integration,
            "Integration tests found" if integration else "Add tests/integration/, e2e/, or configure Playwright/Cypress for E2E tests"
        ))

        # L3: test_coverage_thresholds
        coverage = False
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["coverage", "codecov", "coveralls"]):
                coverage = True
                break
        if self._file_exists(".coveragerc", "coverage.xml", "codecov.yml"):
            coverage = True
        results.append(self._make_result(
            "test_coverage_thresholds", pillar, 3, coverage,
            "Coverage thresholds enforced" if coverage else "Add coverage reporting (codecov.yml, .coveragerc) with minimum threshold enforcement"
        ))

        # L4: flaky_test_detection
        flaky = False
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["retry", "flaky", "quarantine", "rerun"]):
                flaky = True
                break
        results.append(self._make_result(
            "flaky_test_detection", pillar, 4, flaky,
            "Flaky test handling configured" if flaky else "Add test retry logic or flaky test quarantine mechanism in CI workflow"
        ))

        # L4: test_performance_tracking
        test_perf = False
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["durations", "timing", "benchmark"]):
                test_perf = True
                break
        results.append(self._make_result(
            "test_performance_tracking", pillar, 4, test_perf,
            "Test performance tracked" if test_perf else "Add --durations flag to pytest or benchmark tracking in CI for test timing analysis"
        ))

        return results

    def _evaluate_documentation(self) -> list[CriterionResult]:
        """Evaluate Documentation pillar."""
        pillar = "Documentation"
        results = []

        # L1: readme
        readme = self._file_exists("README.md", "README.rst", "README.txt", "README")
        results.append(self._make_result(
            "readme", pillar, 1, readme,
            "README exists" if readme else "Add README.md with project overview, setup instructions, and usage examples"
        ))

        # L2: agents_md
        agents_md = self._file_exists("AGENTS.md", "CLAUDE.md")
        results.append(self._make_result(
            "agents_md", pillar, 2, agents_md,
            "AGENTS.md exists" if agents_md else "Add AGENTS.md or CLAUDE.md with codebase context for AI coding assistants"
        ))

        # L2: documentation_freshness
        freshness = False
        code, output = self._run_command([
            "git", "log", "-1", "--format=%ci", "--", "README.md"
        ])
        if code == 0 and output.strip():
            freshness = True
        results.append(self._make_result(
            "documentation_freshness", pillar, 2, freshness,
            "Documentation recently updated" if freshness else "Update README.md with latest project changes and ensure docs stay current"
        ))

        # L3: api_schema_docs
        api_docs = self._file_exists(
            "openapi.yaml", "openapi.json", "swagger.yaml", "swagger.json",
            "schema.graphql", "*.graphql",
            "docs/api/**", "api-docs/**"
        )
        results.append(self._make_result(
            "api_schema_docs", pillar, 3, api_docs,
            "API documentation exists" if api_docs else "Add openapi.yaml, schema.graphql, or docs/api/ for API documentation"
        ))

        # L3: automated_doc_generation
        doc_gen = self._search_files(
            ".github/workflows/*.yml",
            r"(docs|documentation|mkdocs|sphinx|typedoc)"
        )
        results.append(self._make_result(
            "automated_doc_generation", pillar, 3, doc_gen,
            "Doc generation automated" if doc_gen else "Add mkdocs, sphinx, or typedoc workflow to CI for automated doc generation"
        ))

        # L3: service_flow_documented
        diagrams = self._file_exists(
            "**/*.mermaid", "**/*.puml", "docs/architecture*",
            "docs/**/*.md"
        )
        results.append(self._make_result(
            "service_flow_documented", pillar, 3, diagrams,
            "Architecture documented" if diagrams else "Add docs/architecture.md with Mermaid diagrams or PlantUML for service flow"
        ))

        # L3: skills
        skills = self._file_exists(
            ".claude/skills/**", ".factory/skills/**", ".skills/**"
        )
        results.append(self._make_result(
            "skills", pillar, 3, skills,
            "Skills directory exists" if skills else "Add .claude/skills/ or .skills/ directory with reusable AI agent workflows"
        ))

        # L4: agents_md_validation
        agents_validation = False
        workflows = list(self.repo_path.glob(".github/workflows/*.yml"))
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["agents.md", "claude.md"]):
                agents_validation = True
                break
        results.append(self._make_result(
            "agents_md_validation", pillar, 4, agents_validation,
            "AGENTS.md validation in CI" if agents_validation else "Add CI workflow to validate AGENTS.md structure and content on PRs"
        ))

        return results

    def _evaluate_dev_environment(self) -> list[CriterionResult]:
        """Evaluate Dev Environment pillar."""
        pillar = "Dev Environment"
        results = []

        # L2: env_template
        env_template = self._file_exists(".env.example", ".env.template", ".env.sample")
        if not env_template:
            readme = self._read_file("README.md") or ""
            agents_md = self._read_file("AGENTS.md") or ""
            env_template = "environment variable" in (readme + agents_md).lower()
        results.append(self._make_result(
            "env_template", pillar, 2, env_template,
            "Environment template exists" if env_template else "Add .env.example or .env.template with required environment variables"
        ))

        # L3: devcontainer
        devcontainer = self._file_exists(".devcontainer/devcontainer.json")
        results.append(self._make_result(
            "devcontainer", pillar, 3, devcontainer,
            "Devcontainer configured" if devcontainer else "Add .devcontainer/devcontainer.json for reproducible dev environments"
        ))

        # L3: devcontainer_runnable
        devcontainer_valid = False
        if devcontainer:
            content = self._read_file(".devcontainer/devcontainer.json")
            if content and "image" in content.lower():
                devcontainer_valid = True
        results.append(self._make_result(
            "devcontainer_runnable", pillar, 3, devcontainer_valid,
            "Devcontainer appears valid" if devcontainer_valid else "Add 'image' or 'dockerFile' key to devcontainer.json"
        ))

        # L3: database_schema
        db_schema = self._file_exists(
            "migrations/**", "db/migrations/**", "alembic/**",
            "prisma/schema.prisma", "schema.sql", "db/schema.rb"
        )
        results.append(self._make_result(
            "database_schema", pillar, 3, db_schema,
            "Database schema managed" if db_schema else "Add migrations/ (Alembic/Prisma/Rails) or schema.sql for database versioning"
        ))

        # L3: local_services_setup
        local_services = self._file_exists(
            "docker-compose.yml", "docker-compose.yaml",
            "compose.yml", "compose.yaml"
        )
        results.append(self._make_result(
            "local_services_setup", pillar, 3, local_services,
            "Local services configured" if local_services else "Add docker-compose.yml for local database, cache, and service dependencies"
        ))

        return results

    def _evaluate_observability(self) -> list[CriterionResult]:
        """Evaluate Debugging & Observability pillar."""
        pillar = "Debugging & Observability"
        results = []

        # L2: structured_logging
        logging_found = False
        deps = (self._read_file("package.json") or "") + \
               (self._read_file("requirements.txt") or "") + \
               (self._read_file("go.mod") or "")
        if any(x in deps.lower() for x in [
            "pino", "winston", "bunyan", "structlog", "loguru",
            "zerolog", "zap", "slog"
        ]):
            logging_found = True
        if "Python" in self.result.languages:
            if self._search_files("**/*.py", r"import logging"):
                logging_found = True
        results.append(self._make_result(
            "structured_logging", pillar, 2, logging_found,
            "Structured logging configured" if logging_found else "Add pino/winston (JS), structlog/loguru (Python), or zap/zerolog (Go) for structured logs"
        ))

        # L2: code_quality_metrics
        quality_metrics = self._search_files(
            ".github/workflows/*.yml",
            r"(coverage|sonar|quality)"
        )
        results.append(self._make_result(
            "code_quality_metrics", pillar, 2, quality_metrics,
            "Code quality metrics tracked" if quality_metrics else "Add SonarQube, Codecov, or code coverage reporting to CI workflow"
        ))

        # L3: error_tracking_contextualized
        error_tracking = any(x in deps.lower() for x in [
            "sentry", "bugsnag", "rollbar", "honeybadger"
        ])
        results.append(self._make_result(
            "error_tracking_contextualized", pillar, 3, error_tracking,
            "Error tracking configured" if error_tracking else "Add Sentry, Bugsnag, Rollbar, or Honeybadger for error monitoring"
        ))

        # L3: distributed_tracing
        tracing = any(x in deps.lower() for x in [
            "opentelemetry", "jaeger", "zipkin", "datadog", "x-request-id"
        ])
        results.append(self._make_result(
            "distributed_tracing", pillar, 3, tracing,
            "Distributed tracing configured" if tracing else "Add OpenTelemetry, Jaeger, or Datadog APM for distributed request tracing"
        ))

        # L3: metrics_collection
        metrics = any(x in deps.lower() for x in [
            "prometheus", "datadog", "newrelic", "statsd", "cloudwatch"
        ])
        results.append(self._make_result(
            "metrics_collection", pillar, 3, metrics,
            "Metrics collection configured" if metrics else "Add Prometheus, Datadog, or StatsD for application metrics collection"
        ))

        # L3: health_checks
        health = self._search_files(
            "**/*.py", r"health|ready|alive"
        ) or self._search_files(
            "**/*.ts", r"health|ready|alive"
        ) or self._search_files(
            "**/*.go", r"health|ready|alive"
        )
        results.append(self._make_result(
            "health_checks", pillar, 3, health,
            "Health checks implemented" if health else "Add /health, /ready, and /alive endpoints for container orchestration"
        ))

        # L4: profiling_instrumentation
        profiling = any(x in deps.lower() for x in [
            "pyinstrument", "py-spy", "pprof", "clinic"
        ])
        results.append(self._make_result(
            "profiling_instrumentation", pillar, 4, profiling,
            "Profiling configured" if profiling else "Add pyinstrument/py-spy (Python), pprof (Go), or clinic (Node) for profiling"
        ))

        # L4: alerting_configured
        alerting = self._file_exists(
            "**/alerts*.yml", "**/alertmanager*", "monitoring/**"
        )
        results.append(self._make_result(
            "alerting_configured", pillar, 4, alerting,
            "Alerting configured" if alerting else "Add monitoring/alerts.yml or configure Alertmanager/PagerDuty integration"
        ))

        # L4: deployment_observability
        deploy_obs = self._search_files(
            ".github/workflows/*.yml",
            r"(datadog|grafana|newrelic|deploy.*notify)"
        )
        results.append(self._make_result(
            "deployment_observability", pillar, 4, deploy_obs,
            "Deployment observability configured" if deploy_obs else "Add deployment tracking via Datadog, Grafana annotations, or deploy notifications"
        ))

        # L4: runbooks_documented
        runbooks = self._file_exists("runbooks/**", "docs/runbooks/**", "ops/**")
        results.append(self._make_result(
            "runbooks_documented", pillar, 4, runbooks,
            "Runbooks documented" if runbooks else "Add runbooks/ or docs/runbooks/ with incident response procedures"
        ))

        # L5: circuit_breakers
        circuit = any(x in deps.lower() for x in [
            "opossum", "resilience4j", "hystrix", "cockatiel"
        ])
        results.append(self._make_result(
            "circuit_breakers", pillar, 5, circuit,
            "Circuit breakers configured" if circuit else "Add opossum (Node), resilience4j (Java), or cockatiel (TS) for circuit breakers"
        ))

        return results

    def _evaluate_security(self) -> list[CriterionResult]:
        """Evaluate Security pillar."""
        pillar = "Security"
        results = []

        # L1: gitignore_comprehensive
        gitignore = self._file_exists(".gitignore")
        comprehensive = False
        if gitignore:
            content = self._read_file(".gitignore") or ""
            comprehensive = any(x in content.lower() for x in [
                ".env", "node_modules", "__pycache__", ".idea", ".vscode"
            ])
        results.append(self._make_result(
            "gitignore_comprehensive", pillar, 1, comprehensive,
            "Comprehensive .gitignore" if comprehensive else "Add .env, node_modules, __pycache__, .idea, .vscode to .gitignore"
        ))

        # L2: secrets_management
        secrets_mgmt = False
        workflows = list(self.repo_path.glob(".github/workflows/*.yml"))
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if "secrets." in content:
                secrets_mgmt = True
                break
        results.append(self._make_result(
            "secrets_management", pillar, 2, secrets_mgmt,
            "Secrets properly managed" if secrets_mgmt else "Use GitHub Secrets (${{ secrets.* }}) in workflows instead of hardcoded values"
        ))

        # L2: codeowners
        codeowners = self._file_exists("CODEOWNERS", ".github/CODEOWNERS")
        results.append(self._make_result(
            "codeowners", pillar, 2, codeowners,
            "CODEOWNERS configured" if codeowners else "Add .github/CODEOWNERS to define code ownership and review requirements"
        ))

        # L2: branch_protection
        branch_rules = self._file_exists(".github/branch-protection.yml", ".github/rulesets/**")
        results.append(self._make_result(
            "branch_protection", pillar, 2, branch_rules,
            "Branch protection configured" if branch_rules else "Enable branch protection rules in GitHub Settings or add .github/rulesets/"
        ))

        # L3: dependency_update_automation
        dep_updates = self._file_exists(
            ".github/dependabot.yml", "renovate.json", ".renovaterc"
        )
        results.append(self._make_result(
            "dependency_update_automation", pillar, 3, dep_updates,
            "Dependency updates automated" if dep_updates else "Add .github/dependabot.yml or renovate.json for automated dependency updates"
        ))

        # L3: log_scrubbing
        log_scrub = False
        deps = (self._read_file("package.json") or "") + \
               (self._read_file("requirements.txt") or "")
        if any(x in deps.lower() for x in ["pino", "redact", "scrub"]):
            log_scrub = True
        results.append(self._make_result(
            "log_scrubbing", pillar, 3, log_scrub,
            "Log scrubbing configured" if log_scrub else "Configure pino redact, loguru filters, or custom log sanitizers for sensitive data"
        ))

        # L3: pii_handling
        pii = self._search_files(
            "**/*.py", r"(redact|sanitize|mask|pii)"
        ) or self._search_files(
            "**/*.ts", r"(redact|sanitize|mask|pii)"
        )
        results.append(self._make_result(
            "pii_handling", pillar, 3, pii,
            "PII handling implemented" if pii else "Add redact/sanitize/mask functions for PII in logs, errors, and responses"
        ))

        # L4: automated_security_review
        security_scan = self._search_files(
            ".github/workflows/*.yml",
            r"(codeql|snyk|sonar|security)"
        )
        results.append(self._make_result(
            "automated_security_review", pillar, 4, security_scan,
            "Security scanning enabled" if security_scan else "Add CodeQL, Snyk, or SonarQube security scanning to CI workflow"
        ))

        # L4: secret_scanning
        secret_scan = self._search_files(
            ".github/workflows/*.yml",
            r"(gitleaks|trufflehog|secret)"
        )
        results.append(self._make_result(
            "secret_scanning", pillar, 4, secret_scan,
            "Secret scanning enabled" if secret_scan else "Add gitleaks or trufflehog to CI for secret scanning in commits"
        ))

        # L5: dast_scanning
        dast = self._search_files(
            ".github/workflows/*.yml",
            r"(zap|dast|owasp|burp)"
        )
        results.append(self._make_result(
            "dast_scanning", pillar, 5, dast,
            "DAST scanning enabled" if dast else "Add OWASP ZAP or Burp Suite DAST scanning in CI for runtime security testing"
        ))

        # L5: privacy_compliance
        privacy = self._file_exists(
            "PRIVACY.md", "docs/privacy/**", "gdpr/**"
        )
        results.append(self._make_result(
            "privacy_compliance", pillar, 5, privacy,
            "Privacy compliance documented" if privacy else "Add PRIVACY.md or docs/privacy/ with GDPR/CCPA compliance documentation"
        ))

        return results

    def _evaluate_task_discovery(self) -> list[CriterionResult]:
        """Evaluate Task Discovery pillar."""
        pillar = "Task Discovery"
        results = []

        # L2: issue_templates
        issue_templates = self._file_exists(
            ".github/ISSUE_TEMPLATE/**", ".github/ISSUE_TEMPLATE.md"
        )
        results.append(self._make_result(
            "issue_templates", pillar, 2, issue_templates,
            "Issue templates configured" if issue_templates else "Add .github/ISSUE_TEMPLATE/ with bug_report.md and feature_request.md"
        ))

        # L2: issue_labeling_system
        labels = False
        if issue_templates:
            templates = list(self.repo_path.glob(".github/ISSUE_TEMPLATE/*.md"))
            for t in templates[:5]:
                content = t.read_text(errors='ignore')
                if "labels:" in content.lower():
                    labels = True
                    break
        results.append(self._make_result(
            "issue_labeling_system", pillar, 2, labels,
            "Issue labels configured" if labels else "Add 'labels:' frontmatter to issue templates for automatic categorization"
        ))

        # L2: pr_templates
        pr_template = self._file_exists(
            ".github/pull_request_template.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
            "pull_request_template.md"
        )
        results.append(self._make_result(
            "pr_templates", pillar, 2, pr_template,
            "PR template configured" if pr_template else "Add .github/pull_request_template.md with checklist and description sections"
        ))

        # L3: backlog_health
        backlog = self._file_exists("CONTRIBUTING.md", ".github/CONTRIBUTING.md")
        results.append(self._make_result(
            "backlog_health", pillar, 3, backlog,
            "Contributing guidelines exist" if backlog else "Add CONTRIBUTING.md with setup instructions, coding standards, and PR process"
        ))

        return results

    def _evaluate_product_analytics(self) -> list[CriterionResult]:
        """Evaluate Product & Analytics pillar."""
        pillar = "Product & Analytics"
        results = []

        # L5: error_to_insight_pipeline
        error_pipeline = False
        workflows = list(self.repo_path.glob(".github/workflows/*.yml"))
        for wf in workflows[:5]:
            content = wf.read_text(errors='ignore')
            if any(x in content.lower() for x in ["sentry", "create.*issue", "error.*issue"]):
                error_pipeline = True
                break
        # Also check for Sentry-GitHub integration
        deps = (self._read_file("package.json") or "") + \
               (self._read_file("requirements.txt") or "") + \
               (self._read_file("go.mod") or "")
        if "sentry" in deps.lower():
            # Check for issue creation automation
            for wf in workflows[:5]:
                content = wf.read_text(errors='ignore')
                if "issue" in content.lower() and "sentry" in content.lower():
                    error_pipeline = True
                    break
        results.append(self._make_result(
            "error_to_insight_pipeline", pillar, 5, error_pipeline,
            "Error-to-issue pipeline exists" if error_pipeline else "Configure Sentry-GitHub integration to auto-create issues from production errors"
        ))

        # L5: product_analytics_instrumentation
        analytics = False
        if any(x in deps.lower() for x in [
            "mixpanel", "amplitude", "posthog", "heap", "segment", "ga4", "google-analytics"
        ]):
            analytics = True
        results.append(self._make_result(
            "product_analytics_instrumentation", pillar, 5, analytics,
            "Product analytics configured" if analytics else "Add Mixpanel, Amplitude, PostHog, or Segment for product usage analytics"
        ))

        return results

    def _calculate_levels(self):
        """Calculate maturity level based on criteria pass rates."""
        level_criteria: dict[int, list[CriterionResult]] = {i: [] for i in range(1, 6)}

        for pillar in self.result.pillars.values():
            for criterion in pillar.criteria:
                if criterion.status != CriterionStatus.SKIP:
                    level_criteria[criterion.level].append(criterion)

        for level in range(1, 6):
            criteria = level_criteria[level]
            if not criteria:
                self.result.level_scores[level] = 100.0
                continue

            passed = sum(1 for c in criteria if c.status == CriterionStatus.PASS)
            self.result.level_scores[level] = round((passed / len(criteria)) * 100, 1)

        achieved = 0
        for level in range(1, 6):
            if self.result.level_scores[level] >= 80:
                achieved = level
            else:
                break

        # Only set achieved level if at least L1 is passed
        self.result.achieved_level = achieved if achieved > 0 else 0


def main():
    parser = argparse.ArgumentParser(
        description="Analyze repository for agent readiness"
    )
    parser.add_argument(
        "--repo-path", "-r",
        default=".",
        help="Path to the repository to analyze"
    )
    parser.add_argument(
        "--output", "-o",
        default="/tmp/readiness_analysis.json",
        help="Output file for analysis results"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    if not args.quiet:
        print(f"Analyzing repository: {args.repo_path}")

    analyzer = RepoAnalyzer(args.repo_path)
    result = analyzer.analyze()

    # Get current git branch
    try:
        git_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=args.repo_path,
            capture_output=True,
            text=True
        ).stdout.strip() or "unknown"
    except Exception:
        git_branch = "unknown"

    output = {
        "repo_path": result.repo_path,
        "repo_name": result.repo_name,
        "repo_type": result.repo_type,
        "git_branch": git_branch,
        "generated_at": datetime.now().isoformat(),
        "languages": result.languages,
        "pass_rate": result.pass_rate,
        "total_passed": result.total_passed,
        "total_criteria": result.total_criteria,
        "achieved_level": result.achieved_level,
        "level_scores": result.level_scores,
        "detected_apps": [{"name": app.name, "path": str(app.path), "languages": app.languages} for app in result.detected_apps],
        "undetected_app_folders": result.undetected_app_folders,
        "pillars": {}
    }

    for pillar_name, pillar in result.pillars.items():
        output["pillars"][pillar_name] = {
            "name": pillar.name,
            "passed": pillar.passed,
            "total": pillar.total,
            "percentage": pillar.percentage,
            "criteria": [asdict(c) for c in pillar.criteria]
        }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2))

    if not args.quiet:
        print(f"Analysis complete: {result.total_passed}/{result.total_criteria} criteria passed ({result.pass_rate}%)")
        print(f"Achieved Level: L{result.achieved_level}")
        print(f"Results saved to: {args.output}")

    return result


if __name__ == "__main__":
    main()
