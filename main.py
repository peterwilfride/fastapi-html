from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from item_dao import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

dao = ItemDAO()

sequence = 1

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html"
    )

@app.get("/items/", response_class=HTMLResponse)
async def read_items(request: Request):
    items = dao.find_all()
    has_items = len(items) > 0
    return templates.TemplateResponse(
        request=request, name="items.html", context={'items': items, 'has_items': has_items}
    )

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    item = dao.find_one(int(id))
    if item is None:
        return templates.TemplateResponse(
            request=request, name="notfound.html", status_code=404
        )
    return templates.TemplateResponse(
        request=request, name="item.html", context={"item": item}
    )

@app.get("/cadastro")
async def exibir_formulario(request: Request):
    return templates.TemplateResponse(
        request=request, name="item_insert_form.html"
    )

@app.get("/items/{id}/edit")
async def exibir_formulario(request: Request, id: str):
    item = dao.find_one(int(id))
    return templates.TemplateResponse(
        request=request, name="item_edit_form.html", context={"item": item}
    )

@app.get("/items/{id}/remove")
async def exibir_formulario(request: Request, id: str):
    dao.remove(int(id))
    return RedirectResponse(url="/items/", status_code=303) 

@app.post("/processar-formulario", response_class=HTMLResponse)
async def processar_formulario(request: Request, nome: str = Form(...), price: str = Form(...)):
    global sequence
    item = Item(id=sequence, nome=nome, price=float(price))
    sequence += 1
    dao.add(item)
    return RedirectResponse(url="/items/", status_code=303)

@app.post("/processar-formulario-edit", response_class=HTMLResponse)
async def processar_formulario_edit(request: Request, id: str = Form(...), nome: str = Form(...), price: str = Form(...)):
    item = Item(id=int(id), nome=nome, price=float(price))
    dao.edit(int(id), item)
    return RedirectResponse(url="/items/", status_code=303)  