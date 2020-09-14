import serial, asyncio

class comms:
    '''Manages the serial communications of trainlink'''

    ser = None
    prevPacket = {}

    def __init__(self, port):
        global emulator
        try:
            self.ser = serial.Serial(baudrate=115200, port=port)
            self.ser.close()
            self.ser.open()
            emulator = False
        except:
            print("Using Emulator")
            emulator = True

    def updateCabs(self, cabSpeeds, cabDirections):
        for cab in cabSpeeds:
            address = int(cab)
            speed = int(cabSpeeds[cab])
            direction = int(cabDirections[cab])
            packet = b'<t 1 %d %d %d>'%(address, speed, direction)
            try:
                if packet != self.prevPacket[address]:
                    self.ser.write(packet)
                    self.prevPacket[address] = packet
            except KeyError:
                self.write(packet)
                self.prevPacket[address] = packet

    async def directCommand(self, packet):
        packet = packet.encode('utf-8')
        self.write(packet)
        
    async def setPower(self, powerState):
        try:
            powerstate = int(powerState)
            if powerState == 1:
                self.write(b'<1>')
            elif powerState == 0:
                self.write(b'<0>')
            else:
                print("Invalid power state")
        except ValueError:
            print("Invalid power state")
        
    
    def write(self, packet):
        global emulator
        if emulator:
            pass
        else:
            self.ser.write(packet)