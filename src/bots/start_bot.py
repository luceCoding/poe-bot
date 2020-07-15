import pkg_resources
from src.bots.seed_bot.seed_bot import SeedBot

resource_package = pkg_resources.get_distribution('poe_bot').location

if __name__ == "__main__":
    s = SeedBot()
    s.start()