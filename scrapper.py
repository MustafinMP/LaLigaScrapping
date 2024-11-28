from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.laliga.com/en-RU/laliga-easports/results/2024-25/gameweek-13'

response = requests.get(url)
bs = BeautifulSoup(response.text, "lxml")
games: dict = dict()
for a in bs.find_all('script'):
    if 'matches' in a.text:
        games = json.loads(a.text)
        break

# for a in bs.find_all('script'):
#     try:
#         if 'matches' not in a.text:
#             print('======================')
#             print(json.loads(a.text))
#             print('----------------------')
#     except Exception:
#         pass

# for game in games['props']['pageProps']['matches']:
#     if game['status'] != 'PreMatch':
#         print(f'{game["home_team"]["name"]} {game["home_score"]} - {game["away_score"]} {game["away_team"]["name"]}')
#     else:
#         print(f'{game["home_team"]["name"]} vs {game["away_team"]["name"]}')


def scrap_all_matches():
    for a in bs.find_all('script'):
        if "SportsEvent" in a.text:
            print(a.text)
            scrap_match(json.loads(a.text)['url'])



def scrap_match(url):
    response = requests.get(url)
    team_page = BeautifulSoup(response.text, "lxml")
    for script in team_page.find_all('script'):
        if 'props' in script.text:
            game = json.loads(script.text)
            for goal in game['props']['pageProps']['events']:
                if goal["match_event_kind"]["collection"] == 'goal':
                    print(f'Gooooooooaaaaal by {goal["lineup"]["person"]["nickname"]}')



scrap_all_matches()