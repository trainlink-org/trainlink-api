import serial, asyncio

class comms:
    '''Manages the serial communications of trainlink'''

    ser = None
    prevPacket = {}

    def __init__(self, port):

        self.ser = serial.Serial(baudrate=115200, port=port)
        self.ser.close()
        self.ser.open()

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
                self.ser.write(packet)
                self.prevPacket[address] = packet

    async def directCommand(self, packet):
        packet = packet.encode('utf-8')
        self.ser.write(packet)
        
    async def setPower(self, powerState):
        if int(powerState):
            self.ser.write(b'<1>')
        else:
            self.ser.write(b'<0>')