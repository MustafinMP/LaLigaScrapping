from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=['pages']
)

templates = Jinja2Templates(directory='../frontend/templates')


@router.get('/matches')
def matches(request: Request):
    return templates.TemplateResponse('matches.html', {'request': request})


@router.get('/players')
def players(request: Request):
    return templates.TemplateResponse('players.html', {'request': request})
