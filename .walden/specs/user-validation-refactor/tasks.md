---
walden_schema_version: v1alpha1
status: approved
approved_at: 2026-11-13T11:04:17Z
last_modified: 2026-11-13T11:11:12Z
approved_fingerprint: sha256:c17debb641edec2c665bcadc6557652893568215735dd0e2b4d7fb805d1b5d3f
source_design_approved_at: 2026-11-13T11:02:47Z
source_design_fingerprint: sha256:cf550a0d3d8f471529fce8d08faaf11483e991654bce9528ce64c2c0db4ca1cf
---

# Implementation Plan

- [x] 1. Centralizzare le validazioni in `utils.py`
  - [x] 1.1 Aggiungere `validate_name`, `validate_email` e `validate_age` in `utils.py`
    - Requirements: `R2.AC1`
    - Design: Architecture
    - Verification:
      - command: ["python3", "-B", "-c", "import utils\ndef msg(f, v):\n    try:\n        f(v)\n    except ValueError as e:\n        return str(e)\nassert msg(utils.validate_name, '  ') == 'name is required'\nassert msg(utils.validate_name, None) == 'name is required'\nassert msg(utils.validate_email, 'nomail') == 'invalid email'\nassert msg(utils.validate_email, None) == 'invalid email'\nassert [msg(utils.validate_age, a) for a in (None, -1, 121)] == ['invalid age'] * 3\nassert all(msg(utils.validate_age, a) is None for a in (0, 120))\nassert msg(utils.validate_name, 'A') is None and msg(utils.validate_email, 'a@b.it') is None\nprint('validators ok')"]
        expect_output: "validators ok"
  - [x] 1.2 Usare i validatori in `service.create_user` e `service.update_user`
    - Requirements: `R1.AC6`, `R1.AC7`, `R1.AC8`, `R2.AC2`
    - Design: Architecture
    - Verification:
      - command: ["sh", "-c", "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider test_behavior.py"]
        expect_output: "10 passed"
        covers: ["R1.AC6", "R1.AC7", "R1.AC8"]
      - command: ["sh", "-c", "grep -q 'utils.validate_name' service.py && grep -q 'utils.validate_email' service.py && grep -q 'utils.validate_age' service.py && ! grep -nE '\"@\" not in|> 120|strip\\(\\) == \"\"' service.py && echo service-ok"]
        expect_output: "service-ok"
        covers: ["R2.AC2"]
  - [x] 1.3 Rimuovere i controlli duplicati da `main.run`
    - Requirements: `R1.AC1`, `R1.AC2`, `R1.AC3`, `R1.AC4`, `R1.AC5`, `R2.AC3`
    - Design: Architecture
    - Verification:
      - command: ["sh", "-c", "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider test_behavior.py"]
        expect_output: "10 passed"
        covers: ["R1.AC1", "R1.AC2", "R1.AC3", "R1.AC4", "R1.AC5"]
      - command: ["sh", "-c", "! grep -nE '\"@\" not in|> 120|strip\\(\\) == \"\"' main.py && grep -q 'error: ' main.py && echo main-ok"]
        expect_output: "main-ok"
        covers: ["R2.AC3"]
  - [x] 1.4 Verificare la coerenza tra i file
    - Requirements: `R2.AC1`
    - Design: Verification Plan
    - Verification:
      - command: ["sh", "-c", "grep -q '@' utils.py && ! grep -nE '\"@\" not in|> 120|strip\\(\\) == \"\"' main.py service.py && echo central-ok"]
        expect_output: "central-ok"
        covers: ["R2.AC1"]
      - command: ["sh", "-c", "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider test_behavior.py"]
        expect_output: "10 passed"
