from flask import Flask, request, render_template_string, make_response
import csv
import io

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DataPilot - Demo</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 850px; margin: 40px auto; padding: 0 16px; color: #222; }
    section { border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin: 18px 0; }
    button { padding: 10px 14px; cursor: pointer; }
    table { border-collapse: collapse; width: 100%; margin-top: 14px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f2f2f2; }
    .stats { display: flex; gap: 18px; flex-wrap: wrap; }
  </style>
</head>
<body>
  <h1>DataPilot</h1>
  <p>Demo semplice per controllare la qualità di un file CSV.</p>
  <section>
    <h2>1. Carica i dati</h2>
    <p>Il file deve essere in formato CSV, con la prima riga contenente i nomi delle colonne.</p>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept=".csv" required>
      <button type="submit">Analizza CSV</button>
    </form>
  </section>
  {% if report %}
  <section>
    <h2>2. Risultato</h2>
    <div class="stats">
      <p><b>Righe:</b> {{ report.rows }}</p>
      <p><b>Righe duplicate:</b> {{ report.duplicates }}</p>
      <p><b>Campi vuoti:</b> {{ report.empty }}</p>
    </div>
    <p>La demo identifica i problemi, ma non modifica il file originale.</p>
    <form method="post" action="/download">
      <input type="hidden" name="data" value="{{ csv_data }}">
      <button type="submit">Scarica CSV senza duplicati</button>
    </form>
    <h3>Anteprima</h3>
    <table>
      <thead><tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}</tr></thead>
      <tbody>
      {% for row in preview %}
        <tr>{% for value in row %}<td>{{ value }}</td>{% endfor %}</tr>
      {% endfor %}
      </tbody>
    </table>
  </section>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    columns = []
    preview = []
    csv_data = ""

    if request.method == "POST":
        uploaded = request.files.get("file")
        if not uploaded or not uploaded.filename:
            return "Seleziona un file CSV.", 400

        try:
            content = uploaded.stream.read().decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(content))
            columns = reader.fieldnames or []
            rows = list(reader)

            if not columns:
                return "Il CSV deve avere una riga iniziale con i nomi delle colonne.", 400

            seen = set()
            clean_rows = []
            duplicates = 0
            empty = 0

            for row in rows:
                empty += sum(1 for value in row.values() if value is None or not value.strip())
                key = tuple((row.get(col) or "").strip() for col in columns)
                if key in seen:
                    duplicates += 1
                else:
                    seen.add(key)
                    clean_rows.append({col: (row.get(col) or "").strip() for col in columns})

            report = {
                "rows": len(rows),
                "duplicates": duplicates,
                "empty": empty,
            }
            preview = [[row.get(col, "") for col in columns] for row in rows[:10]]

            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=columns)
            writer.writeheader()
            writer.writerows(clean_rows)
            csv_data = output.getvalue()

        except (UnicodeDecodeError, csv.Error):
            return "Non riesco a leggere il file. Prova a salvarlo come CSV UTF-8.", 400

    return render_template_string(
        PAGE, report=report, columns=columns, preview=preview, csv_data=csv_data
    )

@app.route("/download", methods=["POST"])
def download():
    data = request.form.get("data", "")
    response = make_response(data)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=dati_puliti.csv"
    return response

if __name__ == "__main__":
    app.run(debug=True)
