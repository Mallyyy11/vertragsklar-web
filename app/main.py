# app/main.py
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader
from io import BytesIO

from .analyze import analyze_contract_text
from .middleware_embed import FrameAncestorsMiddleware

app = FastAPI()
app.add_middleware(FrameAncestorsMiddleware)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze-text", response_class=HTMLResponse)
def analyze_text(request: Request, contract_text: str = Form(...)):
    result = analyze_contract_text(contract_text)
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

@app.post("/analyze-pdf", response_class=HTMLResponse)
async def analyze_pdf(request: Request, pdf: UploadFile = File(...)):
    if not pdf.filename.lower().endswith(".pdf"):
        return templates.TemplateResponse("result.html", {"request": request, "result": "Bitte eine PDF-Datei hochladen."})
    try:
        content = await pdf.read()
        reader = PdfReader(BytesIO(content))
        pages_text = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(pages_text).strip()
        if not text:
            return templates.TemplateResponse("result.html", {"request": request, "result": "Kein Text in der PDF gefunden (evtl. Scan)."})
        result = analyze_contract_text(text)
        return templates.TemplateResponse("result.html", {"request": request, "result": result})
    except Exception as e:
        return templates.TemplateResponse("result.html", {"request": request, "result": f"Fehler beim PDF-Lesen: {e}"})
