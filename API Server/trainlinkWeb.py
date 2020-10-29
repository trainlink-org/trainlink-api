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
    websocket = None

    # Arrays used for storing runtime data
    power = 0
    users = set()
    cabID = {}
    cabSpeeds = {}
    cabDirections = {}
    #cabFunctions = {"1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "2":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    cabFunctions = {}
    
    # Assigns config variables from arguments
    def __init__ (self, address, port, debug, cabIDxml, serialUtils):
        self.serialUtils = serialUtils
        self.address = address
        self.port = port
        self.cabID = cabIDxml
        self.debug = debug.capitalize()
        functionFormat = []
        for i in range(0,29):
            functionFormat.append(0)
        cabNames = ['Train1', 'Train2'] 
        for cab in cabIDxml:
            self.cabSpeeds[cabIDxml[cab]] = 0
            self.cabDirections[cabIDxml[cab]] = 0
            self.cabFunctions[str(cabIDxml[cab])] = []
            for i in range(0,29):
                self.cabFunctions[cabIDxml[cab]].append(0)
            #self.cabFunctions[cabIDxml[cab]] = 0

        self.cabFunctions['1'].append(0)
        print(self.cabFunctions)

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
        #print("main")
        self.websocket = websocket
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
                elif data["class"] == "cabFunction":
                    await self.cabFunction(data)
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
            await websocket.send(json.dumps({"type": "state", "updateType": "cab", "cab": cab, "speed": self.cabSpeeds[cab], "direction": self.cabDirections[cab], "functions": self.cabFunctions[cab]}))
        await websocket.send(json.dumps({"type": "state", "updateType": "power", "state": self.power}))
    
    def cabControl(self, data):
        try:
            if data["action"] == "setSpeed":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                self.cabSpeeds[address] = data["cabSpeed"]
                self.cabDirections[address] = data["cabDirection"]
            elif data["action"] == "stop":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                self.cabSpeeds[address] = "0"
                self.cabDirections[address] = "0"
            elif data["action"] == "estop":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                self.cabSpeeds[address] = "-1"
                self.cabDirections[address] = "0"
        except UnboundLocalError:
            if self.debug:
                print("Unknowen Address!")

    async def directCommand(self, packet):
        await self.serialUtils.directCommand(packet)
    
    async def setPower(self, powerState):
        await self.serialUtils.setPower(powerState)
        self.power = powerState

    async def cabFunction(self, data):
        if data["state"] != -1:
            self.cabFunctions[self.cabID[data["cab"]]][data["func"]] = data["state"]
        else:
            newState = self.cabFunctions[self.cabID[data["cab"]]]
            newState[data["func"]] = int(not newState[data["func"]])
            print(self.cabFunctions["1"])
        
        legacyMode = True
        if legacyMode:
            await self.serialUtils.setFunction(self.cabID[data["cab"]], functionStates=self.cabFunctions[self.cabID[data["cab"]]])
        else:
            await self.serialUtils.setFunction(self.cabID[data["cab"]], function=data["func"], state=data["state"])
        

    def update(self):
        asyncio.run(self.notifyState(self.websocket))