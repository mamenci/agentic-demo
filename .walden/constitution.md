# Project Constitution

This file captures stable project-wide context that applies across all features. It is optional and does not participate in the approval workflow.

## Project Summary

Piccolo progetto Python dimostrativo (hands-on Agentic Development) che crea e aggiorna utenti con validazione di nome, email ed età.

## Tech Stack

Python 3.14, pytest 9, nessuna dipendenza esterna.

## Conventions

[Naming, file layout, code style, branching strategy, and commit message format]

## Sanity Checks

```bash
python3 -m pytest -q
```

## Key Files

`main.py` (entry point), `service.py` (creazione/aggiornamento utenti), `utils.py` (funzioni di supporto), `test_behavior.py` (contratto di comportamento).

## Hard Rules

Il refactoring non deve cambiare il comportamento osservabile: messaggi di errore e ordine dei controlli restano invariati.
