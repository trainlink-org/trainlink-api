try:
    # Imports required trainlink modules
    import trainlinkSerial, trainlinkWeb, trainlinkUtils
    # Imports required external modules
    import threading, time, asyncio

    # Sets the location of the config file
    configFile = 'config/config.xml'

    # Continues the main logic after the server starts
    def main():
        serialMsg = serialUtils.startComms()
        if server.debug:
            print(serialMsg)
        readloop = threading.Thread(target=readLoop)
        readloop.start()
        while True:
            if killThread:
                break
            serialUtils.updateCabs(server.cabSpeeds, server.cabDirections)
            readSerial = serialUtils.getLatest()
            if readSerial != False:
                if readSerial == "<p2>":
                    if server.debug:
                        print("CURRENT OVERLOAD")
                    server.power = 0
                    server.update()
            time.sleep(0.001)

    def readLoop():
        while True:
            if killThread:
                break
            serialUtils.readInLoop()

    # Loads in the xml module
    xmlUtils = trainlinkUtils.xmlUtils(configFile)
    # Loads in the xml file and checks it actually was loaded correctly
    check = xmlUtils.loadXml()
    if check == 1:
        print("FileLoad failed")

    # Gets the cabs list from the xml
    cabs = xmlUtils.listCabs()
    # Gets the server config from the xml
    config = xmlUtils.loadConfig()

    serialUtils = trainlinkSerial.comms(config["serialPort"])
    # Creates an instance of the trainlinkWeb library
    server = trainlinkWeb.web(config['ipAddress'], config["port"], config["debug"], cabs, serialUtils)

    # Creates a main thread - the server can't run in a second thread, so the main logic has to
    killThread = False
    mainThread = threading.Thread(target=main)
    mainThread.start()


    # Starts the server
    server.start()

except KeyboardInterrupt:
    killThread = True
