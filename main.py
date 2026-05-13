from datetime import datetime

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Base de datos simulada (una lista en memoria)
mensajes_db = []


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="formulario.html",
        context={"ano_actual": datetime.now().year},
    )


@app.post("/enviar")
async def enviar_mensaje(autor: str = Form(...), mensaje: str = Form(...)):
    mensajes_db.append({"autor": autor, "mensaje": mensaje})
    return RedirectResponse(url="/muro", status_code=303)


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

@app.post("/eliminar/{indice}")
async def eliminar_mensaje(indice: int):
    if 0 <= indice < len(mensajes_db):
        mensajes_db.pop(indice)
    return RedirectResponse(url="/muro", status_code=303)

@app.post("/enviar")
async def enviar_mensaje(
    autor: str = Form(...),
    mensaje: str = Form(...),
    color: str = Form(...),       # NUEVO
):
    mensajes_db.append({
        "autor": autor,
        "mensaje": mensaje,
        "color": color,            # NUEVO
    })
    return RedirectResponse(url="/muro", status_code=303)