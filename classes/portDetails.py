
class portDetails(object):

    portNumber = 0
    tcp = False
    udp = False
    portDetails = ""
    reliable = ""

    def __init__(self, portNumber , tcp , udp , portDetails , reliable):
        self.portNumber = portNumber
        self.tcp = tcp
        self.udp = udp
        self.portDetails = portDetails
        self.reliable = reliable