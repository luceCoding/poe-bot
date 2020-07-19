import pkg_resources
import requests
from datetime import datetime, timezone
from src.bots.seed_bot.seed_bot import SeedBot
import logging

resource_package = pkg_resources.get_distribution('poe_bot').location


def is_expired():
    url = r"https://www.google.com/"
    response = requests.get(url=url)
    date = response.headers['Date']
    online_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
    now = datetime.utcnow()

    start = datetime(year=2020, month=7, day=16, tzinfo=timezone.utc)
    expire = datetime(year=2020, month=7, day=27, tzinfo=timezone.utc)

    for time in [online_date, now]:
        timez = time.replace(tzinfo=timezone.utc)
        if start >= timez or expire <= timez:
            return True
    return False

if __name__ == "__main__":
    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    s = SeedBot()
    s.run()
