import json

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()

        self.default_config = {
            "apikey": None,
            "whisper_model":"large-v2",
            "Vocal_remover_model":"Kim_Vocal_1"
        }

        if not self.config:
            self.config = self.default_config
            self.save_config(self.config)

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
            return config
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_config(self, config_data):
        self.config.update(config_data)
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file, indent=4)
