# ============================================================

# TOS PROFESSIONAL EDITION

# PROJECT SESSION

# ============================================================

## Project Information

Project Name:
Trading Operating System (TOS) Professional Edition

Repository:
https://github.com/rajeshsingh437/tos-professional-edition

Technology Stack:

- Python
- PySide6
- SQLite (Planned)
- pandas
- pyqtgraph

Branch:
main

---

# Current Status

Current Build:
0.2.002

Current Phase:
Application Framework

Application Status:
✅ Running Successfully

Current Architecture:
Python Desktop Application

---

# Completed Files

app/
✔ application.py
✔ main.py

ui/
✔ dashboard.py
✔ header.py
✔ main_window.py
✔ sidebar.py
✔ theme.py

---

# Pending Files

□ PROJECT_MASTER.md
□ WORK_LOG.md
□ start.ps1
□ run.ps1
□ build.ps1
□ commit.ps1
□ clean.ps1

---

# Current Decisions

✔ Python Desktop only

✔ SENTRY is reference-only

✔ One complete file per response

✔ Replace entire file only

✔ Verify after every file

✔ Git commit only after stable build

✔ Branch:
main

✔ Modular architecture

---

# Current Folder Structure

TOS Professional Edition/

app/

ui/

docs/

---

# Next Build Target

Build 0.2.002

Objectives:

1. Create project documentation
2. Build application framework
3. Implement QStackedWidget navigation
4. Create page architecture
5. Create reusable UI components

---

# Next File

PROJECT_MASTER.md

---

# Session Start Checklist

□ Open PROJECT_SESSION.md

□ Verify project folder

□ Activate .venv

□ Run application

□ Continue from "Next File"

---

# Session End Checklist

□ Application runs

□ Git Commit

□ Git Push

□ Update CHANGELOG.md

□ Update PROJECT_SESSION.md

---

# Notes

Old React/Vite project still exists.

Repository cleanup will be done after Build 0.2.002.

---

Last Stable Build:

Build 0.2.001

Initial PySide6 Desktop Application Shell

## Latest Development Progress — 2026-08-01

- Established the broker architecture around the broker interface and a
  broker-specific Flattrade adapter.
- Renamed the Flattrade authentication component to
  `AuthenticationManager` and retained session-backed authentication state.
- Integrated `OAuthClient` for Flattrade OAuth payload construction and
  `RestClient` for broker API access in the adapter.
- Debugged `src/brokers/flattrade/adapter.py`: its constructor indentation
  was invalid and duplicate initialization had been placed after the context
  manager return statement.
- Replaced `adapter.py` as one complete file; do not apply incremental
  patches to large source files going forward. Use complete-file
  replacements and verify each replacement by compiling it.
