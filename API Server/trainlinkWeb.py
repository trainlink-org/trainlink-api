import webUtils as utils
import websockets, asyncio, logging, json

cabID = {}
cabs = {}

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
        global cabs
        cabID = cabIDxml
        for cab in cabIDxml:
            cabs[cabIDxml[cab]] = 0
        print(cabs)

    def start(self):
        print("Starting server at %s:%s" %(self.address,self.port))
        start_server = websockets.serve(main, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    
async def main (websocket, path):
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["class"] == "cabControl":
                print("cabControl")
                cabControl(data)

    finally:
        await unregister(websocket)

async def register(websocket):
    web.users.add(websocket)
    print(websocket)

async def unregister(websocket):
    web.users.remove(websocket)

def state_event():
    return json.dumps({"type": "state"})

def cabControl(data):
    if data["action"] == "setSpeed":
        address = utils.obtainAddress(data["cabAddress"], cabID)
        print(address)
    