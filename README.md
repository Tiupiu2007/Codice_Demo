# Demo

Piccolo progetto Python con due funzioni: controllare un file CSV e provare la codifica Base64.

## Avvio su Windows

Dalla cartella del progetto, nel terminale:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Apri http://127.0.0.1:5000 nel browser.

Per provare il controllo CSV puoi usare `esempio.csv`.

## Decodificare il messaggio

Il file `decodifica.py` non ha un'interfaccia: stampa direttamente nel terminale il testo decodificato.

```powershell
py decodifica.py
```

Il messaggio è prima codificato in Base64 e poi trasformato con ROT13. Non è crittografia sicura: è solo una codifica semplice.
