import requests
import json
from datetime import date
from urllib.parse import urlencode, quote
from src.record_table import insert_daily_record
import sys
import schedule
import time
import logging
from pathlib import Path
from src.config import config

log_dir = Path().absolute() / "logs"

# Create a directory to save log files
if not log_dir.is_dir():
    log_dir.mkdir()

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(log_dir / "daily_record.log")),
    ],
)

logger = logging.getLogger(__name__)

try:
    URL_ARGS = {
        "map": config.get("URL_ARGS", "MAP"),
        "season": config.get("URL_ARGS", "SEASON"),
        "limit": config.get("URL_ARGS", "LIMIT"),
        "mode": config.get("URL_ARGS", "MODE"),
    }
except KeyError as e:
    logger.error(f"Following variable's missing from config file : {str(e)}")
    sys.exit()

URL = "https://api.wc3stats.com/leaderboard&"


def request_game_record():

    # quote_via=quote parameter replace " " character by "%20"
    http_address = URL + urlencode(URL_ARGS, quote_via=quote)

    try:
        response = requests.get(http_address)
        response.raise_for_status()
    except Exception as e:
        logger.error(str(e))
        return
    else:
        body = response.json().get("body")
        logger.info(f"Received json body with {len(body)} records")

        for record in body:
            record["date"] = date.today()

        with open(str(log_dir / f"{str(date.today())}.json"), "w") as f:
            json.dump(response.json(), f, indent=4)

        try:
            insert_daily_record(body)
            logger.info(f"Inserted {len(body)} record on {date.today()}")
        except Exception as e:
            logger.error(str(e))
            return

def main():

    # Request game record every day at 00:00 AM
    schedule.every().day.at("00:00").do(request_game_record)

    logger.info("Starting scheduler")

    while True:
        schedule.run_pending()
        time.sleep(1)

    logger.info("Closing scheduler")
