# Piano di refactoring

## Obiettivo
Migliorare la struttura del progetto ed eliminare la duplicazione delle validazioni,
senza cambiare il comportamento osservabile.

## Passi
1. Aggiungere in `utils.py` `validate_name`, `validate_email` e `validate_age`, che sollevano
   `ValueError` con gli stessi messaggi di oggi. Nessun altro file cambia.
   Verifica: `python3 -m pytest -q`.
2. Usare i validatori in `service.create_user` e `service.update_user`.
   Verifica: `python3 -m pytest -q`.
3. Rimuovere i controlli duplicati da `main.run`, che si affida a `service` e al suo `except ValueError`.
   Verifica: `python3 -m pytest -q` e `python3 main.py`.
4. Verificare la coerenza tra i file: nessun controllo ripetuto, messaggi e ordine degli errori invariati.

## Rischio
`main.run` controlla nell'ordine nome, email, età. `service.create_user` deve mantenere lo stesso ordine.

## Stato
Approvato dall'utente ed eseguito (passaggi 6-11). Test: `python3 -m pytest -q`.
