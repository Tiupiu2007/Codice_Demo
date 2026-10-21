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
    <title>Demo</title>
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
    <h1>Demo</h1>
    <p>Una piccola demo per controllare la qualità di un file CSV.</p>

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
    )


@app.route("/scarica", methods=["POST"])
def scarica():
    contenuto = request.form.get("csv", "")
    risposta = make_response(contenuto)
    risposta.headers["Content-Type"] = "text/csv; charset=utf-8"
    risposta.headers["Content-Disposition"] = "attachment; filename=csv_pulito.csv"
    return risposta


if __name__ == "__main__":
    app.run()
