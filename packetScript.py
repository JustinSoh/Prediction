# from datetime import datetime
# from Prediction.classes.packet import packet
# # from Prediction.classes.portDetails import  portDetails
# # import math
# # import numpy as np
# def readFromFile(filename):
#     packets = []
#     file_object = open(filename, "r")
#     lines = file_object.read().split("Packet #")
#     for i in range (1 , len(lines)):
#         data = lines[i].split("TimeStamp:")
#         count = data[0].replace(" ", "")
#         count = count.replace("\n" , "")
#         data = data[1].split("Packet")
#         time = data[0].replace('\n', "")
#         time = datetime.strptime(time, ' %H:%M:%S %d/%m/%Y')
#
#
#         ipLayer = "None"
#         test1 = "None"
#         destinationIP = ""
#         sourceIP = ""
#         protocolType = ""
#         sourcePort = 0
#         destinationPort = 0
#         typeOfPort = ""
#         sourceType = ""
#         destinationType = ""
#         sourcePortName = ""
#         destinationPortName = ""
#
#         try:
#             if "Layer UDP:" in data[1]:
#                 data = data[1].split("Layer UDP:")
#                 splitData = data[0].split("Layer IP:")
#                 ipLayer = splitData[1]
#                 ipLayerData = ipLayer.split("\n")
#                 for i in ipLayerData:
#                     if "Destination: " in i:
#                         destinationIP = i
#                         destinationIP = destinationIP.split(":")
#                         destinationIP = destinationIP[1]
#                     if "Source: " in i:
#                         sourceIP = i;
#                         sourceIP = sourceIP.split(":")
#                         sourceIP = sourceIP[1]
#                     if "Protocol: " in i:
#                         protocolType = i.split(":")
#                         protocolType = protocolType[1].split("(")
#                         protocolType = protocolType[0]
#                         protocolType = protocolType.replace(" ", "")
#
#
#                 data = data[1].split("Layer UDP:")
#                 data = data[0].split("Layer")
#                 udpLayer = data[0]
#                 udpLayerData = udpLayer.split("\n")
#                 for i in udpLayerData:
#                     if "Source Port: " in i:
#                         sourcePort = i.split(":")
#                         sourcePort = int(sourcePort[1])
#                         sourceType = checkTypeOfPort(sourcePort)
#                         sourceDetails = getPortDetails(sourcePort , sourceType)
#                         sourcePortName = sourceDetails.portDetails
#
#
#                     if "Destination Port: " in i:
#                         destinationPort = i.split(":")
#                         destinationPort = int(destinationPort[1])
#                         destinationType = checkTypeOfPort(destinationPort)
#                         destinationDetails = getPortDetails(destinationPort , destinationType)
#                         destinationPortName = destinationDetails.portDetails
#
#
#
#
#
#             elif "Layer TCP:" in data[1]:
#                 data = data[1].split("Layer TCP:")
#                 splitData = data[0].split("Layer IP:")
#                 ipLayer = splitData[1]
#                 ipLayerData = ipLayer.split("\n")
#                 for i in ipLayerData:
#                     if "Destination: " in i:
#                         destinationIP = i
#                         destinationIP = destinationIP.split(":")
#                         destinationIP = destinationIP[1]
#                     if "Source: " in i:
#                         sourceIP = i;
#                         sourceIP = sourceIP.split(":")
#                         sourceIP = sourceIP[1]
#                     if "Protocol: " in i:
#                         protocolType = i.split(":")
#                         protocolType = protocolType[1].split("(")
#                         protocolType = protocolType[0]
#                         protocolType = protocolType.replace(" ", "")
#
#
#                 data = data[1].split("Layer TCP:")
#                 data = data[0].split("Layer")
#                 tcpLayer = data[0]
#                 tcpLayerData = tcpLayer.split("\n")
#
#                 for i in tcpLayerData:
#                     if "Source Port: " in i:
#                         sourcePort = i.split(":")
#                         sourcePort = int(sourcePort[1])
#                         sourceType = checkTypeOfPort(sourcePort)
#                         sourceDetails = getPortDetails(sourcePort, sourceType)
#                         sourcePortName = sourceDetails.portDetails
#
#                     if "Destination Port: " in i:
#                         destinationPort = i.split(":")
#                         destinationPort = int(destinationPort[1])
#                         destinationType = checkTypeOfPort(destinationPort)
#                         destinationDetails = getPortDetails(destinationPort , destinationType)
#                         destinationPortName = destinationDetails.portDetails
#
#
#
#
#
#
#
#
#
#         except Exception as e:
#             value = 0
#
#         """if sourcePort == 80 or sourcePort == 443 or destinationPort == 80 or destinationPort == 443:"""
#
#         data = createPacket(count , protocolType , destinationPort , sourcePort , time , sourceIP , destinationIP , sourceType , destinationType , sourcePortName , destinationPortName)
#         if data is not None:
#             packets.append(data)
#         #print (detailsString)
#
#     return packets
#
#
#
#
# def createPacket(count , protocolType ,  destinationPort , sourcePort , datetime , sourceIP , destinationIP , sourceType , destinationType , sourcePortName , destinationPortName):
#
#     if protocolType is None or destinationPort is 0 or sourcePort is 0 or sourceIP is None or destinationIP is None:
#         return None
#     else:
#         pkt = packet(count , protocolType , destinationPort , sourcePort , datetime , sourceIP , destinationIP ,sourceType , destinationType , sourcePortName , destinationPortName)
#         """ print(count)
#         print(datetime)
#         print("Protocol: " + protocolType)
#         print(sourcePortName + "|" + destinationPortName)
#         print(str(sourcePort) + sourceType + "|" + str(destinationPort) + destinationType)
#         print("Destination:" + destinationIP + "| Source:" + sourceIP)
#         print("================")"""
#         return pkt
#
#
# def printInfo(packet):
#     print(packet.packetId)
#     print(packet.dateTime)
#     print("Protocol: " + packet.protocolType)
#     print(packet.sourcePortName + "|" + packet.destinationPortName)
#     print(str(packet.sourcePortNumber) + packet.sourcePortType + "|" + str(packet.destinationPortNumber) + packet.destinationPortType)
#     print("Source:" + packet.sourceIp + "| Destination:" + packet.destinationIp)
#     print("================")
#
# def printBandwidthInfo(bandwidth):
#     print("Document ID: " + bandwidth.documentId)
#     print("Bandwidth ID: " + bandwidth.bandwidthId )
#     print("HostId: " + bandwidth.hostId)
#     print("Included: " + str(bandwidth.included))
#     print("Organization Id: " + bandwidth.organizationId)
#     print("Risk Status: " + bandwidth.riskScore)
#     print("Time: " +  str(bandwidth.time))
#     print("Usage: " + bandwidth.usage)
#     print("Processed: " + str(bandwidth.processed))
#     print("================")
# def checkTypeOfPort(portNumber):
#     if portNumber <= 1023:
#         return "Well-Known Port"
#     elif portNumber <= 49151:
#         return "Registered Port"
#     else:
#         return "Private Port"
#
# def getPortDetails(portNumber , portType):
#     file_object = open("data/portDetails.txt", "r")
#     lines = file_object.read().split("@")
#     if portNumber is not None:
#         if portType is not None:
#             if portNumber <= 49151:
#                 for i in lines:
#                     info = i.split("|")
#                     pn = info[0]
#                     tcp = info[1]
#                     udp = info[2]
#                     description = ""
#                     reliable = ""
#                     tcpBoolean = False
#                     udpBoolean = False
#                     if checkIfInt(pn):
#                         if portNumber == int(pn):
#                             if tcp is not None:
#                                 tcpBoolean = True
#                             if udp is not None:
#                                 udpBoolean = True
#                             description = info[3]
#                             reliable = info[4]
#                             pd = portDetails(portNumber, tcpBoolean, udpBoolean, description, reliable)
#                             return pd
#             else:
#                 pd = portDetails(portNumber, False, False, "Private Port", "Private Port")
#                 return pd
#
#
# def checkIfInt(value):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False
#
#
# def getWebPackets(packets):
#     webPackets = []
#     for p in packets:
#         if p.sourcePortNumber == 80 or p.destinationPortNumber == 80 or p.sourcePortNumber == 443  or p.destinationPortNumber == 443:
#             webPackets.append(p)
#     return webPackets
#
# """if "destination port" in l.lower():
#     print(l)
# if "protocol" in l.lower():
#     print(l)"""
# def getBandwidthThreshold(fullData):
#     #data = [3,4,5,1,2,7,5,3,30,40,30,2,5,3,5,4,3]
#     data = []
#     for i in fullData:
#         data.append(float(i.usage))
#     mean = np.mean(data)
#     differences = []
#     for i in data:
#         differences.append(mean - i)
#     sqrDifferences = []
#     for i  in differences:
#         sqrDifferences.append(i * i)
#     differencemean = np.mean(sqrDifferences)
#     sd = math.sqrt(differencemean)
#     range1from =  mean - (sd * 1)
#     range1to = mean + (sd * 1)
#     range2from = mean - (sd * 2)
#     range2to = mean + (sd * 2)
#     range3from = mean - (sd * 3)
#     range3to = mean + (sd * 3)
#
#
#     print(str(range1from) + " to " + str(range1to))
#     print(str(range2from) + " to " + str(range2to))
#     print(str(range3from) + " to " + str(range3to))
#
#     #plt.scatter(data , [5,5,5,5,5,5,5,5])
#    # plt.bar([range3from , range2from , range1from , mean ,  range1to , range2to , range3to] , [10 ,10 , 10,10,10])
#     #plt.scatter(100, 5)
#     #plt.plot(data);
#     #plt.plot([low , mean , high])
#     #plt.show()
#     return range1from  , range1to , range2from , range2to , range3from , range3to
#
#
# def calculateBandwidthRisk(bandwidth , value):
#     riskScore = ""
#     if "User" not in value:
#         value = float(value)
#         if value >= bandwidth[0] and value <= bandwidth[1]:
#             riskScore = "low"
#         elif value >= bandwidth[2] and value <= bandwidth[3]:
#             riskScore = "medium"
#         elif value >= bandwidth[4] and value <= bandwidth[5]:
#             riskScore = "high"
#         else:
#             riskScore = "very high"
#         return riskScore
#     else:
#         return "Error"
#
#
# packet = readFromFile("data/logsv2.txt")


data = open("data/logsv2.txt")
lines = data.readlines()
for i in lines:
    arrayOfData = []
    cont = False;
    if "Packet #" in i:
        print(i)
        cont == True;
    if cont == True:

