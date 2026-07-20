from __future__ import annotations

import argparse
import csv
import os
import shutil
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


LOG_FIELDS = [
    "date",
    "session",
    "exercise",
    "sets",
    "reps",
    "load_kg",
    "rir",
    "rpe",
    "status",
    "pain_notes",
    "notes",
]


def default_data_dir() -> Path:
    configured = os.environ.get("FITNESS_COACH_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".fitness-coach"


def data_dir(value: str | None) -> Path:
    return Path(value).expanduser() if value else default_data_dir()


def asset_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "assets"


def initialize(destination: Path, force: bool) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "weekly-reviews").mkdir(exist_ok=True)
    files = {
        "profile-template.md": "profile.md",
        "current-plan-template.md": "current-plan.md",
        "training-log-template.csv": "training-log.csv",
    }
    created = []
    skipped = []
    for source_name, target_name in files.items():
        source = asset_dir() / source_name
        target = destination / target_name
        if target.exists() and not force:
            skipped.append(target_name)
            continue
        shutil.copyfile(source, target)
        created.append(target_name)
    check_ins = destination / "check-ins.md"
    if not check_ins.exists() or force:
        check_ins.write_text("# Check-ins\n", encoding="utf-8")
        created.append("check-ins.md")
    print(f"data_dir={destination}")
    if created:
        print(f"created={','.join(created)}")
    if skipped:
        print(f"skipped={','.join(skipped)}")


def parse_iso_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def non_negative(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("value must be numeric") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must not be negative")
    return parsed


def optional_non_negative(value: str | None) -> str:
    if value is None:
        return ""
    return format(non_negative(value), "g")


def append_log(args: argparse.Namespace) -> None:
    destination = data_dir(args.data_dir)
    log_path = destination / "training-log.csv"
    if not log_path.exists():
        raise FileNotFoundError(f"training log not found: {log_path}. Run init first.")
    row = {
        "date": parse_iso_date(args.date),
        "session": args.session.strip(),
        "exercise": args.exercise.strip(),
        "sets": format(non_negative(args.sets), "g"),
        "reps": format(non_negative(args.reps), "g"),
        "load_kg": format(non_negative(args.load_kg), "g"),
        "rir": optional_non_negative(args.rir),
        "rpe": optional_non_negative(args.rpe),
        "status": args.status,
        "pain_notes": args.pain_notes.strip(),
        "notes": args.notes.strip(),
    }
    if not row["session"] or not row["exercise"]:
        raise ValueError("session and exercise must not be empty")
    with log_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS)
        writer.writerow(row)
    print(f"appended={row['date']}|{row['session']}|{row['exercise']}")


def load_rows(log_path: Path) -> list[dict[str, str]]:
    if not log_path.exists():
        raise FileNotFoundError(f"training log not found: {log_path}. Run init first.")
    with log_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != LOG_FIELDS:
            raise ValueError("training-log.csv has an unexpected header")
        return list(reader)


def summarize(args: argparse.Namespace) -> None:
    destination = data_dir(args.data_dir)
    rows = load_rows(destination / "training-log.csv")
    end = date.fromisoformat(args.end) if args.end else date.today()
    start = end - timedelta(days=args.days - 1)
    selected = []
    for row in rows:
        try:
            row_date = date.fromisoformat(row["date"])
        except ValueError:
            continue
        if start <= row_date <= end:
            selected.append(row)
    sessions = {(row["date"], row["session"]) for row in selected if row["status"] == "completed"}
    volume_by_exercise: dict[str, float] = defaultdict(float)
    completed_sets = 0.0
    for row in selected:
        if row["status"] != "completed":
            continue
        sets = float(row["sets"] or 0)
        reps = float(row["reps"] or 0)
        load = float(row["load_kg"] or 0)
        completed_sets += sets
        volume_by_exercise[row["exercise"]] += sets * reps * load
    print(f"period={start.isoformat()}..{end.isoformat()}")
    print(f"logged_rows={len(selected)}")
    print(f"completed_sessions={len(sessions)}")
    print(f"completed_sets={format(completed_sets, 'g')}")
    for exercise in sorted(volume_by_exercise):
        print(f"volume_kg[{exercise}]={format(volume_by_exercise[exercise], 'g')}")


def show_paths(args: argparse.Namespace) -> None:
    destination = data_dir(args.data_dir)
    print(f"data_dir={destination}")
    for relative in ["profile.md", "current-plan.md", "training-log.csv", "check-ins.md", "weekly-reviews"]:
        path = destination / relative
        print(f"{relative}={'present' if path.exists() else 'missing'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local fitness-coach data.")
    parser.add_argument("--data-dir", help="Override FITNESS_COACH_HOME and the default data directory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create the local profile, plan, log, and review files.")
    init_parser.add_argument("--force", action="store_true", help="Replace existing template files.")
    init_parser.set_defaults(handler=lambda args: initialize(data_dir(args.data_dir), args.force))

    append_parser = subparsers.add_parser("append-log", help="Append one completed, skipped, or partial exercise entry.")
    append_parser.add_argument("--date", required=True)
    append_parser.add_argument("--session", required=True)
    append_parser.add_argument("--exercise", required=True)
    append_parser.add_argument("--sets", required=True)
    append_parser.add_argument("--reps", required=True)
    append_parser.add_argument("--load-kg", required=True)
    append_parser.add_argument("--rir")
    append_parser.add_argument("--rpe")
    append_parser.add_argument("--status", choices=["completed", "partial", "skipped"], default="completed")
    append_parser.add_argument("--pain-notes", default="")
    append_parser.add_argument("--notes", default="")
    append_parser.set_defaults(handler=append_log)

    summary_parser = subparsers.add_parser("summary", help="Summarize training logs for a recent period.")
    summary_parser.add_argument("--days", type=int, default=7)
    summary_parser.add_argument("--end", type=parse_iso_date)
    summary_parser.set_defaults(handler=summarize)

    paths_parser = subparsers.add_parser("paths", help="Show local data file locations and presence.")
    paths_parser.set_defaults(handler=show_paths)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "days", 1) < 1:
        parser.error("--days must be at least 1")
    try:
        args.handler(args)
    except (argparse.ArgumentTypeError, FileNotFoundError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
