import webUtils as utils
import websockets, asyncio, logging, json

cabID = {}
cabSpeeds = {}
cabDirections = {}

class web:
    """ Serves websocket users """
    address = ""
    port = ""
    users = set()
    
    

    def __init__ (self, address, port, cabIDxml):
        logging.basicConfig()
        self.address = address
        self.port = port
        global cabID
        global cabSpeeds
        global cabDirections
        cabID = cabIDxml
        for cab in cabIDxml:
            cabSpeeds[cabIDxml[cab]] = 0
            cabDirections[cabIDxml[cab]] = 0

    def start(self):
        print("Starting server at %s:%s" %(self.address,self.port))
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
                if data["class"] == "cabControl":
                    self.cabControl(data)
                    await self.notifyState(websocket)
                if data["class"] == "directCommand":
                    pass
        finally:
            await self.unregister(websocket)

    async def register(self, websocket):
        self.users.add(websocket)
        await websocket.send(json.dumps({"type": "config", "cabs": cabID}))

    async def unregister(self, websocket):
        web.users.remove(websocket)

    async def stateEvent(self, websocket):
        for cab in cabSpeeds:
            await websocket.send(json.dumps({"type": "state", "cab": cab, "speed": cabSpeeds[cab], "direction": cabDirections[cab]}))
    
    def cabControl(self, data):
        if data["action"] == "setSpeed":
            address = utils.obtainAddress(data["cabAddress"], cabID)
            cabSpeeds[address] = data["cabSpeed"]
            cabDirections[address] = data["cabDirection"]
        elif data["action"] == "stop":
            address = utils.obtainAddress(data["cabAddress"], cabID)
            cabSpeeds[address] = "0"
        elif data["action"] == "estop":
            address = utils.obtainAddress(data["cabAddress"], cabID)
            cabSpeeds[address] = "-1"
    