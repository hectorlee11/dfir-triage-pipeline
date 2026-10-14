# Live Local Host IR & Forensic Triage Pipeline

A lightweight, automated endpoint incident response and forensic triage pipeline built with PowerShell, Eric Zimmerman's CLI Tools, and Python.

## Architecture & Workflow

- **1. Administrator PowerShell:** Parses raw Prefetch and JumpList artifacts from protected system directories.
- **2. Python Normalization Engine:** Ingests CSVs, handles large field limits, and sorts events chronologically.
- **3. Master Incident Timeline:** Outputs a clean, human-readable markdown report (TIMELINE.md).

## Features
- **Privileged Collection:** Targets locked Windows system directories requiring elevation.
- **Standardized Parsing:** Uses PECmd and JLECmd for execution and file-access artifacts.
- **Python Normalization:** Merges disparate CSV schemas into a reverse-chronological master timeline.

## Quick Start Guide
1. Open PowerShell as Administrator and navigate to C:\DFIR_Triage.
2. Run your artifact parsers.
3. Execute python generate_timeline.py to build your master timeline.