import requests
import json
from datetime import date
import schedule
from urllib.parse import urlencode, quote
from record_table import insert_daily_record

URL_ARGS = {
    'map': 'Footmen Vs Grunts',
    'season': 'Season 5',
    'limit': 15,
    'mode': 'Regular'
}

URL = "https://api.wc3stats.com/leaderboard"

# /leaderboard&map=Broken%20Alliances&
# ladder=Public&season=Season%201&
# round=Global&mode=2&sort=rank&order=asc&page=1&limit=15

def request_game_statistic(record_limit):
    # quote_via=quote replace " " by "%20"
    http_address = URL + urlencode(URL_ARGS, quote_via=quote)
    r = requests.get(http_address)
    body = r.json().get("body")

    # with open("2021-08-20.json", "r") as fp:
    #     body = json.load(fp).get('body')

    for record in body:
        record["date"] = date.today()

    with open(f"{str(date.today())}.json", "w") as f:
        json.dump(r.json(), f, indent=4)
    insert_daily_record(record)



# schedule.every().day.at("00:00").do(request_game_statistic)
