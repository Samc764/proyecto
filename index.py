from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

mensajes_db = []


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="formulario.html",
        context={
            "ano_actual": datetime.now().year,
        },
    )


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


@app.post("/enviar")
async def enviar_mensaje(
    autor: str = Form(...),
    mensaje: str = Form(...),
    color: str = Form(...),
):
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


@app.post("/eliminar/{indice}")
async def eliminar_mensaje(indice: int):
    if 0 <= indice < len(mensajes_db):
        mensajes_db.pop(indice)

    return RedirectResponse(url="/muro", status_code=303)