import asyncio

from bs4 import BeautifulSoup
import requests
import json

import db_session
from repositories.match import MatchRepository
from repositories.goal import GoalRepository
from repositories.player import PlayerRepository
from repositories.team import TeamRepository


class Scrapper:

    @staticmethod
    async def get_page(url: str) -> BeautifulSoup:
        while True:
            try:
                response = requests.get(url)
                return BeautifulSoup(response.text, "lxml")
            except Exception:
                print(f'WARNING:    Превышено время ожидания от {url}. Повторная попытка подключения через 30 секунд')
                await asyncio.sleep(30)

    @staticmethod
    async def scrap_all_gameweeks() -> None:
        print('INFO:    Run scrapper')
        gameweeks = 38
        for gameweek in range(1, gameweeks + 1):
            await Scrapper.scrap_gameweek_results(gameweek)
        print('INFO:    Finish scrapper')

    @staticmethod
    async def scrap_gameweek_results(gameweek: int = 13) -> None:
        print(f'INFO:    Parse Gameweek {gameweek}')
        url = f'https://www.laliga.com/en-RU/laliga-easports/results/2024-25/gameweek-{gameweek}'
        page = await Scrapper.get_page(url)
        for script in page.find_all('script'):
            if "SportsEvent" in script.text:
                url = json.loads(script.text)['url']
                if not Scrapper._match_is_exist(url):
                    data = await Scrapper.extract_match_data(url)
                    await Scrapper.process_data(data, url)

    @staticmethod
    def _match_is_exist(match_url: str) -> bool:
        with db_session.create_session() as session:
            repository = MatchRepository(session)
            return repository.get_by_url(match_url) is not None

    @staticmethod
    async def extract_match_data(match_url: str) -> dict:
        for script in (await Scrapper.get_page(match_url)).find_all('script'):
            if 'props' in script.text:
                return json.loads(script.text)['props']['pageProps']

    @staticmethod
    async def process_data(data: dict, match_url: str):
        with db_session.create_session() as session:
            team_repository = TeamRepository(session)
            goal_repository = GoalRepository(session)
            match_repository = MatchRepository(session)
            player_repository = PlayerRepository(session)

            game = data['match']

            # добавление команд
            home_team_data = game["home_team"]
            if (home_team := team_repository.get_by_laliga_id(home_team_data['id'])) is None:
                team_repository.add(
                    home_team_data["nickname"],
                    home_team_data["id"],
                    home_team_data["shield"]['url']
                )
                home_team = team_repository.get_by_laliga_id(home_team_data["id"])
            away_team_data = game["away_team"]
            if (away_team := team_repository.get_by_laliga_id(away_team_data['id'])) is None:
                team_repository.add(
                    away_team_data["nickname"],
                    away_team_data["id"],
                    away_team_data["shield"]['url']
                )
                away_team = team_repository.get_by_laliga_id(away_team_data["id"])

            home_score = game.get('home_score', None)
            away_score = game.get('away_score', None)
            if home_score is None or away_score is None:
                return
            match_repository.add(
                match_url,
                game['slug'],
                game['date'],
                home_score,
                away_score,
                home_team,
                away_team
            )

            match_object = match_repository.get_by_url(match_url)

            goals = [
                event
                for event in data['events']
                if event["match_event_kind"]["collection"] == 'goal'
            ]
            for goal in goals:
                team_id = goal['lineup']['team']['id']
                player_data = goal['lineup']['person']
                if (player := player_repository.get_by_name_and_team_id(player_data['name'],
                                                                        team_id)) is None:
                    player_repository.add(
                        player_data['name'],
                        player_data['nickname'],
                        team_id
                    )
                    player = player_repository.get_by_name_and_team_id(player_data['name'], team_id)
                if 'assist' in goal.keys():
                    assist_team_id = goal['assist']['team']['id']
                    assist_player_data = goal['lineup']['person']
                    if (assist_player := player_repository.get_by_name_and_team_id(assist_player_data['name'],
                                                                                   assist_team_id)) is None:
                        player_repository.add(
                            assist_player_data['name'],
                            assist_player_data['nickname'],
                            assist_team_id
                        )
                        assist_player = player_repository.get_by_name_and_team_id(assist_player_data['name'],
                                                                                  assist_team_id)
                    goal_repository.add(goal['minute'], match_object, player, assist_player)
                else:
                    goal_repository.add(goal['minute'], match_object, player)

