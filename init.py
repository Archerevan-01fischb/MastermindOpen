"""
Mastermind installer for Claude Code.
=====================================

Cross-platform Python stdlib-only installer. Two modes:

  python init.py            — first-time install (creates memory dir,
                              merges settings, drops onboarding flag)

  python init.py bootstrap  — create a new project under your existing
                              mastermind (drafts CLAUDE.md, initializes
                              the project memory dir, updates Project
                              Registry)

The installer is idempotent — re-running detects existing setup and only
fills in missing pieces. No overwrites without confirmation.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo-relative paths (resolved at runtime)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent
REPO_MEMORY = REPO_ROOT / "memory"
REPO_SETTINGS = REPO_ROOT / "settings"
REPO_TEMPLATES = REPO_ROOT / "templates"


def detect_claude_dir() -> Path:
    """Find ~/.claude (cross-platform)."""
    home = Path.home()
    claude = home / ".claude"
    return claude


def detect_existing_memory_dir(claude_dir: Path) -> Path | None:
    """If a memory dir already exists under ~/.claude/projects, return it."""
    projects = claude_dir / "projects"
    if not projects.exists():
        return None
    candidates = list(projects.glob("*/memory"))
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    # Multiple — return the most recently modified.
    return max(candidates, key=lambda p: p.stat().st_mtime)


def ask(question: str, default: str = "") -> str:
    prompt = f"{question}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    answer = input(prompt).strip()
    return answer or default


def ask_yes_no(question: str, default: bool = False) -> bool:
    default_str = "Y/n" if default else "y/N"
    answer = input(f"{question} [{default_str}]: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def ask_multi(question: str, options: list[str]) -> list[str]:
    """Ask the user to pick zero or more options from a list."""
    print(f"\n{question}")
    print("  Enter numbers separated by commas, or 'all', or 'none'.")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    raw = input("> ").strip().lower()
    if raw in ("none", ""):
        return []
    if raw == "all":
        return options[:]
    selected = []
    for token in raw.split(","):
        token = token.strip()
        if token.isdigit():
            idx = int(token) - 1
            if 0 <= idx < len(options):
                selected.append(options[idx])
    return selected


def substitute_placeholders(text: str, mapping: dict[str, str]) -> str:
    """Replace {USER}-style placeholders with values."""
    out = text
    for key, value in mapping.items():
        out = out.replace("{" + key + "}", value)
    return out


def copy_with_substitution(src: Path, dst: Path, mapping: dict[str, str]) -> None:
    """Copy a file with text substitution applied (for text files)."""
    if dst.exists():
        # Idempotent — skip if dst already exists (don't overwrite user edits).
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        text = src.read_text(encoding="utf-8")
        text = substitute_placeholders(text, mapping)
        dst.write_text(text, encoding="utf-8")
    except UnicodeDecodeError:
        # Binary file — copy without substitution.
        shutil.copy2(src, dst)


def cmd_init(args: argparse.Namespace) -> int:
    print("Welcome to Mastermind for Claude Code by DrEvil.")
    print()

    # --- Q1: user name ---
    user = ask("What name should Claude call you?", "Alex")
    user_slug = re.sub(r"[^a-z0-9]+", "_", user.lower()).strip("_") or "user"

    # --- Q2: memory dir ---
    claude_dir = detect_claude_dir()
    existing_memory = detect_existing_memory_dir(claude_dir)
    if existing_memory:
        print(f"\nFound existing Claude Code memory dir: {existing_memory}")
        if ask_yes_no("Install mastermind into this dir?", default=True):
            memory_dir = existing_memory
        else:
            memory_dir = Path(ask(
                "Where do you want your memory dir?",
                str(claude_dir / "projects" / "mastermind" / "memory"),
            ))
    else:
        memory_dir = Path(ask(
            "Where do you want your memory dir?",
            str(claude_dir / "projects" / "mastermind" / "memory"),
        ))
    memory_dir = memory_dir.expanduser().resolve()

    # --- Q3: snapshot target ---
    snapshot_root_raw = ask(
        "Where to store memory snapshots? ('skip' for none)",
        str(Path.home() / "mastermind-snapshots"),
    )
    snapshot_root = None if snapshot_root_raw.lower() == "skip" else Path(snapshot_root_raw).expanduser().resolve()

    # --- Q4: integrations ---
    available_integrations = [
        "Telegram (DM control + boot pings)",
        "Gmail (read/write via gmail-multi MCP)",
        "Google Calendar",
        "Google Drive",
        "Home Assistant (smart home + remote PC power)",
        "DocuSign",
        "QuickBooks",
    ]
    integrations = ask_multi(
        "Which integrations do you want to enable?",
        available_integrations,
    )

    # --- Q5: optional Windows startup chain ---
    windows_startup = False
    if sys.platform.startswith("win"):
        windows_startup = ask_yes_no(
            "\nDo you want the Windows startup chain (auto-launch Claude Code on login)?",
            default=False,
        )

    # --- Q6: optional HA SSH-fallback shutdown chain ---
    shutdown_chain = False
    if any("Home Assistant" in s for s in integrations):
        shutdown_chain = ask_yes_no(
            "Do you want the HA SSH-fallback shutdown chain (advanced)?",
            default=False,
        )

    print()
    print(f"> Claude Code config dir:   {claude_dir}")
    print(f"> Memory dir:               {memory_dir}")
    if snapshot_root:
        print(f"> Snapshot target:          {snapshot_root}")
    print(f"> Integrations:             {len(integrations)} selected")
    print()

    if not ask_yes_no("Proceed?", default=True):
        print("Aborted.")
        return 1

    # ---- Do the install ----

    placeholders = {
        "USER": user_slug,
        "USER_DISPLAY": user,
        "MEMORY_DIR": str(memory_dir).replace("\\", "/"),
        "HOME": str(Path.home()).replace("\\", "/"),
        "PROJECT_ROOT": str(Path.cwd()).replace("\\", "/"),
        "SNAPSHOT_ROOT": str(snapshot_root).replace("\\", "/") if snapshot_root else str(Path.home() / "mastermind-snapshots").replace("\\", "/"),
    }

    # 1. Copy memory templates to memory_dir
    print(f"> Copying memory templates to {memory_dir}/...")
    memory_dir.mkdir(parents=True, exist_ok=True)
    (memory_dir / "session_archive").mkdir(exist_ok=True)
    (memory_dir / "scripts").mkdir(exist_ok=True)

    for src in REPO_MEMORY.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(REPO_MEMORY)
        # Rename user_{USER}.md → user_<user_slug>.md
        rel_str = str(rel).replace("{USER}", user_slug)
        dst = memory_dir / rel_str
        copy_with_substitution(src, dst, placeholders)

    # 2. Personalize MEMORY.md header
    memory_md = memory_dir / "MEMORY.md"
    if memory_md.exists():
        text = memory_md.read_text(encoding="utf-8")
        text = text.replace("Memory Index for {USER}", f"Memory Index for {user}")
        memory_md.write_text(text, encoding="utf-8")

    # 3. Settings.json merge
    settings_template = REPO_SETTINGS / "settings.json.template"
    user_settings_path = claude_dir / "settings.json"
    if settings_template.exists():
        print(f"> Merging settings.json template into {user_settings_path}...")
        template_text = settings_template.read_text(encoding="utf-8")
        template_text = substitute_placeholders(template_text, placeholders)
        # Strip _comment_ keys from the template before parsing.
        template_text = re.sub(r'"_comment_?"\s*:\s*"[^"]*"\s*,?\s*\n', "", template_text)
        template_text = re.sub(r'"_note_"\s*:\s*"[^"]*"\s*,?\s*\n', "", template_text)
        # Tidy trailing commas if any.
        template_text = re.sub(r",(\s*[}\]])", r"\1", template_text)

        try:
            template_obj = json.loads(template_text)
        except json.JSONDecodeError as e:
            print(f"  WARNING: settings.json template didn't parse cleanly ({e}). Skipping merge — fill in by hand.")
            template_obj = None

        if template_obj:
            if user_settings_path.exists():
                try:
                    user_obj = json.loads(user_settings_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    print(f"  Your existing settings.json didn't parse — leaving it alone. Edit by hand.")
                    user_obj = None
            else:
                user_obj = {}
            if user_obj is not None:
                # Non-destructive merge: only add keys missing on user side.
                def merge(target: dict, source: dict) -> None:
                    for k, v in source.items():
                        if k not in target:
                            target[k] = v
                        elif isinstance(v, dict) and isinstance(target.get(k), dict):
                            merge(target[k], v)
                merge(user_obj, template_obj)
                user_settings_path.parent.mkdir(parents=True, exist_ok=True)
                user_settings_path.write_text(json.dumps(user_obj, indent=2), encoding="utf-8")

    # 4. Statusline.ps1
    statusline_template = REPO_SETTINGS / "statusline.ps1.template"
    statusline_dst = claude_dir / "statusline.ps1"
    if statusline_template.exists() and not statusline_dst.exists():
        statusline_dst.parent.mkdir(parents=True, exist_ok=True)
        text = statusline_template.read_text(encoding="utf-8")
        text = substitute_placeholders(text, placeholders)
        statusline_dst.write_text(text, encoding="utf-8")
        print(f"> Installed statusline at {statusline_dst}")

    # 5. Write .onboarding_pending flag
    onboarding_pending = memory_dir / ".onboarding_pending"
    onboarding_pending.write_text(
        json.dumps({
            "user": user,
            "user_slug": user_slug,
            "integrations": integrations,
            "windows_startup": windows_startup,
            "shutdown_chain": shutdown_chain,
        }, indent=2),
        encoding="utf-8",
    )

    print()
    print("Done. Setup complete.")
    print()
    print("Next steps:")
    print("  1. Open Claude Code in your project root.")
    print('  2. Say (exactly): "Mastermind waking up for the first time."')
    print("  3. I'll walk you through populating your templates (about 5 minutes).")
    print()
    print("If you skip step 2, mastermind will still detect you're new and start")
    print("onboarding automatically — but the magic phrase is the proper invocation.")
    print()
    if integrations:
        print(f"After onboarding completes, the per-integration setup guides at")
        print(f"integrations/<name>.md walk you through credentials for each")
        print(f"enabled integration:")
        for i in integrations:
            short = i.split(" ")[0].lower()
            print(f"  - integrations/{short}.md")
        print()
    return 0


# ---------------------------------------------------------------------------
# `python init.py bootstrap` — create a new project under existing mastermind
# ---------------------------------------------------------------------------

PROJECT_TYPES = ["general", "web-service", "business", "game", "document-library"]


def cmd_bootstrap(args: argparse.Namespace) -> int:
    print("Mastermind project bootstrap")
    print()

    name = ask("What's the project name?", "my-cool-thing")
    name_slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "project"

    print(f"\nProject types: {' / '.join(PROJECT_TYPES)}")
    type_ = ask("What type?", "general")
    if type_ not in PROJECT_TYPES:
        print(f"Unknown type '{type_}'. Use one of: {PROJECT_TYPES}")
        return 1

    description = ask("Brief description (1 sentence)", "")

    default_dir = str(Path.home() / "projects" / name)
    project_dir = Path(ask("Where should the project live?", default_dir)).expanduser().resolve()

    spawn_child = ask_yes_no("Spawn a dedicated child Claude?", default=False)
    child_name = ""
    if spawn_child:
        child_name = ask("Child Claude name (e.g. Frostsmith)", "")
        if not child_name:
            print("Empty name — skipping child setup.")
            spawn_child = False

    print()
    print(f"> Project dir: {project_dir}")
    print(f"> Type:        {type_}")
    print(f"> Description: {description}")
    if spawn_child:
        print(f"> Child Claude: {child_name}")
    print()
    if not ask_yes_no("Proceed?", default=True):
        print("Aborted.")
        return 1

    # Create project dir.
    project_dir.mkdir(parents=True, exist_ok=True)

    # Draft CLAUDE.md from template.
    template_path = REPO_TEMPLATES / "project-types" / type_ / "CLAUDE.md.template"
    if not template_path.exists():
        print(f"Template not found: {template_path}")
        return 1
    claude_md_path = project_dir / "CLAUDE.md"
    if not claude_md_path.exists():
        text = template_path.read_text(encoding="utf-8")
        mapping = {
            "PROJECT_NAME": name,
            "PROJECT_SLUG": name_slug,
            "ONE_PARAGRAPH_DESCRIPTION": description or "TBD",
            "PROJECT_TYPE": type_,
            "PARENT_DIR": str(project_dir.parent).replace("\\", "/"),
        }
        text = substitute_placeholders(text, mapping)
        claude_md_path.write_text(text, encoding="utf-8")
        print(f"> Drafted {claude_md_path}")
    else:
        print(f"> {claude_md_path} already exists — skipping.")

    # Initialize project memory dir (best-effort — we don't know Claude Code's
    # hash, so we just create a memory file template in the project dir's
    # memory subdir if it exists, or instruct the user).
    project_memory_md = project_dir / "PROJECT_MEMORY_TEMPLATE.md"
    bootstrap_memory_tmpl = REPO_TEMPLATES / "project-bootstrap-memory.md.template"
    if bootstrap_memory_tmpl.exists() and not project_memory_md.exists():
        text = bootstrap_memory_tmpl.read_text(encoding="utf-8")
        text = substitute_placeholders(text, {
            "PROJECT_NAME": name,
            "PROJECT_SLUG": name_slug,
            "ONE_LINE_DESCRIPTION": description,
            "CREATED_DATE": "today",
            "PROJECT_TYPE": type_,
            "PROJECT_PATH": str(project_dir).replace("\\", "/"),
            "STATUS": "active",
        })
        project_memory_md.write_text(text, encoding="utf-8")
        print(f"> Wrote {project_memory_md}")
        print(f"  Move this into Claude Code's per-project memory dir on first run.")

    print()
    print("Done.")
    print()
    print(f"Open Claude Code in {project_dir} and say:")
    print(f'  "Project waking up for the first time."')
    print()
    if spawn_child:
        print(f"Child Claude '{child_name}' setup: write CLAUDE.md identifying")
        print(f"the project Claude as '{child_name}' (see docs/projects/child-mastermind-pattern.md).")
    return 0


# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="init.py", description="Mastermind installer.")
    subparsers = parser.add_subparsers(dest="cmd")

    bootstrap = subparsers.add_parser("bootstrap", help="Create a new project under existing mastermind")
    bootstrap.set_defaults(func=cmd_bootstrap)

    parser.set_defaults(func=cmd_init)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
