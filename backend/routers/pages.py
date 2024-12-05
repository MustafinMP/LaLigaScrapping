from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

router = APIRouter(
    tags=['pages']
)

templates = Jinja2Templates(directory='../frontend/templates')


@router.get('/')
def home():
    return RedirectResponse("/matches")


@router.get('/matches')
def matches(request: Request):
    return templates.TemplateResponse('matches.html', {'request': request})


@router.get('/players')
def players(request: Request):
    return templates.TemplateResponse('players.html', {'request': request})


@router.get('/result-table')
def result_table(request: Request):
    return templates.TemplateResponse('results.html', {'request': request})