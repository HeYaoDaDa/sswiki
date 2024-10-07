import configparser

_config = configparser.ConfigParser()
_config.read("config.ini")
SS_DIR = _config['DEFAULT']['GameDataDir']