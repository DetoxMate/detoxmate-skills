#!/usr/bin/env python3
"""Link the same team skills into Codex and/or Claude Code. Python 3 only."""
import argparse
from pathlib import Path

NAMES = ("fetch-notion-wiki", "update-notion-wiki")
LOCATIONS = {"codex": ".agents/skills", "claude": ".claude/skills"}


def install(target, home, source_root):
    targets = tuple(LOCATIONS) if target == "both" else (target,)
    plan = []
    conflicts = []
    seen = set()
    for client in targets:
        for name in NAMES:
            source = source_root / "skills" / name
            if not (source / "SKILL.md").is_file():
                raise RuntimeError(f"Missing skill: {source}")
            destination = home / LOCATIONS[client] / name
            # Resolve only the parent: never follow an unrelated skill link.
            key = destination.parent.resolve() / destination.name
            if key in seen:
                continue
            seen.add(key)
            if destination.is_symlink() and destination.resolve() == source.resolve():
                plan.append((source, destination, False))
            elif destination.exists() or destination.is_symlink():
                conflicts.append(str(destination))
            else:
                plan.append((source, destination, True))
    if conflicts:
        raise RuntimeError("Existing skills were not changed. Resolve these names first:\n" + "\n".join(conflicts))
    created = []
    try:
        for source, destination, needed in plan:
            if needed:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.symlink_to(source.resolve(), target_is_directory=True)
                created.append(destination)
            print(f"{'Linked' if needed else 'Already linked'}: {destination}")
    except OSError:
        for destination in reversed(created):
            destination.unlink()
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=("codex", "claude", "both"))
    parser.add_argument("--home", type=Path, default=Path.home(), help="Installation home (default: current user)")
    args = parser.parse_args()
    try:
        install(args.target, args.home.expanduser().resolve(), Path(__file__).resolve().parent)
    except (OSError, RuntimeError) as exc:
        parser.exit(1, f"{exc}\n")
