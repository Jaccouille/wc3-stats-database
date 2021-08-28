import requests
import json
from datetime import date
import schedule

GAME = "Footmen%20Vs%20Grunts"
SEASON = "Season%205"
# ET /leaderboard&map=Broken%20Alliances&
# ladder=Public&season=Season%201&
# round=Global&mode=2&sort=rank&order=asc&page=1&limit=15


def request_game_statistic(record_limit):
    http_address = f"https://api.wc3stats.com/leaderboard&map={GAME}&season={SEASON}&mode=Regular&limit={record_limit}"
    r = requests.get(http_address)
    body = r.json().get("body")

    # with open("2021-08-20.json", "r") as fp:
    #     body = json.load(fp).get('body')

    for record in body:
        record["date"] = date.today()
        record["battletag"] = record.pop("name")

    with open(f"{str(date.today())}.json", "w") as f:
        json.dump(r.json(), f, indent=4)


schedule.every().day.at("00:00").do(request_game_statistic)
