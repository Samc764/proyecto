from datetime import datetime

from fastapi import FastAPI, Form, Request  # type: ignore[import]
from fastapi.responses import HTMLResponse, RedirectResponse  # type: ignore[import]
from fastapi.staticfiles import StaticFiles  # type: ignore[import]
from fastapi.templating import Jinja2Templates  # type: ignore[import]

app = FastAPI()

# Archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Base de datos simulada
mensajes_db = []


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        "formulario.html",
        {
            "request": request,
            "ano_actual": datetime.now().year,
        },
    )


@app.get("/muro", response_class=HTMLResponse)
async def muro(request: Request):
    return templates.TemplateResponse(
        "muro.html",
        {
            "request": request,
            "mensajes": mensajes_db,
            "ano_actual": datetime.now().year,
        },
    )


@app.post("/enviar")
async def enviar_mensaje(
    autor: str = Form(...),
    mensaje: str = Form(...),
    color: str = Form(...),
):
    mensajes_db.append(
        {
            "autor": autor.strip(),
            "mensaje": mensaje.strip(),
            "color": color,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
    )

    return RedirectResponse(url="/muro", status_code=303)


@app.post("/eliminar/{indice}")
async def eliminar_mensaje(indice: int):
    if 0 <= indice < len(mensajes_db):
        mensajes_db.pop(indice)

    return RedirectResponse(url="/muro", status_code=303)