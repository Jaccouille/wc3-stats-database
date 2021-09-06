from logging import log
import requests
import json
from datetime import date
from urllib.parse import urlencode, quote
from src.record_table import insert_daily_record
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
from src.config import logger, log_dir
import schedule
import time


load_dotenv()

try:
    URL_ARGS = {
        "map": os.environ["MAP"],
        "season": os.environ["SEASON"],
        "limit": os.environ["LIMIT"],
        "mode": os.environ["MODE"],
    }
except KeyError as e:
    logger.error(f"Following .env variable's missing : {str(e)}")
    sys.exit()

URL = "https://api.wc3stats.com/leaderboard&"


def request_game_record():

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

        with open(str(log_dir / f"{str(date.today())}.json"), "w") as f:
            json.dump(response.json(), f, indent=4)

        try:
            insert_daily_record(body)
            logger.info(f"Inserted {len(body)} record on {date.today()}")
        except Exception as e:
            logger.error(str(e))


def main():
    # schedule.every().day.at("00:00").do(request_game_record)
    schedule.every(10).seconds.do(request_game_record)

    logger.info("Starting scheduler")

    while True:
        schedule.run_pending()
        time.sleep(1)

    logger.info("Closing scheduler")
