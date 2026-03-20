from __future__ import annotations

import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ParticipantInfo:
    participant_id: str
    session_id: str
    name: str
    age: str
    extra_fields: dict[str, str] = field(default_factory=dict)

    def to_record(self) -> dict[str, str]:
        record = {
            "participant_id": self.participant_id,
            "session_id": self.session_id,
            "name": self.name,
            "age": self.age,
        }
        record.update(self.extra_fields)
        return record


def collect_participant_info(
    participant_id: str,
    session_id: str,
    name: str = "",
    age: str = "",
    skip_dialog: bool = False,
) -> ParticipantInfo:
    defaults = {
        "name": name,
        "participant_id": participant_id,
        "age": age,
        "session_id": session_id,
    }

    if skip_dialog:
        return _validate_participant_info(defaults)

    try:
        from psychopy import gui  # type: ignore
    except ModuleNotFoundError:
        return _collect_from_terminal(defaults)

    dialog = gui.Dlg(title="被试信息", alwaysOnTop=True)
    dialog.addText("请输入本次实验的被试信息")
    dialog.addField("姓名", defaults["name"])
    dialog.addField("被试号", defaults["participant_id"])
    dialog.addField("年龄", defaults["age"])
    dialog.addField("Session", defaults["session_id"])
    values = dialog.show()

    if not dialog.OK:
        raise RuntimeError("Participant info entry cancelled.")

    return _validate_participant_info(
        {
            "name": values[0],
            "participant_id": values[1],
            "age": values[2],
            "session_id": values[3],
        }
    )


def write_participant_info(
    output_dir: Path,
    participant_info: ParticipantInfo,
    run_id: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "run_id": run_id,
        **participant_info.to_record(),
    }

    json_path = output_dir / "participant_info.json"
    csv_path = output_dir / "participant_info.csv"

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(record, handle, ensure_ascii=False, indent=2)

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(record.keys()))
        writer.writeheader()
        writer.writerow(record)


def _collect_from_terminal(defaults: dict[str, str]) -> ParticipantInfo:
    if not sys.stdin.isatty():
        return _validate_participant_info(defaults)

    print("请输入本次实验的被试信息：")
    record = {
        "name": _prompt("姓名", defaults["name"]),
        "participant_id": _prompt("被试号", defaults["participant_id"]),
        "age": _prompt("年龄", defaults["age"]),
        "session_id": _prompt("Session", defaults["session_id"]),
    }
    return _validate_participant_info(record)


def _prompt(label: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    if raw:
        return raw
    return default


def _validate_participant_info(raw_record: dict[str, str]) -> ParticipantInfo:
    cleaned = {key: str(value).strip() for key, value in raw_record.items()}
    missing = [label for label, value in _required_fields(cleaned).items() if not value]
    if missing:
        labels = ", ".join(missing)
        raise RuntimeError(f"Missing required participant fields: {labels}.")

    return ParticipantInfo(
        participant_id=cleaned["participant_id"],
        session_id=cleaned["session_id"],
        name=cleaned["name"],
        age=cleaned["age"],
    )


def _required_fields(cleaned: dict[str, str]) -> dict[str, str]:
    return {
        "name": cleaned.get("name", ""),
        "participant_id": cleaned.get("participant_id", ""),
        "age": cleaned.get("age", ""),
        "session_id": cleaned.get("session_id", ""),
    }
