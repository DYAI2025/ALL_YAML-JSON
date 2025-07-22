from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import yaml, datetime

app = FastAPI()

# ➡️ MongoDB-Zugangsdaten HIER eintragen (ersetze die Platzhalter!):
client = MongoClient("mongodb+srv://<USER>:<PASS>@<CLUSTER>.mongodb.net/mydb?retryWrites=true&w=majority")
db = client["mydb"]["markerdocs"]

def valid_marker(m):
    return all(x in m for x in ("id", "description", "examples"))

@app.get("/", response_class=HTMLResponse)
def upload_form():
    return """
    <html>
    <body>
    <h2>Marker Datei Upload</h2>
    <form action="/upload/" enctype="multipart/form-data" method="post">
      <input name="file" type="file">
      <input type="submit">
    </form>
    </body>
    </html>
    """

@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    data = yaml.safe_load(content)
    items = data if isinstance(data, list) else [data]
    imported, failed = [], []
    for m in items:
        if valid_marker(m):
            m["_audit"] = {"ts": datetime.datetime.utcnow().isoformat(), "src": file.filename}
            db.replace_one({"id": m["id"]}, m, upsert=True)
            imported.append(m["id"])
        else:
            failed.append(m.get("id", "?"))
    return f"<b>Importiert:</b> {imported}<br><b>Fehlerhaft:</b> {failed}"