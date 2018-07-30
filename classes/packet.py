from datetime import datetime
class packet(object):
    packetId = ""
    protocolType = ""
    destinationPortNumber = 0
    sourcePortNumber = 0
    dateTime = datetime.now()
    sourceIp = ""
    destinationIp = ""
    sourcePortType = ""
    destinationPortType = ""
    sourcePortName = ""
    destinationPortName = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, packetId , protocolType, destinationPortNumber , sourcePortNumber , dateTime , sourceIp , destinationIp , sourcePortType , destinationPortType , sourcePortName , destinationPortName ):
        self.packetId = packetId
        self.protocolType = protocolType
        self.destinationPortNumber = destinationPortNumber
        self.sourcePortNumber = sourcePortNumber
        self.dateTime = dateTime
        self.sourceIp = sourceIp
        self.destinationIp = destinationIp
        self.sourcePortType = sourcePortType
        self.destinationPortType = destinationPortType
        self.sourcePortName = sourcePortName
        self.destinationPortName = destinationPortName


