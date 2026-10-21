import base64
import csv
import io

from flask import Flask, make_response, render_template_string, request

app = Flask(__name__)

PAGINA = """
<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DataPilot</title>
    <style>
        body {
            max-width: 850px;
            margin: 35px auto;
            padding: 0 16px;
            font-family: Arial, sans-serif;
            color: #222;
        }
        section {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 18px;
            margin: 20px 0;
        }
        input, button, textarea { margin: 6px 0; }
        textarea { box-sizing: border-box; width: 100%; padding: 10px; }
        button { padding: 9px 12px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; margin-top: 12px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f2f2f2; }
        .errore { color: #b00020; }
    </style>
</head>
<body>
    <h1>DataPilot</h1>
    <p>Una piccola demo per controllare un CSV e lavorare con Base64.</p>

    <section>
        <h2>Controlla un file CSV</h2>
        <p>Carica un file CSV con i nomi delle colonne nella prima riga.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv" required>
            <button type="submit">Analizza file</button>
        </form>
    </section>

    {% if errore %}
        <p class="errore">{{ errore }}</p>
    {% endif %}

    {% if report %}
    <section>
        <h2>Risultato</h2>
        <p>Righe nel file: <b>{{ report.righe }}</b></p>
        <p>Righe duplicate: <b>{{ report.duplicate }}</b></p>
        <p>Campi vuoti: <b>{{ report.vuoti }}</b></p>
        <p>Qui sotto trovi un'anteprima delle prime 10 righe.</p>

        <table>
            <thead>
                <tr>{% for colonna in colonne %}<th>{{ colonna }}</th>{% endfor %}</tr>
            </thead>
            <tbody>
                {% for riga in anteprima %}
                <tr>{% for valore in riga %}<td>{{ valore }}</td>{% endfor %}</tr>
                {% endfor %}
            </tbody>
        </table>

        <form method="post" action="/scarica">
            <input type="hidden" name="csv" value="{{ csv_pulito }}">
            <button type="submit">Scarica il CSV senza duplicati</button>
        </form>
    </section>
    {% endif %}

    <section>
        <h2>Convertitore Base64</h2>
        <p>Scrivi un testo e scegli se codificarlo o provare a decodificarlo.</p>
        <form method="post" action="/base64">
            <textarea name="testo" rows="4" placeholder="Scrivi qui il testo...">{{ testo }}</textarea>
            <br>
            <button name="azione" value="codifica" type="submit">Codifica</button>
            <button name="azione" value="decodifica" type="submit">Decodifica</button>
        </form>
        {% if risultato is not none %}
            <label for="risultato"><b>Risultato</b></label>
            <textarea id="risultato" rows="4" readonly>{{ risultato }}</textarea>
        {% endif %}
    </section>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    colonne = []
    anteprima = []
    csv_pulito = ""
    errore = None

    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename:
            try:
                testo_csv = file.read().decode("utf-8-sig")
                lettore = csv.DictReader(io.StringIO(testo_csv))
                colonne = lettore.fieldnames or []
                righe = list(lettore)

                if not colonne:
                    raise ValueError("Il CSV deve contenere i nomi delle colonne.")

                viste = set()
                righe_pulite = []
                duplicate = 0
                vuoti = 0

                for riga in righe:
                    vuoti += sum(
                        1 for valore in riga.values()
                        if valore is None or not valore.strip()
                    )

                    chiave = tuple((riga.get(colonna) or "").strip() for colonna in colonne)

                    if chiave in viste:
                        duplicate += 1
                        continue

                    viste.add(chiave)
                    righe_pulite.append({
                        colonna: (riga.get(colonna) or "").strip()
                        for colonna in colonne
                    })

                report = {
                    "righe": len(righe),
                    "duplicate": duplicate,
                    "vuoti": vuoti,
                }
                anteprima = [
                    [riga.get(colonna, "") for colonna in colonne]
                    for riga in righe[:10]
                ]

                output = io.StringIO()
                scrittore = csv.DictWriter(output, fieldnames=colonne)
                scrittore.writeheader()
                scrittore.writerows(righe_pulite)
                csv_pulito = output.getvalue()

            except (UnicodeDecodeError, csv.Error, ValueError) as errore_csv:
                errore = str(errore_csv) or "Non riesco a leggere il file. Prova un CSV UTF-8."

    return render_template_string(
        PAGINA,
        report=report,
        colonne=colonne,
        anteprima=anteprima,
        csv_pulito=csv_pulito,
        errore=errore,
        testo="",
        risultato=None,
    )


@app.route("/scarica", methods=["POST"])
def scarica():
    contenuto = request.form.get("csv", "")
    risposta = make_response(contenuto)
    risposta.headers["Content-Type"] = "text/csv; charset=utf-8"
    risposta.headers["Content-Disposition"] = "attachment; filename=csv_pulito.csv"
    return risposta


@app.route("/base64", methods=["POST"])
def converti_base64():
    testo = request.form.get("testo", "")
    azione = request.form.get("azione")
    risultato = ""

    try:
        if azione == "codifica":
            risultato = base64.b64encode(testo.encode("utf-8")).decode("ascii")
        else:
            risultato = base64.b64decode(testo, validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        risultato = "Testo Base64 non valido oppure non codificato in UTF-8."

    return render_template_string(
        PAGINA,
        report=None,
        colonne=[],
        anteprima=[],
        csv_pulito="",
        errore=None,
        testo=testo,
        risultato=risultato,
    )


if __name__ == "__main__":
    app.run()
