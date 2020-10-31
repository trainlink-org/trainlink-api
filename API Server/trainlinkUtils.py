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


def funcToBytes(functionStates, functionRange):
    if functionRange == 0: #F0 - F4
        byte1 = 128 + functionStates[1]*1 + functionStates[2]*2 + functionStates[3]*4 + functionStates[4]*8 + functionStates[0]*16
        byte2 = None
    elif functionRange == 1: #F5 - F8
        byte1 = 176 + functionStates[5]*1 + functionStates[6]*2 + functionStates[7]*4 + functionStates[8]*8
        byte2 = None
    elif functionRange == 2: #F9 - F12
        byte1 = 160 +functionStates[9]*1 + functionStates[10]*2 + functionStates[11]*4 + functionStates[12]*8
        byte2 = None
    elif functionRange == 3: #F13 - F20
        byte1 = 222
        byte2 = functionStates[13]*1 + functionStates[14]*2 + functionStates[15]*4 + functionStates[16]*8 + functionStates[17]*16 + functionStates[18]*32 + functionStates[19]*64 + functionStates[20]*128
    elif functionRange == 4: #F21 - F28
        byte1 = 223
        byte2 = functionStates[21]*1 + functionStates[22]*2 + functionStates[23]*4 + functionStates[24]*8 + functionStates[25]*16 + functionStates[26]*32 + functionStates[27]*64 + functionStates[28]*128
    else:
        return 0

    return [byte1,byte2]