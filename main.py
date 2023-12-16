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

# TODO Añadir funcionalidad: botones (new, edit, delete) que funcionen con la selección de fila actual en el treeview
# TODO Plantear cambiar iconos por "iconos" en fuentes. Cambios de color/tamaño dinámicos
# TODO implementar una pestaña nueva de "Ayuda / (?)" que explique cómo usar el programa
