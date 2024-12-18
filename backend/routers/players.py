from fastapi import APIRouter

from services.players import PlayerService

router = APIRouter(prefix='/players', tags=['players'])


@router.get('/')
async def players():
    return PlayerService.get_all()