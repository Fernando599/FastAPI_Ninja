from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi_zero.schemas import Message

app = FastAPI(
    title='API To-do List',
    description='API projeto To-do List para aprendizado.',
)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá FastAPI'}


templates = Jinja2Templates(directory='templates')


@app.get(
    '/exercicio',
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def exercicio(request: Request):
    return templates.TemplateResponse('exercicio/index.html', {'request': request})
