# Email Triage Helper

A simple, beginner‑friendly Python tool that helps you triage text items (emails, notes, job leads, etc.) and manage a small library of copy‑and‑paste snippets.

It has two main modes:

1. **Triage mode** – reads a text file of items and classifies each into categories (e.g. URGENT, MONEY, JOB_LEAD, PERSONAL, SPAM).  
2. **Snippet mode** – lets you search a JSON file of reusable text snippets and prints one so you can copy‑paste it into emails, forms, or chats.

This project is designed to show a practical workflow: reading files, simple rule‑based logic, and text output you can actually use.

---

## Requirements

- Python 3.x installed  
- You can run Python from PowerShell or File Explorer (already tested)

No external libraries are required.

---

## Files

- `triage.py` – main script with `triage` and `snippet` modes  
- `sample_items.txt` – example input file for triage mode  
- `snippets.json` – example snippet library for snippet mode  
- `README.md` – this documentation

---

## Usage

Open PowerShell in this folder and run:

### 1. Triage mode

```bash
python triage.py triage sample_items.txt
```

This will:

- Read `sample_items.txt`
- Classify each item into a category
- Write:
  - `triage_results.json` – structured results
  - `triage_summary.txt` – human‑readable summary

### 2. Snippet mode

```bash
python triage.py snippet "technical summary"
```

This will:

- Search `snippets.json` for snippets whose title or tags match the search text  
- Print the best match to the console so you can copy‑paste it.

---

## Editing the rules and snippets

- To change how items are classified, edit the keywords in `triage.py` under `CATEGORY_RULES`.  
- To add or edit snippets, open `snippets.json` and follow the existing structure.

This is intentionally simple Python, focused on readability and troubleshooting rather than fancy libraries.
