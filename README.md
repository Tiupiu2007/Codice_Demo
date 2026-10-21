# DataPilot — demo

Piccola demo Python/Flask per mostrare un semplice controllo della qualità dei dati CSV.

## Funzioni
- Caricamento di un CSV.
- Conteggio righe, righe duplicate e campi vuoti.
- Anteprima dei primi 10 record.
- Download di un CSV senza righe duplicate.

## Avvio su Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Apri poi http://127.0.0.1:5000 nel browser.

Il progetto è una demo didattica: usa solo file di prova e non caricare dati personali o aziendali riservati.
