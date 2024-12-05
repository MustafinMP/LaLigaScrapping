from fastapi import APIRouter

from services.matches import MatchService

router = APIRouter(prefix='/matches', tags=['matches'])


@router.get('/')
async def matches():
    return MatchService.get_all()


@router.get('/result-table')
async def result_table():
    return MatchService.get_rating_table()
