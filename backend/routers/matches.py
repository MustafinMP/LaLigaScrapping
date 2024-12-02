from fastapi import APIRouter

from services.matches import MatchService

router = APIRouter(prefix='/matches', tags=['matches'])


@router.get('/')
async def matches():
    return MatchService.get_all()