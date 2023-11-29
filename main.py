import json
import datetime as dt
import logging as log
from interface import Interface
from logic import Logic

# Logging configuration (./logs/...)
log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f'./logs/{dt.datetime.now().strftime("%Y-%m-%d")}.log',
    level=log.INFO)

# Settings import
with open("./settings/settings.json") as f:
    raw = f.read()
    sett = json.loads(raw)
    
def parse_settings(settings):
    """Parses specific settings before sending them as attributes"""
    parsed_sett = {}
    for k, v in settings.items():
        if not v:
            msg = f'Setting "{k}" was not defined'
            log.critical(msg)
            raise Exception(msg)
        if k == "style":
            parsed_sett[k] = f'./settings/styles/{v}.json'
        else:
            parsed_sett[k] = v
    return parsed_sett

def main():
    lgc = Logic()
    app = Interface(
        logic=lgc,
        settings=parse_settings(sett))
    app.display()


if __name__ == "__main__":
    main()
