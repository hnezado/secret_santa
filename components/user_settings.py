import json
import logging as log


class UserSettings:
    def __init__(self) -> None:
        self.user_settings = self.load_user_settings()
        
    def load_user_settings(self) -> dict:
        """Opens the user settings file"""
        
        with open("user_settings/user_settings.json") as f:
            raw = f.read()
            sett = json.loads(raw)
        return self.parse_user_settings(sett)
        
    def parse_user_settings(self, settings: object) -> dict:
        """Parses specific settings"""
        
        parsed_sett = {}
        for k, v in settings.items():
            if not v:
                msg = f'Setting "{k}" was not defined'
                log.critical(msg)
                raise Exception(msg)
            if k == "style":
                parsed_sett[k] = f'user_settings/styles/{v}.json'
            else:
                parsed_sett[k] = v
        return parsed_sett
    
    def unparse_user_settings(self, settings: object) -> dict:
        """Unparses specific settings"""
        
        unparsed_sett = {}
        for k, v in settings.items():
            if not v:
                msg = f'Setting "{k}" was not defined'
                log.critical(msg)
                raise Exception(msg)
            if k == "style":
                unparsed_sett[k] = v.split("/")[-1].split(".json")[0]
            else:
                unparsed_sett[k] = v
        return unparsed_sett

    def update_lang(self, lang) -> None:
        """Updates the language settings"""
        
        self.user_settings["lang"] = lang
        self.update_user_settings()
        
    def update_user_settings(self):
        """Updates the user settings file"""
        
        unparsed_data = self.unparse_user_settings(self.user_settings)
        output = json.dumps(unparsed_data, indent=2)
        with open ("user_settings/user_settings.json", "w") as f:
            f.write(output)

    def get_lang(self):
        """Returns the current set language"""
        
        return self.user_settings["lang"]
