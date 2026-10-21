# DataPilot

Questa è una piccola demo in Python e Flask.

Serve a provare due cose:
- controllare un file CSV e contare righe duplicate e campi vuoti;
- codificare e decodificare un testo in Base64.

## Come avviarla su Windows

Apri il terminale nella cartella del progetto e scrivi:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Poi apri http://127.0.0.1:5000 nel browser.

Per provare la parte CSV puoi usare il file `esempio.csv`.

È una demo semplice, pensata per fare prove con dati di esempio. Base64 non è un sistema di cifratura e non rende segreti i dati.
