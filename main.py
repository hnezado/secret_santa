import datetime as dt
import logging as log
from interface import Interface
from pathlib import Path
from logic import Logic

# Logging configuration (./logs/...)f
Path("./logs").mkdir(parents=True, exist_ok=True)
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

# TODO Añadir funcionalidad: botones (new) que funcionen con la selección de fila actual en el treeview
# TODO implementar una pestaña nueva de "Ayuda / (?)" que explique cómo usar el programa
# TODO Configurar labels y text_boxes en popups (custom languages)
#   Necesitaría "popup_upd_add/edit/del") con label.configure(text="path/de/language")...
# TODO Quitar OrdDicts si es posible
#   Convertir/update los OrderedDict a zip(logic.member_attrs, values)
