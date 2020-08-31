import websockets, asyncio, logging, json

class web:
    """ Serves websocket users """
    address = ""
    port = ""
    USERS = set()

    def __init__ (self, address, port):
        logging.basicConfig()
        self.address = address
        self.port = port

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

    finally:
        await unregister(websocket)

async def register(websocket):
    web.USERS.add(websocket)
    print(websocket)

async def unregister(websocket):
    web.USERS.remove(websocket)

def state_event():
    return json.dumps({"type": "state"})
    