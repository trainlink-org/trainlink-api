try:
    # Imports required trainlink modules
    import trainlinkSerial, trainlinkWeb, trainlinkUtils
    # Imports required external modules
    import threading, time

    # ----- Need to move to xml -----
    socketAddress = "0.0.0.0"
    socketPort = "6789"
    # Sets the location of the config file
    configFile = 'config/config.xml'

    # Continues the main logic after the server starts
    def main():
        
        print("main")
        while True:
            if killThread:
                break
            serialUtils.updateCabs(server.cabSpeeds, server.cabDirections)
            time.sleep(0.001)

    # Loads in the xml module
    xmlUtils = trainlinkUtils.xmlUtils(configFile)
    # Loads in the xml file and checks it actually was loaded correctly
    check = xmlUtils.loadXml()
    if check == 1:
        print("FileLoad failed")

    # Gets the cabs list from the xml
    cabs = xmlUtils.listCabs()

    serialUtils = trainlinkSerial.comms("COM8")
    # Creates an instance of the trainlinkWeb library
    server = trainlinkWeb.web(socketAddress, socketPort, cabs, serialUtils)

    # Creates a main thread - the server can't run in a second thread, so the main logic has to
    killThread = False
    mainThread = threading.Thread(target=main)
    mainThread.start()


    # Starts the server
    server.start()

except KeyboardInterrupt:
    killThread = True
