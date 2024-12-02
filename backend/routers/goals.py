from fastapi import APIRouter

from services.goals import GoalsService

router = APIRouter(prefix='/goals', tags=['goals'])


@router.get('/')
async def goals():
    return GoalsService.get_all()


@router.get('/count')
async def count():
    return GoalsService.get_goal_count()