import configparser

config = configparser.RawConfigParser()
config.read("./Configurations/urlDetails.ini")


class ReadLoginConfig():
    def getWay2AutomationURL(self):
        return config.get("URLS", "way2AutomationURL")
