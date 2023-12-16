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


def main():
    lgc = Logic()
    app = Interface(
        logic=lgc)
    app.display()


if __name__ == "__main__":
    main()

# TODO implementar en CONFIG tab 3 botones (new, edit, delete) que interactúen con la selección actual en el treeview
# TODO implementar una pestaña nueva de "Ayuda / (?)" que explique cómo usar el programa
