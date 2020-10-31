import trainlinkUtils
import serial, asyncio

class comms:
    '''Manages the serial communications of trainlink'''

    ser = None
    prevPacket = {}
    line = ""
    oldLine = ""
    emulator = False

    def __init__(self, port):
        try:
            self.ser = serial.Serial(baudrate=115200, port=port, timeout=2)
            self.ser.close()
            self.ser.open()
        except:
            print("Using Emulator")
            self.emulator = True

    def updateCabs(self, cabSpeeds, cabDirections):
        for cab in cabSpeeds:
            address = int(cab)
            speed = int(cabSpeeds[cab])
            direction = int(cabDirections[cab])
            packet = b'<t 1 %d %d %d>'%(address, speed, direction)
            try:
                if packet != self.prevPacket[address]:
                    self.write(packet)
                    self.prevPacket[address] = packet
            except KeyError:
                self.write(packet)
                self.prevPacket[address] = packet

    async def directCommand(self, packet):
        packet = packet.encode('utf-8')
        self.write(packet)
        
    async def setPower(self, powerState):
        try:
            powerState = int(powerState)
            if powerState == 1:
                self.write(b'<1>')
            elif powerState == 0:
                self.write(b'<0>')
            else:
                print("Invalid power state")
        except ValueError:
            print("Invalid power state")
    
    async def setFunction(self, cab, *args, **kwargs):
        functionStates = kwargs.get('functionStates', None)
        function = kwargs.get('function', None)
        state = kwargs.get('state', None)
        legacyMode = True
        if legacyMode:
            bytes = trainlinkUtils.funcToBytes(functionStates, 0)
            self.write(b'<f %d %d>'%(int(cab),bytes[0]))
            
            bytes = trainlinkUtils.funcToBytes(functionStates, 1)
            self.write(b'<f %d %d>'%(int(cab),bytes[0]))
            
            bytes = trainlinkUtils.funcToBytes(functionStates, 2)
            self.write(b'<f %d %d>'%(int(cab),bytes[0]))

            bytes = trainlinkUtils.funcToBytes(functionStates, 3)
            self.write(b'<f %d %d %d>'%(int(cab),bytes[0],bytes[1]))

            bytes = trainlinkUtils.funcToBytes(functionStates, 4)
            self.write(b'<f %d %d %d>'%(int(cab),bytes[0],bytes[1]))
            
        else:
            self.write(b'<F %s %s %s'%(cab,function,state))
        
    
    def write(self, packet):
        if self.emulator:
            pass
        else:
            self.ser.write(packet)
    
    def read(self, char):
        line = self.ser.read_until(char)
        return line
    
    def startComms(self):
        if not self.emulator:
            line1 = self.ser.read_until(b'>')
            line2 = self.ser.read_until(b'>')
            line1 = line1.decode("utf-8")
            line2 = line2.decode("utf-8")
            return line1 + line2

    def getLatest(self):
        if self.line == self.oldLine:
            return False
        else:
            self.oldLine = self.line
            return self.line

    def readInLoop(self):
        if not self.emulator:
            line = self.ser.read_until(b'>')
            if line != '':
                self.line = line
            