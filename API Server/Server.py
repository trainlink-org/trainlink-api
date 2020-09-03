import trainlinkSerial, trainlinkWeb, trainlinkUtils
import threading

socketAddress = "127.0.0.1"
socketPort = "6789"
configFile = 'config/config.xml'

def main():
    pass

xmlUtils = trainlinkUtils.xmlUtils(configFile)
check = xmlUtils.loadXml()
if check == 1:
    print("FileLoad failed")
cabs = xmlUtils.listCabs()

#serial = trainlinkSerial()


mainThread = threading.Thread(target=main)
mainThread.start()

server = trainlinkWeb.web(socketAddress, socketPort, cabs)
server.start()

