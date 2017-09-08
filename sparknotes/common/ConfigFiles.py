import ConfigParser

class ConfigFiles:
    def __init__(self):
        pass

    # ==fc== return the final config object by reading from the config file
    @staticmethod
    def config():
        config_file_path = ConfigFiles.config_file()
        config = ConfigParser.ConfigParser()
        config.read("../../config/" + config_file_path)
        config = {
            'url': config.get("Mongo", "url"),
            'username': config.get("Mongo", "username"),
            'password': config.get("Mongo", "password"),
            'dbname': config.get("Mongo", "dbname"),
            'scrapeUrl': config.get("Scrape", "url"),
        }
        return config

    # ==fc== get the config file path object from reading from the environment file
    @staticmethod
    def config_file():
        config = ConfigParser.ConfigParser()
        config.read("../../config/environment.cfg")
        config_file = config.get("Config", "configFile")
        return config_file
