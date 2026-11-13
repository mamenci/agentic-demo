---
walden_schema_version: v1alpha1
status: approved
approved_at: 2026-11-13T10:57:47Z
last_modified: 2026-11-13T10:57:47Z
approved_fingerprint: sha256:c88cccbdc4fd66ed361bd2e5081d04a14e6854e83f3c263545b7ae49bd5f65d1
---

# Requirements Document

## Introduction

Il progetto crea e aggiorna utenti validando nome, email ed età. Le regole di validazione sono oggi duplicate in `main.py` e `service.py`. Questa feature centralizza le validazioni in `utils.py` senza modificare il comportamento osservabile: messaggi di errore, ordine dei controlli e risultati restano invariati.

## Requirements

### R1 Comportamento di validazione preservato

**User Story:** As a developer, I want the user validation behavior to stay identical after the refactoring, so that no caller observes a change.

#### Acceptance Criteria

1. `R1.AC1` WHEN `main.run` receives a missing or blank name, the system SHALL return `error: name is required`.
   - Acceptance check: `main.run("", "m@x.it", 1)` and `main.run(None, "m@x.it", 1)` return that exact string.
2. `R1.AC2` WHEN `main.run` receives a name that is valid and an email that is missing or has no `@`, the system SHALL return `error: invalid email`.
   - Acceptance check: `main.run("A", "nomail", 1)` and `main.run("A", None, 1)` return that exact string.
3. `R1.AC3` WHEN `main.run` receives a valid name and email and an age that is missing, below 0 or above 120, the system SHALL return `error: invalid age`.
   - Acceptance check: ages `None`, `-1` and `121` return that exact string, while ages `0` and `120` are accepted.
4. `R1.AC4` WHEN `main.run` receives several invalid fields, the system SHALL report the first invalid field in the order name, email, age.
   - Acceptance check: `main.run(None, None, None)` returns `error: name is required`.
5. `R1.AC5` WHEN `main.run` receives valid data, the system SHALL return the user formatted as `<name> <<email>> (<age>)` with the name trimmed.
   - Acceptance check: `main.run(" Mario ", "m@x.it", 42)` returns `Mario <m@x.it> (42)`.
6. `R1.AC6` WHEN `service.create_user` receives invalid data, the system SHALL raise `ValueError` with the same messages and the same order as in `R1.AC1` to `R1.AC4`.
   - Acceptance check: calling it with a bad email, blank name and out-of-range age raises `ValueError` with `invalid email`, `name is required` and `invalid age`.
7. `R1.AC7` WHEN `service.update_user` receives an email that is not registered, the system SHALL raise `KeyError` with `user not found`.
   - Acceptance check: `service.update_user("zz@b.it", "B", 5)` raises `KeyError`.
8. `R1.AC8` WHEN `service.update_user` receives a blank name or an age out of range for a registered user, the system SHALL raise `ValueError` with `name is required` or `invalid age`.
   - Acceptance check: updating a registered user with `""` as name, or `-3` as age, raises the matching `ValueError`.

### R2 Validazioni centralizzate

**User Story:** As a developer, I want each validation rule defined in one place, so that changing a rule requires a single edit.

#### Acceptance Criteria

1. `R2.AC1` The system SHALL define the name, email and age validation rules only in `utils.py`.
   - Acceptance check: no source file other than `utils.py` contains the checks `"@" not in`, `.strip() == ""` on a name, or the age bounds `0` and `120`.
2. `R2.AC2` The system SHALL use the `utils.py` validators in both `service.create_user` and `service.update_user`.
   - Acceptance check: `service.py` calls the `utils` validators and holds no inline validation conditions.
3. `R2.AC3` The system SHALL keep `main.run` free of validation logic, delegating errors to `service` and reporting them as `error: <message>`.
   - Acceptance check: `main.py` contains no validation conditions and `main.run` returns the message of the `ValueError` raised by `service`.

## Non-Functional Requirements

- `NFR1` Maintainability: a change to a validation rule touches one file. Covered by `R2.AC1` to `R2.AC3`.

## Constraints And Dependencies

- `C1` Python 3.14 and pytest 9, no external dependencies.
- `C2` `test_behavior.py` is the behavior contract and is not modified by the refactoring.

## Out Of Scope

- Handling `KeyError` in `main.run`.
- Removing the global `users` state in `service.py`.
- Adding new validation rules or changing messages.
