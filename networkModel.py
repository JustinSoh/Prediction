from classes.packet import packet
from datetime import datetime
from classes.portDetails import portDetails
from classes.bandwidth import  bandwidth
from dateutil import tz
from flask import Flask
from flask.ext.socketio import SocketIO
import numpy as np
import pandas as pd
import scipy
from sklearn.neighbors import NearestNeighbors
from sklearn import neighbors
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split

from sklearn import metrics

import requests
import re
import matplotlib.pyplot as plt

import math
def readFromFile(filename):
    packets = []
    file_object = open(filename, "r")
    lines = file_object.read().split("Packet #")
    for i in range (1 , len(lines)):
        data = lines[i].split("TimeStamp:")
        count = data[0].replace(" ", "")
        count = count.replace("\n" , "")
        data = data[1].split("Packet")
        time = data[0].replace('\n', "")
        time = datetime.strptime(time, ' %H:%M:%S %d/%m/%Y')



        ipLayer = "None"
        test1 = "None"
        destinationIP = ""
        sourceIP = ""
        protocolType = ""
        sourcePort = 0
        destinationPort = 0
        typeOfPort = ""
        sourceType = ""
        destinationType = ""
        sourcePortName = ""
        destinationPortName = ""

        try:
            if "Layer UDP:" in data[1]:
                data = data[1].split("Layer UDP:")
                splitData = data[0].split("Layer IP:")
                ipLayer = splitData[1]
                ipLayerData = ipLayer.split("\n")
                for i in ipLayerData:
                    if "Destination: " in i:
                        destinationIP = i
                        destinationIP = destinationIP.split(":")
                        destinationIP = destinationIP[1]
                    if "Source: " in i:
                        sourceIP = i;
                        sourceIP = sourceIP.split(":")
                        sourceIP = sourceIP[1]
                    if "Protocol: " in i:
                        protocolType = i.split(":")
                        protocolType = protocolType[1].split("(")
                        protocolType = protocolType[0]
                        protocolType = protocolType.replace(" ", "")


                data = data[1].split("Layer UDP:")
                data = data[0].split("Layer")
                udpLayer = data[0]
                udpLayerData = udpLayer.split("\n")
                for i in udpLayerData:
                    if "Source Port: " in i:
                        sourcePort = i.split(":")
                        sourcePort = int(sourcePort[1])
                        sourceType = checkTypeOfPort(sourcePort)
                        sourceDetails = getPortDetails(sourcePort , sourceType)
                        sourcePortName = sourceDetails.portDetails


                    if "Destination Port: " in i:
                        destinationPort = i.split(":")
                        destinationPort = int(destinationPort[1])
                        destinationType = checkTypeOfPort(destinationPort)
                        destinationDetails = getPortDetails(destinationPort , destinationType)
                        destinationPortName = destinationDetails.portDetails





            elif "Layer TCP:" in data[1]:
                data = data[1].split("Layer TCP:")
                splitData = data[0].split("Layer IP:")
                ipLayer = splitData[1]
                ipLayerData = ipLayer.split("\n")
                for i in ipLayerData:
                    if "Destination: " in i:
                        destinationIP = i
                        destinationIP = destinationIP.split(":")
                        destinationIP = destinationIP[1]
                    if "Source: " in i:
                        sourceIP = i;
                        sourceIP = sourceIP.split(":")
                        sourceIP = sourceIP[1]
                    if "Protocol: " in i:
                        protocolType = i.split(":")
                        protocolType = protocolType[1].split("(")
                        protocolType = protocolType[0]
                        protocolType = protocolType.replace(" ", "")


                data = data[1].split("Layer TCP:")
                data = data[0].split("Layer")
                tcpLayer = data[0]
                tcpLayerData = tcpLayer.split("\n")

                for i in tcpLayerData:
                    if "Source Port: " in i:
                        sourcePort = i.split(":")
                        sourcePort = int(sourcePort[1])
                        sourceType = checkTypeOfPort(sourcePort)
                        sourceDetails = getPortDetails(sourcePort, sourceType)
                        sourcePortName = sourceDetails.portDetails

                    if "Destination Port: " in i:
                        destinationPort = i.split(":")
                        destinationPort = int(destinationPort[1])
                        destinationType = checkTypeOfPort(destinationPort)
                        destinationDetails = getPortDetails(destinationPort , destinationType)
                        destinationPortName = destinationDetails.portDetails









        except Exception as e:
            value = 0




        """if sourcePort == 80 or sourcePort == 443 or destinationPort == 80 or destinationPort == 443:"""

        data = createPacket(count , protocolType , destinationPort , sourcePort , time , sourceIP , destinationIP , sourceType , destinationType , sourcePortName , destinationPortName)
        if data is not None:
            packets.append(data)

        #print (detailsString)

    return packets




def createPacket(count , protocolType ,  destinationPort , sourcePort , datetime , sourceIP , destinationIP , sourceType , destinationType , sourcePortName , destinationPortName):

    if protocolType is None or destinationPort is 0 or sourcePort is 0 or sourceIP is None or destinationIP is None:
        return None
    else:
        pkt = packet(count , protocolType , destinationPort , sourcePort , datetime , sourceIP , destinationIP ,sourceType , destinationType , sourcePortName , destinationPortName)
        """ print(count)
        print(datetime)
        print("Protocol: " + protocolType)
        print(sourcePortName + "|" + destinationPortName)
        print(str(sourcePort) + sourceType + "|" + str(destinationPort) + destinationType)
        print("Destination:" + destinationIP + "| Source:" + sourceIP)
        print("================")"""
        return pkt


def printInfo(packet):
    print(packet.packetId)
    print(packet.dateTime)
    print("Protocol: " + packet.protocolType)
    print(packet.sourcePortName + "|" + packet.destinationPortName)
    print(str(packet.sourcePortNumber) + packet.sourcePortType + "|" + str(packet.destinationPortNumber) + packet.destinationPortType)
    print("Source:" + packet.sourceIp + "| Destination:" + packet.destinationIp)
    print("================")

def printBandwidthInfo(bandwidth):
    print("Document ID: " + bandwidth.documentId)
    print("Bandwidth ID: " + bandwidth.bandwidthId )
    print("HostId: " + bandwidth.hostId)
    print("Included: " + str(bandwidth.included))
    print("Organization Id: " + bandwidth.organizationId)
    print("Risk Status: " + bandwidth.riskScore)
    print("Time: " +  str(bandwidth.time))
    print("Usage: " + bandwidth.usage)
    print("Processed: " + str(bandwidth.processed))
    print("================")
def checkTypeOfPort(portNumber):
    if portNumber <= 1023:
        return "Well-Known Port"
    elif portNumber <= 49151:
        return "Registered Port"
    else:
        return "Private Port"

def getPortDetails(portNumber , portType):
    file_object = open("data/portDetails.txt", "r")
    lines = file_object.read().split("@")
    if portNumber is not None:
        if portType is not None:
            if portNumber <= 49151:
                for i in lines:
                    info = i.split("|")
                    pn = info[0]
                    tcp = info[1]
                    udp = info[2]
                    description = ""
                    reliable = ""
                    tcpBoolean = False
                    udpBoolean = False
                    if checkIfInt(pn):
                        if portNumber == int(pn):
                            if tcp is not None:
                                tcpBoolean = True
                            if udp is not None:
                                udpBoolean = True
                            description = info[3]
                            reliable = info[4]
                            pd = portDetails(portNumber, tcpBoolean, udpBoolean, description, reliable)
                            return pd
            else:
                pd = portDetails(portNumber, False, False, "Private Port", "Private Port")
                return pd


def checkIfInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def getWebPackets(packets):
    webPackets = []
    for p in packets:
        if p.sourcePortNumber == 80 or p.destinationPortNumber == 80 or p.sourcePortNumber == 443  or p.destinationPortNumber == 443:
            webPackets.append(p)
    return webPackets

"""if "destination port" in l.lower():
    print(l)
if "protocol" in l.lower():
    print(l)"""
def getBandwidthThreshold(fullData):
    #data = [3,4,5,1,2,7,5,3,30,40,30,2,5,3,5,4,3]
    data = []
    for i in fullData:
        data.append(float(i.usage))
    mean = np.mean(data)
    differences = []
    for i in data:
        differences.append(mean - i)
    sqrDifferences = []
    for i  in differences:
        sqrDifferences.append(i * i)
    differencemean = np.mean(sqrDifferences)
    sd = math.sqrt(differencemean)
    range1from =  mean - (sd * 1)
    range1to = mean + (sd * 1)
    range2from = mean - (sd * 2)
    range2to = mean + (sd * 2)
    range3from = mean - (sd * 3)
    range3to = mean + (sd * 3)


    print(str(range1from) + " to " + str(range1to))
    print(str(range2from) + " to " + str(range2to))
    print(str(range3from) + " to " + str(range3to))

    #plt.scatter(data , [5,5,5,5,5,5,5,5])
   # plt.bar([range3from , range2from , range1from , mean ,  range1to , range2to , range3to] , [10 ,10 , 10,10,10])
    #plt.scatter(100, 5)
    #plt.plot(data);
    #plt.plot([low , mean , high])
    #plt.show()
    return range1from  , range1to , range2from , range2to , range3from , range3to


def calculateBandwidthRisk(bandwidth , value):
    riskScore = ""
    if "User" not in value:
        value = float(value)
        if value >= bandwidth[0] and value <= bandwidth[1]:
            riskScore = "low"
        elif value >= bandwidth[2] and value <= bandwidth[3]:
            riskScore = "medium"
        elif value >= bandwidth[4] and value <= bandwidth[5]:
            riskScore = "high"
        else:
            riskScore = "very high"
        return riskScore
    else:
        return "Error"


#----------------------------------------------------------------------Bandwidth below -------------------------------------------------------------------------------------------------------------------

#packets = readFromFile("data/logsv2.txt")
#webPackets = getWebPackets(packets)

def addIntoDB(bandwidthId, hostId, organizationId, riskScore , time , usage):

    doc_ref = db.collection(u'Bandwidth').document()
    doc_ref.set(
        {
            u'bandwidthId': bandwidthId,
            u'hostId': hostId,
            u'included': False,
            u'organizationId': organizationId,
            u'riskScore': riskScore,
            u'time': time,
            u'usage': usage,
            u'processed': True
        })



def readFromDB():
    trainingSet = []
    trainingData = db.collection(u'Bandwidth').where(u'included', u'==', True).get()

    for doc in trainingData:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        trainingSet.append(createBandwidthClass(doc))

    unallocatedSet = []
    unallocatedData = db.collection(u'Bandwidth').where(u'processed' , u'==' , False).get()
    for doc in unallocatedData:
        unallocatedSet.append(createBandwidthClass(doc))

    return trainingSet , unallocatedSet

def readAllFromDB():
    allData = db.collection(u'Bandwidth').get()
    allDataSet = []
    for doc in allData:
        allDataSet.append(createBandwidthClass(doc))

    dataToBeProcessed = db.collection(u'Bandwidth').where(u'included' , u'==' , False).get()
    notInclduedData = []
    for doc in dataToBeProcessed:
        notInclduedData.append(createBandwidthClass(doc))



    return allDataSet , notInclduedData

def updateDB(docID , field , data):
    document_ref = db.collection(u'Bandwidth').document(docID)
    document_ref.update({field: data})
    print("Successfully Updated")

def updateAllData(data):
    notIncludedData = data[1]
    allData = data[0]


    for i in notIncludedData:
        usage = i.usage
        time = i.time
        Day = []
        Usage = []
        Class = []
        documentIdTest = i.documentId
        xSource = usage
        ySource = datetime.date(time).weekday()
        print("Current xSource is " + str(xSource))
        print("Current ySource is " + str(ySource))

        for i in allData:
            Usage.append(i.usage)
            Day.append(datetime.date(i.time).weekday())
            Class.append(0)

        ir = pd.DataFrame({'$x': Usage, '$y': Day})
        ir.columns = ["x", "y"]
        ir['CLASS'] = Class
        data = []
        for i in range(0, len(Day)):
            newData = [Usage[i], Day[i]]
            data.append(newData)
        print("All data")
        print(ir)

        result = calculateDistanceAndResults(data, xSource, ySource)
        initialDataFrame = getDataframeFromResult(result, ir, xSource, ySource)
        comparisonDataFrameArray = []

        print("Initial Dataframe")
        print("x is : " + str(xSource) + " and y is : " + str(ySource))
        print(initialDataFrame.to_string())

        print("Comparison Started")
        for index, row in initialDataFrame.iterrows():
            newXSource = row['xTarget']
            newYSource = row['yTarget']
            print("Original had x of " + str(xSource) + " y of " + str(ySource))
            print(str(newXSource) + "|" + str(newYSource))
            result = calculateDistanceAndResults(data, newXSource, newYSource)
            dataFrame = getDataframeFromResult(result, ir, newXSource, newYSource)
            print(dataFrame)
            comparisonDataFrameArray.append(dataFrame)
            print("==============")

        count = calculateCount(xSource, ySource, comparisonDataFrameArray, initialDataFrame)
        #value to change
        if float(count) >= 15:
            updateDB(documentIdTest , "included" , True)

        # ir = pd.DataFrame({'$x': Usage, '$y': Day})
        # ir.columns = ["x", "y"]
        # ir['CLASS'] = Class
        # data = []
        # for i in range(0, len(Day)):
        #     newData = [Usage[i], Day[i]]
        #     data.append(newData)
        #
        # result = calculateDistanceAndResults(data, xSource, ySource)
        # initialDataFrame = getDataframeFromResult(result, ir, xSource, ySource)
        # comparisonDataFrameArray = []
        #
        # print("x is : " + str(xSource) + " and y is : " + str(ySource))
        # print(initialDataFrame.to_string())
        #
        # Usage.append(xSource)
        # Day.append(ySource)
        # Class.append(0)
        #
        # ir = pd.DataFrame({'$x': Usage, '$y': Day})
        # ir.columns = ["x", "y"]
        # ir['CLASS'] = Class
        # data = []
        # for i in range(0, len(Day)):
        #     newData = [Usage[i], Day[i]]
        #     data.append(newData)
        #
        # for index, row in initialDataFrame.iterrows():
        #     newXSource = row['xTarget']
        #     newYSource = row['yTarget']
        #     print("Original had x of " + str(xSource) + " y of " + str(ySource))
        #     print(str(newXSource) + "|" + str(newYSource))
        #     result = calculateDistanceAndResults(data, newXSource, newYSource)
        #     dataFrame = getDataframeFromResult(result, ir, newXSource, newYSource)
        #     print(dataFrame)
        #     comparisonDataFrameArray.append(dataFrame)
        #     print("==============")
        #
        # riskScore = calculateCount(xSource, ySource, comparisonDataFrameArray, initialDataFrame)


def createBandwidthClass(doc):
    documentId = doc.id
    bandwidthId = doc.to_dict()['bandwidthId']
    hostId = doc.to_dict()['hostId']
    included = doc.to_dict()['included']
    organizationId = doc.to_dict()['organizationId']
    riskScore = doc.to_dict()['riskScore']
    time = doc.to_dict()['time']
    usage = doc.to_dict()['usage']
    processed = doc.to_dict()['processed']
    bw = bandwidth(documentId , bandwidthId , hostId , included , organizationId , riskScore , time , usage ,processed)
    return bw

def addInFakeData():

    documentId = ["1", "2", "3" , "4" , "5" , "6" , "7" , "8", "9" , "10"]
    bandwidthId = ["1", "2", "3" , "4" , "5" , "6" , "7" , "8", "9" , "10"]
    hostId = ["host1", "host1" , "host1" ,"host1", "host1" , "hos    t2" , "host2" , "host2", "host2" ,"host2" ]
    riskScore = ["low" , "low" , "low" , "low" , "low" , "low" , "low" , "low" , "low" ,"low" ]
    usage = ['300','400','500','100','200','700','500','300','300','200']
    time = []
    from_zone = tz.gettz('GMT')
    for i in range (0 , len(documentId)):
        doc_ref = db.collection(u'Bandwidth').document(documentId[i])
        doc_ref.set(
            {
                u'bandwidthId': bandwidthId[i] ,
                u'hostId': hostId[i] ,
                u'included' : True ,
                u'organizationId': u'testing' ,
                u'riskScore' : riskScore[i] ,
                u'time' :datetime.now(from_zone),
                u'usage' : usage[i],
                u'processed' : False
            }
    )

    unsorted = db.collection(u'Bandwidth').document(u'unsorted')
    unsorted.set(
        {
            u'bandwidthId': u'unsorted1',
            u'hostId': u'host1',
            u'included' : False,
            u'organizationId': u'testing',
            u'riskScore': "none",
            u'time': datetime.now(from_zone),
            u'usage': "50",
            u'processed': False
        }
    )

import pyrebase
from firebasedata import LiveData

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template
from flask_socketio import SocketIO, send


#db = firestore.db()

#Fake data add into db first
#addInFakeData()
#readFromDB()
#addIntoDB("1", None, None , None ,None , None, None , None)

def convertUsageMetrics(usage):
    if "mbit/s" in usage:
        data = usage.split(" ")
        usageMb = float(data[0])
    elif "kbit/s" in usage:
        data = usage.split(" ")
        usageMb = float(data[0]) / 1000
    elif "gbit/s" in usage:
        data = usage.split(" ")
        usageMb = float(data[0]) * 1000
    else:
        # for seans
        data = usage.split(" ")
        usageMb = float(data[0]) / 1000000
    return usageMb

def convertMessageIntoData(message):
    data = message.split(",")
    bandwidthId = data[0][0]
    hostId = data[1]
    organizationId = data[2]
    time = datetime.strptime(data[3], ' %H:%M:%S %d/%m/%Y')
    txusage = data[4]
    txUsageMbits = convertUsageMetrics(txusage)
    rxusage = data[5]
    rxUsageMbits = convertUsageMetrics(rxusage)
    usage = txUsageMbits + rxUsageMbits
    print(str(usage) + " usage is here ")
    #testing123,host1,testing, 22:14:32 29/7/2018,500 mbit/s,500 mbit/s
    return bandwidthId , hostId , organizationId , time , usage



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
cred = credentials.Certificate('./LogHub.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def hello_world():

    # config = {
    #
    #     "serviceAccount": "./LogHub.json"
    # };
    #
    # firebase = pyrebase.initialize_app(config)
    # db = firebase.database()
    # print(db.child().get().val())
    # return bandwidth.val();
    return render_template('index.html')


from sklearn.datasets import *
def calculateDistanceAndResults(trainingData , xValue , yValue ):
    #value to change
    nn = NearestNeighbors(5)
    nn.fit(trainingData)
    test = np.array([xValue, yValue])
    test1 = test.reshape(1, -1)
    result = nn.kneighbors(test1, 5)
    return result
def getDataframeFromResult(result , ir , xSource , ySource):
    distance = []
    xTargetSet = []
    yTargetSet = []
    xSourceSet = []
    ySourceSet = []
    for i in range(0, len(result[1])):
        for d in result[0][i]:
            distance.append(d)
        for a in result[1][i]:
            xTargetSet.append(ir.ix[a]['x'])
            yTargetSet.append(ir.ix[a]['y'])
            xSourceSet.append(xSource)
            ySourceSet.append(ySource)

    initialDataFrame = pd.DataFrame(
        {'$xTarget': xTargetSet, '$yTarget': yTargetSet, '$distance': distance, '$xSource': xSourceSet,'$ySource': ySourceSet})
    initialDataFrame.columns = ["distance" , "xOrigin" , "xTarget" , "yOrigin" , "yTarget"]
    return initialDataFrame
def calculateCount(xValue , yValue ,data , initialData):
    count = 0;
    for i in data:
        for index , row in i.iterrows():
            comparisonX = row['xTarget']
            comparisonY = row['yTarget']

            if float(comparisonX) == float(xValue) and float(comparisonY) == float(yValue):
                count =  count + 1;
                print("Current x: " + str(xValue) + " and Current y :" + str(yValue))
                print(row['xTarget'])
                print(row['yTarget'])
                print(row)
                print("~~~~~~~~~~~~~~~~~")
    print("The total count: " + str(count))
    return count
def calculateRiskScore(xValue , yValue , data , initalData):
    count = 0;
    lowRiskRow = []
    highRiskAvg = []
    highRiskRow = []

    counter = 0
    for i in data:
        for index , row in i.iterrows():
            comparisonX = row['xTarget']
            comparisonY = row['yTarget']

            if float(comparisonX) == float(xValue) and float(comparisonY) == float(yValue):
                count =  count + 1;
                print("Current x: " + str(xValue) + " and Current y :" + str(yValue))
                print(row['xTarget'])
                print(row['yTarget'])
                print(row)
                lowRiskRow.append(row)
                print("~~~~~~~~~~~~~~~~~")

        #highRiskRow.append([i['xOrigin'][0] , i['yOrigin'][0]])



    riskLevel = ""
    #The number of neighbour is 5
    mean = 0
    if count > 0:
        mean = calculateMeanDistance(initalData , xValue , yValue)
        # print(initalData)
        # Tdistance = initalData['distance']
        # total = 0
        # for i in Tdistance:
        #     print("Individual distance is " + str(i))
        #     total = total + i
        # print("Total Distance between: " + str(xValue) + "," + str(yValue) + " and other points is " + str(Tdistance))
        # mean = total / len(Tdistance)
        # print("The mean is " + str(mean))
    else:
        mean = calculateMeanDistance(initalData , xValue , yValue)

    riskLevel = calculateRiskBasedOnMean(mean , count)
    print(mean)
    print("Total Count: " + str(count))
    return riskLevel
def calculateRiskBasedOnMean(mean , count):
    countRisk = 0
    meanRisk = 0
    extraRisk = 0
    if count >= 5:
        countRisk = 0.05
    elif count >= 5:
        countRisk = 0.1
    elif count >= 2:
        countRisk = 0.2
    else:
        countRisk = 0.6

    if mean <=100:
        meanRisk = 0.05
    elif mean <= 300:
        meanRisk = 0.10
    elif mean <= 600:
        meanRisk = 0.15
    elif mean <= 800:
        meanRisk = 0.20
    else:
        meanRisk = 0.50



    countRiskPercentage = (countRisk ) * 0.5
    meanRiskPercentage = (meanRisk ) * 0.5
    print(countRiskPercentage )
    print(meanRiskPercentage)
    print("asdasdasdasdd")
    totalRisk =(countRisk +  meanRiskPercentage) * 100

    finalRisk = ""
    if totalRisk <= 25.0:
        finalRisk = "Low"
    elif totalRisk <= 50.0:
        finalRisk = "Medium"
    elif totalRisk <= 75.0:
        finalRisk = "High"
    else:
        finalRisk = "Very High"
    return finalRisk
def calculateMeanDistance(initialData , xValue , yValue):
    print(initialData)
    Tdistance = initialData['distance']
    total = 0
    for i in Tdistance:
        print("Individual distance is " + str(i))
        total = total + i
    print("Total Distance between: " + str(xValue) + "," + str(yValue) + " and other points is " + str(Tdistance))
    mean = total / len(Tdistance)
    print("The mean is " + str(mean))
    return mean
def getDistanceOfNeighbors(data , input):
    Day = []
    Usage = []
    Class = []

    xSource = input[4]
    ySource = datetime.date(input[3]).weekday()

    for i in data[0]:
        Usage.append(i.usage)
        Day.append(datetime.date(i.time).weekday())
        Class.append(0)
    ir = pd.DataFrame({'$x': Usage, '$y': Day})
    ir.columns = ["x" , "y"]
    ir['CLASS'] = Class
    data = []
    for i in range (0 , len(Day)):
        newData = [Usage[i] , Day[i]]
        data.append(newData)

    result = calculateDistanceAndResults(data , xSource , ySource)
    initialDataFrame = getDataframeFromResult(result , ir , xSource , ySource)
    comparisonDataFrameArray = []

    print(initialDataFrame[['xTarget', 'yTarget']])


    Usage.append(xSource)
    Day.append(ySource)
    Class.append(0)

    ir = pd.DataFrame({'$x': Usage, '$y': Day})
    ir.columns = ["x", "y"]
    ir['CLASS'] = Class
    data = []
    for i in range(0, len(Day)):
        newData = [Usage[i], Day[i]]
        data.append(newData)

    for index , row in initialDataFrame.iterrows():
        newXSource = row['xTarget']
        newYSource = row['yTarget']
        print("Original had x of " + str(xSource) + " y of " + str(ySource))
        print(str(newXSource) + "|" +  str(newYSource))
        result = calculateDistanceAndResults(data , newXSource , newYSource)
        dataFrame = getDataframeFromResult(result, ir, newXSource, newYSource)
        print(dataFrame)
        comparisonDataFrameArray.append(dataFrame)
        print("==============")

    #Do comparison
    riskScore = calculateRiskScore(xSource , ySource , comparisonDataFrameArray , initialDataFrame)
    print(riskScore)
    return riskScore
    # initialDataFrame = pd.DataFrame({'$xTarget': xTarget , '$yTarget': yTarget , '$distance': distance  , '$xSource': xSource} )
    # print(initialDataFrame.to_string())

    # print(ir.ix[result[1]])
    #iris = load_iris()
    # ir = pd.DataFrame(iris.data)

    # Day = np.array(Day).reshape(-1 ,1)
    # nn.fit(Day , Usage)
    # print(nn)
    # print(ir.describe())
    # test = np.array()



    # test = np.array([498])
    # test1 = np.array(test).reshape(1 , -1)
    # print(nn.kneighbors(test1 , 5))
    # print(ir.ix[[6, 4, 8, 7, 0],])
    # Usage = preprocessing.scale(Usage)
    # X_train , X_test , y_train , y_test = train_test_split(Usage , Day ,  test_size = .33 ,  random_state = 17 )
    # clf = neighbors.KNeighborsClassifier()
    # clf.fit(X_train , y_train)
    # print(clf)



@socketio.on('message')
def handle_message(message):
    print('received message: ' + message);

    # data = readFromDB()
    # test = convertMessageIntoData("testing123,host1,testing, 22:14:32 29/7/2018,488 mbit/s,488 mbit/s")
    # getDistanceOfNeighbors(data ,test )
    #
    # trainingData = db.collection(u'Bandwidth').where(u'included', u'==', "true").get()

    allData = readAllFromDB()
    if len(allData[0]) < 40:
        if message is not None:
            test = convertMessageIntoData(message)
            addIntoDB(bandwidthId=test[0], hostId=test[1], organizationId=test[2], riskScore="training", time=test[3],
                      usage=test[4])
            send("training data", broadcast=True)
    else:
        updateAllData(allData)
        #working
        data = readFromDB()
        if len(data[0]) == 0:
            addInFakeData()

        if message is not None:
            data = readFromDB()
            test = convertMessageIntoData(message)
            value = getDistanceOfNeighbors(data, test)
            print(value)
            # value = calculateBandwidthRisk(bandwidth , test[4])
            addIntoDB(bandwidthId=test[0], hostId=test[1], organizationId=test[2], riskScore=value, time=test[3],
                      usage=test[4])
            send(value, broadcast=True)


if __name__ == '__main__':

    socketio.run(app , host= '0.0.0.0')

    # bandwidth = getBandwidthThreshold()
        # riskLevel = calculateBandwidthRisk(bandwidth , msg)

        # print("Low range: " + str(bandwidth[0]) + " - " + str(bandwidth[1]))
        # print("Medium range: " + str(bandwidth[2]) + " - " + str(bandwidth[3]))
        # print("High range: " + str(bandwidth[4]) + " - " + str(bandwidth[5]))
        # print('Value of : ' + msg + " has a risk score of " + riskLevel)



