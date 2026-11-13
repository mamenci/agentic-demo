---
walden_schema_version: v1alpha1
status: approved
approved_at: 2026-11-13T11:02:47Z
last_modified: 2026-11-13T11:02:47Z
approved_fingerprint: sha256:cf550a0d3d8f471529fce8d08faaf11483e991654bce9528ce64c2c0db4ca1cf
source_requirements_approved_at: 2026-11-13T10:57:47Z
source_requirements_fingerprint: sha256:c88cccbdc4fd66ed361bd2e5081d04a14e6854e83f3c263545b7ae49bd5f65d1
---

# Feature Design

## Architecture

Tre moduli, con dipendenze in una sola direzione: `main` → `service` → `utils`.

- `utils.py`: espone `validate_name(name)`, `validate_email(email)` e `validate_age(age)`. Ognuna solleva `ValueError` con il messaggio attuale (`name is required`, `invalid email`, `invalid age`) e non restituisce nulla. Contiene anche `format_user`, invariata.
- `service.py`: `create_user` chiama i validatori nell'ordine nome, email, età prima di salvare. `update_user` controlla prima che l'utente esista (`KeyError`), poi chiama `validate_name` e `validate_age`.
- `main.py`: `run` chiama `service.create_user` e converte il `ValueError` in `error: <messaggio>`. Non contiene condizioni di validazione.

Flusso: `run` → `create_user` → `validate_name` → `validate_email` → `validate_age` → salvataggio → `format_user`. Il primo `ValueError` interrompe il flusso e arriva a `run`.

## Options Considered

Scelta: tre funzioni di validazione separate in `utils.py`, una per campo.

Alternativa considerata: un'unica `validate_user(name, email, age)`. Non è adatta, perché `update_user` non valida l'email e dovrebbe distinguere i casi. Con funzioni per campo, i due flussi compongono ciò che serve e l'ordine dei controlli resta visibile nel codice.

## Simplicity And Elegance Review

Nessuna classe, nessun framework di validazione e nessuna nuova dipendenza: tre funzioni e un modulo già esistente. I messaggi restano nei validatori, quindi `main` non deve conoscerli. Il refactoring non tocca le firme pubbliche di `run`, `create_user` e `update_user`.

## Failure Modes And Tradeoffs

- **Ordine dei controlli:** un cambio d'ordine in `create_user` altererebbe il messaggio con più campi errati. Contenimento: `R1.AC4` e i test parametrizzati lo verificano.
- **Messaggi divergenti:** copiando male un messaggio cambierebbe l'output di `main.run`. Contenimento: `test_behavior.py` confronta le stringhe esatte.
- **Validazione email in `update_user`:** non c'è oggi e non viene aggiunta, perché cambierebbe il comportamento.
- **Compromesso accettato:** `main.run` non intercetta `KeyError` e `service` mantiene lo stato globale `users`. Sono fuori scopo.

## Verification Plan

- `R1`: `test_behavior.py`, invariato (`C2`), eseguito con `python3 -m pytest -q`. Copre tutti i messaggi, l'ordine e i risultati di `run`, `create_user` e `update_user`.
- `R2.AC1`: ricerca nei sorgenti delle condizioni di validazione (`"@" not in`, `age > 120`) fuori da `utils.py`: nessuna corrispondenza.
- `R2.AC2`: `service.py` contiene le chiamate `utils.validate_name`, `utils.validate_email`, `utils.validate_age` e nessuna condizione di validazione inline.
- `R2.AC3`: `main.py` non contiene condizioni di validazione ed `error: ` è costruito dal messaggio dell'eccezione.
- `NFR1`: coperto dalle verifiche di `R2`.

## Requirement Coverage

| Requirement | Covered By |
| --- | --- |
| `R1` | `validate_*` in `utils.py`, flusso `run` → `create_user`/`update_user`; verificato da `test_behavior.py` |
| `R2` | `utils.py` come unico punto delle regole; verificato da ricerca nei sorgenti |
| `NFR1` | Centralizzazione in `utils.py`; verificata con le ricerche di `R2` |
