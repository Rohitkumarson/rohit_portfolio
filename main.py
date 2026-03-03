from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from weasyprint import HTML
import os
import secrets

# -----------------------
# App Configuration
# -----------------------
app = FastAPI(
    docs_url=None,        # Disable default Swagger
    redoc_url=None,
    openapi_url="/openapi.json"
)

# -----------------------
# Paths
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# -----------------------
# Swagger Protection
# -----------------------
security = HTTPBasic()

def docs_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, "rohitkumar@9211#")
    correct_pass = secrets.compare_digest(credentials.password, "rohit@777775577777")
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/docs", dependencies=[Depends(docs_auth)], include_in_schema=False)
def protected_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Protected API Docs"
    )

# -----------------------
# HTML Pages
# -----------------------
@app.get("/", response_class=HTMLResponse)
def home_page():
    with open(os.path.join(TEMPLATE_DIR, "index.html"), encoding="utf-8") as f:
        return f.read()

@app.get("/ai-pipeline", response_class=HTMLResponse)
def ai_pipeline_page():
    with open(os.path.join(TEMPLATE_DIR, "chatbot_pipeline.html"), encoding="utf-8") as f:
        return f.read()

@app.get("/resume", response_class=HTMLResponse)
def resume_page():
    with open(os.path.join(TEMPLATE_DIR, "resume.html"), encoding="utf-8") as f:
        return f.read()

# -----------------------
# PDF Download
# -----------------------
@app.get("/download-pdf")
def download_pdf():
    html_path = os.path.join(TEMPLATE_DIR, "resume.html")
    pdf_bytes = HTML(filename=html_path).write_pdf()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Rohit_Kumar_AI_ML_Engineer.pdf"
        }
    )

from fastapi.responses import FileResponse 

@app.get("/sitemap.xml", include_in_schema=False)
def sitemap():
    return FileResponse(
        path="sitemap.xml",
        media_type="application/xml"
    )

@app.get("/robots.txt", include_in_schema=False)
def robots():
    return FileResponse(
        path="robots.txt",
        media_type="text/plain"
    )

