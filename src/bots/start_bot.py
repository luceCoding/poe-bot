import pkg_resources
import requests
from datetime import datetime, timezone
from src.bots.seed_bot.seed_bot import SeedBot
import logging
from multiprocessing import Process
from pynput import keyboard

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

def begin():
    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    s = SeedBot()
    s.run()

def on_press(key):
    global break_program
    if key == keyboard.Key.end:
        print('end pressed')
        break_program = True
        return False


if __name__ == "__main__":
    break_program = False
    with keyboard.Listener(on_press=on_press) as listener:
        while break_program is False:
            p = Process(target=begin)
            p.start()
            p.join()
        listener.join()