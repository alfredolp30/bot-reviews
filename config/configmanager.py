import json
import logging

class ConfigManager:
    CONFIG_FILE = "config/config.json"
    REGIONS_FILE = "config/regions.json"

    def __init__(self) -> None:
        self.configJson = self.__getJsonFromFile(self.CONFIG_FILE)
        self.regionsJson = self.__getJsonFromFile(self.REGIONS_FILE)

    def __getJsonFromFile(self, filename: str): 
        with open(filename, 'r') as configFile:
            try: 
                jsonData = json.load(configFile)
                return jsonData
            except:
                logging.error('Parse json file error')
        
        return {}

    def getValueFromConfig(self, path: str):
        keys = path.split('/')

        value = None
        for key in keys: 
            try: 
                if value == None:
                    value = self.configJson[key] 
                else:
                    value = value[key]
            except:
                logging.error('Key json not found')
        
        return value

    def getRegions(self):
        return self.regionsJson