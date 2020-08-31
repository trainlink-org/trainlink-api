import trainlinkSerial, trainlinkWeb, trainlinkUtils, threading

socketAddress = "127.0.0.1"
socketPort = "6789"

def main():
    pass

#serial = trainlinkSerial()
server = trainlinkWeb.web(socketAddress, socketPort)
#utils = trainlinkUtils()


mainThread = threading.Thread(target=main)
mainThread.start()

server.start()

