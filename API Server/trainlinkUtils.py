import xmltodict, sys

class xmlUtils:
    '''Offers xml utilties needed by the trainlink server'''

    xmlFile = ""

    def __init__(self, path):
        self.path = path

    def loadXml(self, path=""):
        if path == "":
            path = self.path

        try:
            file = open(path)
            file.close()
            with open(path) as file:
                self.xmlFile = xmltodict.parse(file.read())
                file.close()
            return self.xmlFile
        except FileNotFoundError:
            return 1

    def listCabs(self):
        cabs = {}
        try:
            for cab in range(0, len(self.xmlFile['config']['cabs']['cab'])):
                cabs[self.xmlFile['config']['cabs']['cab'][cab]['name']] = self.xmlFile['config']['cabs']['cab'][cab]['address']
        except KeyError:
            cabs[self.xmlFile['config']['cabs']['cab']['name']] = self.xmlFile['config']['cabs']['cab']['address']
        return cabs
    
    def loadConfig(self):
        config = {}
        config["ipAddress"] = self.xmlFile['config']['server']['ip']
        config["port"] = self.xmlFile['config']['server']['port']
        config["serialPort"] = self.xmlFile['config']['server']['serialPort']
        config["debug"] = self.xmlFile['config']['debug']['enableDebug']
        if config["ipAddress"] == "auto":
            config["ipAddress"] = "0.0.0.0"
        elif config["ipAddress"] == "local":
            config["ipAddress"] = "127.0.0.1"
        if config["port"] == "auto":
            config["port"] = "6789"
        return config

class osUtils:
    '''Offers os related utilties needed by the trainlink server'''

    def __init__(self):
        pass

    def getOS(self):
        platforms = {
        'linux1' : 'linux',
        'linux2' : 'linux',
        'darwin' : 'mac',
        'win32' : 'win32'
        }
        if sys.platform not in platforms:
            return sys.platform
        
        return platforms[sys.platform]
