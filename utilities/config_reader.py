import configparser


class ConfigReader:
    def __init__(self, config_file_path='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)

    def get_common_option(self, option_name, fallback=None):
        return self.config.get('COMMON', option_name, fallback=fallback)

    def get_browser_option(self, browser_name, option_name, fallback=None):
        return self.config.get(browser_name, option_name, fallback=fallback)