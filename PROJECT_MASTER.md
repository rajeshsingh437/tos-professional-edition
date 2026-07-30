# ============================================================
# TOS PROFESSIONAL EDITION
# PROJECT MASTER
# ============================================================

# Vision

Trading Operating System (TOS) Professional Edition is a professional
desktop application designed to become a complete trading workspace for
planning, execution, journaling, analytics and risk management.

The objective is to build software that is robust, modular, visually
professional and capable of growing for many years without major
architectural changes.

---

# Technology Stack

Language
- Python

Desktop Framework
- PySide6

Database
- SQLite

Data Analysis
- pandas

Charts
- pyqtgraph

Version Control
- Git + GitHub

---

# Architecture Principles

1. Modular

Every major feature must exist as an independent module.

Examples:

- Dashboard
- Trading Journal
- Analytics
- Portfolio
- Risk Manager
- Reports
- Settings

No module should tightly depend on another.

---

2. Reusable Components

UI components should be reusable.

Examples:

- Cards
- Headers
- Metric Tiles
- Tables
- Dialogs
- Charts
- Toolbars

Avoid duplicate code.

---

3. Separation of Responsibilities

Application

↓

Navigation

↓

Pages

↓

Widgets

↓

Business Logic

↓

Database

Each layer should have a single responsibility.

---

4. Desktop First

The application is designed specifically for desktop users.

Requirements include:

- Large monitors
- Multi-monitor support (future)
- Keyboard shortcuts
- High performance
- Offline capability

---

# Project Structure

TOS Professional Edition/

app/
Application bootstrap

ui/
User interface

core/
Business logic

models/
Application models

database/
SQLite

resources/
Icons
Themes
Fonts

docs/
Documentation

---

# Coding Standards

- One complete file per response.
- Never partial snippets.
- Replace entire files.
- Keep functions focused.
- Prefer readability over clever code.
- Use type hints where appropriate.
- Document public classes.

---

# Git Workflow

Branch

main

Commit only after a stable build.

Commit format:

Build X.Y.ZZZ - Description

Examples:

Build 0.2.001 - Initial application shell

Build 0.2.002 - Navigation framework

---

# Development Workflow

Session Start

1.
Open PROJECT_SESSION.md

2.
Run application

3.
Continue from Next File

Session End

1.
Verify application

2.
Commit

3.
Push

4.
Update documentation

---

# User Interface Goals

Professional appearance

Dark theme

Consistent spacing

Readable typography

Minimal visual clutter

Fast navigation

Responsive resizing

---

# Long-Term Roadmap

Foundation

↓

Navigation

↓

Dashboard

↓

Trading Journal

↓

Risk Manager

↓

Portfolio

↓

Analytics

↓

Reports

↓

AI Assistant

↓

Version 1.0

---

# Project Rules

✔ Python Desktop only

✔ One complete file per message

✔ Stable builds only

✔ Documentation updated every build

✔ Keep architecture clean

✔ No technical debt whenever reasonably avoidable

---

This document is the permanent architectural reference for the project.