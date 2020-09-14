#imports the sub-modules
import webUtils as utils
#imports the required external modules
import websockets, asyncio, json



class web:
    """ Serves websocket users """

    # The trainlinkSerial instance
    serialUtils = None

    # The variables needed for configuration
    address = ""
    port = ""
    debug = False

    # Arrays used for storing runtime data
    power = 0
    users = set()
    cabID = {}
    cabSpeeds = {}
    cabDirections = {}
    
    
    # Assigns config variables from arguments
    def __init__ (self, address, port, debug, cabIDxml, serialUtils):
        self.serialUtils = serialUtils
        self.address = address
        self.port = port
        self.cabID = cabIDxml
        self.debug = debug.capitalize()
        for cab in cabIDxml:
            self.cabSpeeds[cabIDxml[cab]] = 0
            self.cabDirections[cabIDxml[cab]] = 0

    def start(self):
        print("Starting server at %s:%s" %(self.address,self.port))
        if self.debug == "True":
            print("Debug enabled")
        start_server = websockets.serve(self.main, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    async def notifyState(self, websocket):
        if self.users:
            for user in self.users:
                await self.stateEvent(user)
    
    async def main (self, websocket, path):
        await self.register(websocket)
        try:
            await self.stateEvent(websocket)
            async for message in websocket:
                data = json.loads(message)
                #print(data)
                if data["class"] == "cabControl":
                    #print("cabControl")
                    self.cabControl(data)
                    await self.notifyState(websocket)
                elif data["class"] == "directCommand":
                    #print(data)
                    await self.directCommand(data["command"])
                elif data["class"] == "power":
                    await self.setPower(data["state"])
                    await self.notifyState(websocket)
        finally:
            await self.unregister(websocket)

    async def register(self, websocket):
        self.users.add(websocket)
        await websocket.send(json.dumps({"type": "config", "cabs": self.cabID,"debug": self.debug}))

    async def unregister(self, websocket):
        web.users.remove(websocket)

    async def stateEvent(self, websocket):
        for cab in self.cabSpeeds:
            await websocket.send(json.dumps({"type": "state", "updateType": "cab", "cab": cab, "speed": self.cabSpeeds[cab], "direction": self.cabDirections[cab]}))
        await websocket.send(json.dumps({"type": "state", "updateType": "power", "state": self.power}))
    
    def cabControl(self, data):
        if data["action"] == "setSpeed":
            address = utils.obtainAddress(data["cabAddress"], self.cabID)
            self.cabSpeeds[address] = data["cabSpeed"]
            self.cabDirections[address] = data["cabDirection"]
        elif data["action"] == "stop":
            address = utils.obtainAddress(data["cabAddress"], self.cabID)
            self.cabSpeeds[address] = "0"
        elif data["action"] == "estop":
            address = utils.obtainAddress(data["cabAddress"], self.cabID)
            self.cabSpeeds[address] = "-1"

    async def directCommand(self, packet):
        await self.serialUtils.directCommand(packet)
    
    async def setPower(self, powerState):
        await self.serialUtils.setPower(powerState)
        self.power = powerState