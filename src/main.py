import requests
import json
from datetime import date
from urllib.parse import urlencode, quote
from record_table import insert_daily_record
import logging

logging.basicConfig(
    filename="daily_record.log",
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger("__name__")

URL_ARGS = {
    "map": "Footmen Vs Grunts",
    "season": "Season 5",
    "limit": 15,
    "mode": "Regular",
}

URL = "https://api.wc3stats.com/leaderboard&"
RECORD_LIMIT = 15


def request_game_record(record_limit):

    # quote_via=quote replace " " by "%20"
    http_address = URL + urlencode(URL_ARGS, quote_via=quote)

    try:
        response = requests.get(http_address)
        response.raise_for_status()
    except Exception as e:
        logger.error(str(e))
        return
    else:
        body = response.json().get("body")
        logger.info(f"received json body with {len(body)} records")

        for record in body:
            record["date"] = date.today()

        with open(f"{str(date.today())}.json", "w") as f:
            json.dump(response.json(), f, indent=4)

        try:
            insert_daily_record(body)
            logger.info(f"Inserted {len(body)} record on {date.today()}")
        except Exception as e:
            logger.error(str(e))


request_game_record(RECORD_LIMIT)
# schedule.every().day.at("00:00").do(request_game_record)
