#!/usr/bin/env python3
"""Validate the knowledge-base structure without third-party dependencies."""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLES = {"system", "initiatives", "decisions", "sources", "archive"}
SPECIAL_ROOTS = {".git", "scratch", "tools", "target", "__pycache__"}
INITIATIVE_STATUSES = {
    "proposed",
    "approved",
    "in-progress",
    "blocked",
    "completed",
    "superseded",
    "rejected",
}
TASK_STATUSES = {"open", "completed", "abandoned", "superseded", "unknown"}
AGENT_ROLES = {"direct", "coordinator", "coder", "reviewer", "researcher"}
ENTRY_STATES = {
    "pending",
    "incorporated",
    "already-represented",
    "informational",
    "rejected",
    "superseded",
    "abandoned",
    "needs-owner",
}
ENTRY_TYPES = {
    "decision",
    "current-delta",
    "finding",
    "contract-change",
    "terminology-change",
    "constraint",
    "correction",
    "blocking-question",
    "source-adoption",
}
APPLICABILITY = {
    "local-development",
    "shared-development",
    "staging",
    "production",
    "environment-independent",
    "unknown",
}
VERIFICATION = {
    "verified",
    "unverified",
    "unverifiable-cheaply",
    "drifted",
    "obsolete",
    "not-required",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument(
        "--stale-days",
        type=int,
        default=int(os.environ.get("KB_STALE_DAYS", "120")),
        help="warn when current-system verification is older than this many days",
    )
    args = parser.parse_args()

    issues: list[tuple[str, str, str]] = []
    for required in ("README.md", "ORGANIZATION.md", "AGENTS.md", "CLAUDE.md"):
        if not (ROOT / required).is_file():
            add(issues, "ERROR", required, "required root file is missing")

    projects = find_projects(issues)
    validate_projects(projects, issues)

    markdown = sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in {".git", "scratch", "target", "__pycache__"} for part in path.parts)
    )
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in markdown:
        by_stem[path.stem].append(path)

    identifiers: dict[str, str] = {}
    for path in markdown:
        validate_document(
            path,
            projects,
            by_stem,
            identifiers,
            args.stale_days,
            issues,
        )

    issues.sort(key=lambda item: (item[0] != "ERROR", item[1], item[2]))
    for level, path, message in issues:
        print(f"{level}\t{path}\t{message}")
    errors = sum(level == "ERROR" for level, _, _ in issues)
    warnings = sum(level == "WARN" for level, _, _ in issues)
    print(
        f"checked={len(markdown)} projects={len(projects)} "
        f"errors={errors} warnings={warnings} strict={str(args.strict).lower()}"
    )
    return 1 if errors or (args.strict and warnings) else 0


def find_projects(issues: list[tuple[str, str, str]]) -> list[str]:
    projects: list[str] = []
    for path in ROOT.iterdir():
        if not path.is_dir() or path.name.startswith(".") or path.name in SPECIAL_ROOTS:
            continue
        has_role = any((path / role).is_dir() for role in ROLES)
        if (path / "README.md").is_file() and has_role:
            projects.append(path.name)
        else:
            add(
                issues,
                "ERROR",
                path.name,
                "top-level directory is neither reserved nor a project with README.md and a semantic role",
            )
    return sorted(projects)


def validate_projects(projects: list[str], issues: list[tuple[str, str, str]]) -> None:
    for project in projects:
        project_path = ROOT / project
        for child in project_path.iterdir():
            if not child.is_dir():
                continue
            if child.name not in ROLES:
                add(issues, "ERROR", rel(child), "project-root directory is not a semantic role")
                continue
            if not (child / "README.md").is_file():
                add(issues, "ERROR", rel(child), "semantic role requires README.md")

        initiatives = project_path / "initiatives"
        if initiatives.is_dir():
            for directory in sorted(path for path in initiatives.iterdir() if path.is_dir()):
                readme = directory / "README.md"
                if not readme.is_file():
                    add(issues, "ERROR", rel(directory), "material initiative requires README.md")
                    continue
                status = top_label(readme.read_text(encoding="utf-8"), "Status")
                if status not in INITIATIVE_STATUSES:
                    add(
                        issues,
                        "ERROR",
                        rel(readme),
                        f"initiative Status must be controlled; found {status!r}",
                    )

        archived = project_path / "archive" / "initiatives"
        if archived.is_dir():
            for directory in sorted(path for path in archived.iterdir() if path.is_dir()):
                readme = directory / "README.md"
                if not readme.is_file():
                    add(issues, "ERROR", rel(directory), "archived initiative requires README.md")
                    continue
                if top_label(readme.read_text(encoding="utf-8"), "Archived") is None:
                    add(issues, "ERROR", rel(readme), "archived initiative requires an Archived date")


def validate_document(
    path: Path,
    projects: list[str],
    by_stem: dict[str, list[Path]],
    identifiers: dict[str, str],
    stale_days: int,
    issues: list[tuple[str, str, str]],
) -> None:
    relative = rel(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        add(issues, "ERROR", relative, f"Markdown is not valid UTF-8: {exc}")
        return

    frontmatter = parse_frontmatter(text)
    if identifier := frontmatter.get("id"):
        record_identifier(identifier, relative, identifiers, issues)
    for match in re.finditer(r"^### ([A-Z]+-\d{4}-\d{3})\b", text, re.MULTILINE):
        record_identifier(match.group(1), relative, identifiers, issues)

    if is_system_document(relative):
        status = top_label(text, "Status")
        if status is not None and status != "current":
            add(
                issues,
                "ERROR",
                relative,
                f"current-system document has non-current top-level Status: {status}",
            )

    validate_metadata(relative, text, frontmatter, stale_days, issues)
    if is_task_log(relative):
        validate_task_log(relative, text, frontmatter, identifiers, issues)

    clean = strip_fenced_code(text)
    for kind, raw in extract_links(clean):
        target, problem = resolve_link(path, kind, raw, projects, by_stem)
        if problem:
            add(issues, "ERROR", relative, problem)
        elif target is not None and is_default_index(relative) and "/archive/" in rel(target):
            target_rel = rel(target)
            project_archive_index = relative.count("/") == 1 and target_rel.endswith(
                "/archive/README.md"
            )
            if not project_archive_index:
                add(
                    issues,
                    "ERROR",
                    relative,
                    f"default reading index links directly into archive: {target_rel}",
                )


def validate_metadata(
    relative: str,
    text: str,
    frontmatter: dict[str, str],
    stale_days: int,
    issues: list[tuple[str, str, str]],
) -> None:
    if applicability := frontmatter.get("applicability"):
        if applicability not in APPLICABILITY and not applicability.startswith("environment:"):
            add(issues, "ERROR", relative, f"unknown applicability: {applicability}")
    if verification := frontmatter.get("verification"):
        if verification not in VERIFICATION:
            add(issues, "ERROR", relative, f"unknown verification value: {verification}")
        if verification == "verified":
            for required in ("last_verified", "verification_source"):
                if not frontmatter.get(required):
                    add(
                        issues,
                        "ERROR",
                        relative,
                        f"verification=verified requires {required}",
                    )

    verified = frontmatter.get("last_verified") or top_label(text, "Last verified")
    if verified:
        try:
            verified_date = date.fromisoformat(verified)
        except ValueError:
            add(issues, "ERROR", relative, f"invalid last_verified ISO date: {verified}")
        else:
            age = (date.today() - verified_date).days
            if is_system_document(relative) and age > stale_days:
                add(
                    issues,
                    "WARN",
                    relative,
                    f"current-system verification is {age} days old (limit {stale_days})",
                )


def validate_task_log(
    relative: str,
    text: str,
    frontmatter: dict[str, str],
    identifiers: dict[str, str],
    issues: list[tuple[str, str, str]],
) -> None:
    required = {
        "id",
        "task_id",
        "project",
        "agent_role",
        "status",
        "applicability",
        "opened",
        "last_activity",
    }
    for field in sorted(required - frontmatter.keys()):
        add(issues, "ERROR", relative, f"task log missing frontmatter field: {field}")
    if frontmatter.get("agent_role") not in AGENT_ROLES:
        add(issues, "ERROR", relative, f"unknown agent_role: {frontmatter.get('agent_role')!r}")
    if frontmatter.get("status") not in TASK_STATUSES:
        add(issues, "ERROR", relative, f"unknown task status: {frontmatter.get('status')!r}")
    expected_project = relative.split("/", 1)[0]
    if frontmatter.get("project") != expected_project:
        add(
            issues,
            "ERROR",
            relative,
            f"task project must match owning path {expected_project!r}",
        )
    applicability = frontmatter.get("applicability", "")
    if applicability not in APPLICABILITY and not applicability.startswith("environment:"):
        add(issues, "ERROR", relative, f"unknown task applicability: {applicability!r}")
    for field in ("opened", "last_activity"):
        try:
            date.fromisoformat(frontmatter.get(field, ""))
        except ValueError:
            add(issues, "ERROR", relative, f"task log has invalid {field} date")

    entries = list(re.finditer(r"^## ([^\n—]+?)\s+—\s+([^\n]+)$", text, re.MULTILINE))
    for index, match in enumerate(entries):
        entry_id = match.group(1).strip()
        record_identifier(entry_id, relative, identifiers, issues)
        start = match.end()
        end = entries[index + 1].start() if index + 1 < len(entries) else len(text)
        fields = dict(
            (key.strip(), value.strip())
            for key, value in re.findall(r"^- ([^:\n]+):\s*(.*)$", text[start:end], re.MULTILINE)
        )
        for field in (
            "Timestamp",
            "Type",
            "State",
            "Statement",
            "Rationale",
            "Evidence",
            "Destinations",
        ):
            if field not in fields:
                add(issues, "ERROR", relative, f"task entry {entry_id} missing field: {field}")
        entry_type = fields.get("Type")
        if entry_type not in ENTRY_TYPES:
            add(
                issues,
                "ERROR",
                relative,
                f"task entry {entry_id} has unknown type: {entry_type!r}",
            )
        state = fields.get("State")
        if state not in ENTRY_STATES:
            add(issues, "ERROR", relative, f"task entry {entry_id} has unknown state: {state!r}")
        if state and state != "pending" and not fields.get("Disposition note"):
            add(
                issues,
                "ERROR",
                relative,
                f"task entry {entry_id} requires a disposition note for state {state}",
            )
        timestamp = fields.get("Timestamp", "").replace("Z", "+00:00")
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            add(issues, "ERROR", relative, f"task entry {entry_id} has invalid Timestamp")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def top_label(text: str, label: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(label)}:\s*(.*?)\s*$", re.IGNORECASE)
    for line in text.splitlines()[:30]:
        if match := pattern.match(line.strip()):
            return match.group(1)
    return None


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.DOTALL)


def extract_links(text: str) -> list[tuple[str, str]]:
    links = [("wiki", match.group(1)) for match in re.finditer(r"\[\[([^\]]+)\]\]", text)]
    links += [
        ("markdown", match.group(1))
        for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)
    ]
    return links


def resolve_link(
    source: Path,
    kind: str,
    raw: str,
    projects: list[str],
    by_stem: dict[str, list[Path]],
) -> tuple[Path | None, str | None]:
    if kind == "markdown":
        target = clean_markdown_target(raw)
        if not target or target.startswith("#") or is_external(target):
            return None, None
        target = target.split("#", 1)[0]
        candidate = ROOT / target.lstrip("/") if target.startswith("/") else source.parent / target
        resolved = resolve_candidate(candidate)
        return (resolved, None) if resolved else (None, f"missing Markdown link target: {raw}")

    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return None, None
    if target.split("/", 1)[0] in projects:
        resolved = resolve_candidate(ROOT / target)
        return (resolved, None) if resolved else (None, f"missing wiki link target: {raw}")
    if "/" in target or target.startswith("."):
        resolved = resolve_candidate(source.parent / target)
        return (resolved, None) if resolved else (None, f"missing wiki link target: {raw}")
    if local := resolve_candidate(source.parent / target):
        return local, None
    matches = by_stem.get(target, [])
    if len(matches) == 1:
        return matches[0], None
    if not matches:
        return None, f"missing wiki link target: {raw}"
    return None, f"ambiguous wiki link target ({len(matches)} matches): {raw}"


def clean_markdown_target(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1 : raw.index(">")]
    return raw.split(maxsplit=1)[0] if raw else ""


def resolve_candidate(candidate: Path) -> Path | None:
    candidate = candidate.resolve(strict=False)
    if candidate.is_dir() and (candidate / "README.md").is_file():
        return candidate / "README.md"
    if candidate.is_file():
        return candidate
    markdown = Path(f"{candidate}.md")
    return markdown if markdown.is_file() else None


def is_external(target: str) -> bool:
    return bool(re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE))


def is_system_document(relative: str) -> bool:
    parts = relative.split("/")
    return len(parts) >= 3 and parts[1] == "system" and relative.endswith(".md")


def is_task_log(relative: str) -> bool:
    return (
        "/decisions/tasks/" in relative
        and relative.endswith(".md")
        and not relative.endswith(("/README.md", "/INDEX.md"))
    )


def is_default_index(relative: str) -> bool:
    parts = relative.split("/")
    return (
        relative == "README.md"
        or (len(parts) == 2 and parts[1] == "README.md")
        or (
            len(parts) == 3
            and parts[1] in {"system", "initiatives"}
            and parts[2] == "README.md"
        )
        or ("/system/" in relative and relative.endswith("/overview.md"))
    )


def record_identifier(
    identifier: str,
    relative: str,
    identifiers: dict[str, str],
    issues: list[tuple[str, str, str]],
) -> None:
    if first := identifiers.get(identifier):
        if first != relative:
            add(
                issues,
                "ERROR",
                relative,
                f"duplicate stable identifier {identifier}; first seen in {first}",
            )
    else:
        identifiers[identifier] = relative


def rel(path: Path) -> str:
    return path.resolve(strict=False).relative_to(ROOT).as_posix()


def add(issues: list[tuple[str, str, str]], level: str, path: str, message: str) -> None:
    issues.append((level, path, message))


if __name__ == "__main__":
    sys.exit(main())
