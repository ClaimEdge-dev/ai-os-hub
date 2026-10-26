"""DEBO Phase 2 local command-core pilot. No external calls or production access.

This is an isolated reference adapter, not the canonical Neon runtime.
"""
from __future__ import annotations

import json
import hashlib
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path


STATES = frozenset({"CAPTURED", "READY", "WAITING_APPROVAL", "BLOCKED", "RUNNING", "VERIFYING", "VERIFIED", "FAILED", "CANCELLED"})
TRANSITIONS = {
    "CAPTURED": {"READY", "WAITING_APPROVAL", "BLOCKED", "CANCELLED"},
    "READY": {"RUNNING", "CANCELLED"},
    "RUNNING": {"VERIFYING", "FAILED"},
    "VERIFYING": {"VERIFIED", "FAILED"},
    "FAILED": {"READY", "CANCELLED"},
    "WAITING_APPROVAL": {"READY", "CANCELLED"},
    "BLOCKED": {"READY", "CANCELLED"},
    "VERIFIED": set(), "CANCELLED": set(),
}


def timestamp():
    return datetime.now(timezone.utc).isoformat()


class CommandCore:
    def __init__(self, db_path, project_ids):
        self.project_ids = frozenset(project_ids)
        self.db = sqlite3.connect(str(db_path), isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS command_tasks (
          id TEXT PRIMARY KEY, project_id TEXT NOT NULL, command TEXT NOT NULL,
          idempotency_key TEXT UNIQUE NOT NULL, state TEXT NOT NULL,
          operation TEXT NOT NULL, result TEXT, checkpoint TEXT,
          created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS command_events (
          id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL,
          event TEXT NOT NULL, evidence TEXT NOT NULL, created_at TEXT NOT NULL,
          FOREIGN KEY(task_id) REFERENCES command_tasks(id));
        CREATE TABLE IF NOT EXISTS security_events (
          id INTEGER PRIMARY KEY AUTOINCREMENT, actor_id TEXT NOT NULL,
          action TEXT NOT NULL, outcome TEXT NOT NULL, created_at TEXT NOT NULL);
        """)

    def audit_security(self, actor_id, action, outcome):
        """Record minimal access evidence, never credentials or request contents."""
        self.db.execute("INSERT INTO security_events(actor_id,action,outcome,created_at) VALUES (?,?,?,?)",
                        (actor_id, action, outcome, timestamp()))

    def close(self):
        self.db.close()

    def _event(self, task_id, event, evidence):
        self.db.execute("INSERT INTO command_events(task_id,event,evidence,created_at) VALUES (?,?,?,?)",
                        (task_id, event, json.dumps(evidence, sort_keys=True), timestamp()))

    def get(self, task_id, actor_projects):
        row = self.db.execute("SELECT * FROM command_tasks WHERE id=?", (task_id,)).fetchone()
        if not row:
            raise KeyError(task_id)
        if row["project_id"] not in actor_projects:
            raise PermissionError("Project access denied")
        return dict(row)

    def submit(self, command, project_id, actor_projects, idempotency_key):
        if project_id not in self.project_ids or project_id not in actor_projects:
            raise PermissionError("Project not registered or accessible")
        if not command.strip() or not idempotency_key:
            raise ValueError("Command and idempotency key required")
        operation = "local_note" if command.strip().lower().startswith("note:") else "external_or_unknown"
        state = "READY" if operation == "local_note" else "WAITING_APPROVAL"
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute("SELECT * FROM command_tasks WHERE idempotency_key=?", (idempotency_key,)).fetchone()
            if old:
                if old["project_id"] != project_id or old["command"] != command:
                    raise ValueError("Conflicting idempotency key")
                task_id = old["id"]
            else:
                task_id = str(uuid.uuid4())
                self.db.execute("INSERT INTO command_tasks VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (task_id, project_id, command, idempotency_key, state, operation, None, None, timestamp(), timestamp()))
                self._event(task_id, "SUBMITTED", {"state": state, "operation": operation})
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return self.get(task_id, actor_projects)

    def transition(self, task_id, actor_projects, target, *, checkpoint=None, evidence=None):
        if target not in STATES:
            raise ValueError("Unknown state")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            current = self.get(task_id, actor_projects)
            if target not in TRANSITIONS[current["state"]]:
                raise ValueError("Invalid state transition")
            if current["state"] == "WAITING_APPROVAL" and target == "READY":
                # A distinct authenticated approval service is not implemented.
                raise PermissionError("Approval service unavailable: fail closed")
            if target == "VERIFIED" and not evidence:
                raise ValueError("Verification evidence required")
            self.db.execute("UPDATE command_tasks SET state=?,checkpoint=COALESCE(?,checkpoint),updated_at=? WHERE id=?",
                            (target, checkpoint, timestamp(), task_id))
            self._event(task_id, "TRANSITION", {"from": current["state"], "to": target, "evidence": evidence})
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return self.get(task_id, actor_projects)

    def execute_note(self, task_id, actor_projects):
        """Atomic deterministic local action; never contacts another service."""
        self.db.execute("BEGIN IMMEDIATE")
        try:
            task = self.get(task_id, actor_projects)
            if task["state"] == "VERIFIED":
                self.db.commit()
                return task
            if task["state"] != "READY" or task["operation"] != "local_note":
                raise PermissionError("Action not eligible for local execution")
            note = task["command"].split(":", 1)[1].strip()
            if not note:
                raise ValueError("Empty note")
            result = json.dumps({"note": note}, sort_keys=True)
            self.db.execute("UPDATE command_tasks SET state='VERIFIED',result=?,checkpoint=?,updated_at=? WHERE id=?",
                            (result, "local_note:committed", timestamp(), task_id))
            self._event(task_id, "LOCAL_NOTE_VERIFIED", {"result": result})
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return self.get(task_id, actor_projects)

    def events(self, task_id, actor_projects):
        self.get(task_id, actor_projects)
        return [dict(row) for row in self.db.execute("SELECT * FROM command_events WHERE task_id=? ORDER BY id", (task_id,))]

    def list_tasks(self, actor_projects, limit=50):
        """Only list tasks in the caller's configured project scope."""
        scoped = sorted(self.project_ids.intersection(actor_projects))
        if not scoped:
            return []
        if not 1 <= limit <= 100:
            raise ValueError("Invalid limit")
        marks = ",".join("?" for _ in scoped)
        rows = self.db.execute(
            f"SELECT * FROM command_tasks WHERE project_id IN ({marks}) ORDER BY created_at DESC LIMIT ?",
            (*scoped, limit))
        return [dict(row) for row in rows]

    def backup_to(self, destination):
        """Create a consistent, non-overwriting SQLite snapshot for manual safekeeping.

        The snapshot is NOT encrypted. Caller must store it in an approved private location.
        """
        destination = Path(destination)
        if destination.exists():
            raise FileExistsError("Backup destination already exists")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(destination)) as snapshot:
            self.db.backup(snapshot)
        with sqlite3.connect(str(destination)) as check:
            valid = check.execute("PRAGMA integrity_check").fetchone()[0]
        if valid != "ok":
            raise RuntimeError("Backup integrity check failed")
        return {"path": str(destination), "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                "integrity": "ok"}
