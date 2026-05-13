from datetime import datetime
import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Archivos estáticos y plantillas
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Base de datos simulada (mensajes en memoria)
mensajes_db = []


# Página principal con formulario
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="formulario.html",
        context={
            "ano_actual": datetime.now().year,
        },
    )


# Página del muro donde se muestran los mensajes
@app.get("/muro", response_class=HTMLResponse)
async def muro(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="muro.html",
        context={
            "mensajes": mensajes_db,
            "ano_actual": datetime.now().year,
        },
    )


# Enviar mensaje desde el formulario
@app.post("/enviar")
async def enviar_mensaje(
    autor: str = Form(...),
    mensaje: str = Form(...),
    color: str = Form(...),
):
    # Evita mensajes vacíos
    if autor.strip() and mensaje.strip():
        mensajes_db.append(
            {
                "autor": autor.strip(),
                "mensaje": mensaje.strip(),
                "color": color,
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
        )

    return RedirectResponse(url="/muro", status_code=303)


# Eliminar mensaje por índice
@app.post("/eliminar/{indice}")
async def eliminar_mensaje(indice: int):
    if 0 <= indice < len(mensajes_db):
        mensajes_db.pop(indice)

    return RedirectResponse(url="/muro", status_code=303)