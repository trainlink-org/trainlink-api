import xmltodict

class xmlUtils:
    '''Offers xml utilties needed by the trainlink server'''

    xmlFile = ""

    def __init__(self, path):
        print('Utils loaded')
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
        for cab in range(0, len(self.xmlFile['config']['cabs']['cab'])):
            cabs[self.xmlFile['config']['cabs']['cab'][cab]['name']] = self.xmlFile['config']['cabs']['cab'][cab]['address']
        return cabs