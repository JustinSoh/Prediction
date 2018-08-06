import socket
import sys
from _thread import *
from datetime import datetime

def splitIdentifier(data):
    d = data.split("{")
    data = d[1].split("}")
    return data[0]


def convertToTime(date , time , sunormoon):
    sunormoon = sunormoon.split(":")
    newTime = datetime.strptime(" " + time + " " + sunormoon[0] + " " + date, ' %I:%M:%S %p %d/%m/%Y')
    return newTime

from datetime import datetime , timedelta
def uploadIntoDBIndBW(hostname , time , organization , upload , download):

    document_ref = db.collection(u'IndBW').document()
    document_ref.set({
        u'hostname': hostname,
        u'organizationId': organization,
        u'time': time - timedelta(hours=8),
        u'upload': upload,
        u'download': download
    })
    print("Successfully Updated")



def getHostIdentification(data):
    if "@Hostname@" in data:
        data = ""
        data = splitIdentifier(data);
        data1 = data.replace("\n", "")
        Hostname = data1;
    if "@Organization ID@" in data:
        data = ""
        data = splitIdentifier(data);
        OrganizationId = data;
    if "@IP Address@" in data:
        data = ""
        data = splitIdentifier(data);
        IPAddress = data;
    if "@Default Gateway@" in data:
        data = ""
        data = splitIdentifier(data);
        DefaultGateway = data;
    if "@MAC Address@" in data:
        data = ""
        data = splitIdentifier(data)
        MACAddress = data;

    #
    # if Hostname is not "-1" and IPAddress is not "-1" and MACAddress is not "-1" and DefaultGateway is not "-1" and OrganizationId is not "-1":
    #     print(Hostname)
    #     print(IPAddress)
    #     print(MACAddress)
    #     print(DefaultGateway)
    #     print(OrganizationId)

def addEntryToHostMapping(Hostname , OrganizationId , IPAddress , DefaultGateway , MACAddress):
    document_ref = db.collection(u'HostMapping').document(Hostname)
    try:
        document_ref.get()
        document_ref.update({
            u'Hostname': Hostname,
            u'OrganizationId': OrganizationId,
            u'IPAddress': IPAddress,
            u'DefaultGateway': DefaultGateway,
            u'MACAddress': MACAddress
         })
        print("Updated")
    except:
        document_ref.set({
            u'Hostname': Hostname,
            u'OrganizationId': OrganizationId,
            u'IPAdress': IPAddress,
            u'DefaultGateway': DefaultGateway,
            u'MACAddress': MACAddress
        })
        print("Created")
    # except:
    #     document_ref.set({
    #         u'Hostname': Hostname,
    #         u'OrganizationId': OrganizationId,
    #         u'IPAdress': IPAddress,
    #         u'DefaultGateway': DefaultGateway,
    #         u'MACAddress': MACAddress
    #     })
    #     print("Successfully Created")


import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./LogHub.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()



HOST = ""
PORT = 10009
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket created!')
try:
    # hello_world()
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Error: ' + str(msg[0] + ' Message ' + msg[1]))
    sys.exit()

print('Socket bind complete.')

s.listen(10)
print('Now listening')
import time, threading

def clientthread(conn):
    count = 0;
    num = 0;
    Hostname = "-1"
    IPAddress = "-1"
    MACAddress = "-1"
    DefaultGateway = "-1"
    OrganizationId = "-1"
    while True:
        data = (conn.recv(5000)).decode()
        print(data)
        # if "@Hostname@" in data:
        #     data = splitIdentifier(data);
        #     Hostname = data;
        # if "@Organization ID@" in data:
        #     data = splitIdentifier(data);
        #     OrganizationId = data;
        # if "@IP Address@" in data:
        #     data = splitIdentifier(data);
        #     IPAddress = data;
        # if "@Default Gateway@" in data:
        #     data = splitIdentifier(data);
        #     DefaultGateway = data;
        # if "@MAC Address@" in data:
        #     data = splitIdentifier(data)
        #     MACAddress = data;
        if "@check@" in data:
            #hostname,organiaationid,ip,dgw,mac
            data =  data.split(":")
            data = data[4].split(",")
            Hostname = data[0]
            OrganizationId = data[1]
            IPAddress = data[2]
            DefaultGateway = data[3]
            MACAddress = data[4]
            addEntryToHostMapping(Hostname, OrganizationId, IPAddress, DefaultGateway, MACAddress)
            print("*************")
            print("entry added")
            print("*************")
        if "Download/Upload" in data:
            data = data.split(" ")
            bwHostname = data[0]
            time = convertToTime(data[1], data[2], data[3])
            organization = data[4].split(":")
            organization = organization[0]
            data = data[5]
            data = data.split("{")
            data = data[1].split("}")
            data = data[0].split(",")
            upload = data[0]
            upload = upload.split("B")
            upload = upload[0]
            upload = float(upload) * 8
            upload = upload / 1000000
            # upload = (upload * 8000000)
            download = data[1]
            download = download.split("B")
            download = download[0]
            download = float(download) * 8
            download = download / 1000000
            # download = (download * 8000000)
            uploadIntoDBIndBW(bwHostname, time, organization, upload, download)
            print(str(upload) + "Mbit/s is upload")
            print(str(download) + "Mbit/s is download")
            print("============")
            print(MACAddress)
            print(DefaultGateway)
            print(OrganizationId)
            print(Hostname)
            print(IPAddress)
            print("===========")

        # if MACAddress is not "-1" and DefaultGateway is not "-1" and IPAddress is not "-1" and OrganizationId is not "-1" and Hostname is not "-1":
        #     addEntryToHostMapping(Hostname, OrganizationId, IPAddress, DefaultGateway, MACAddress)
        #     MACAddress = "-1"
        #     DefaultGateway = "-1"
        #     IPAddress = "-1"
        #     OrganizationId = "-1"
        #     Hostname = "-1"
        #     print("*************")
        #     print("entry added")
        #     print("*************")

        # if "@Hostname@" in data:
        #     data = splitIdentifier(data);
        #     Hostname = data;
        # elif "@Organization ID@" in data:
        #     data = splitIdentifier(data);
        #     OrganizationId = data;
        # elif "@IP Address@" in data:
        #     data = splitIdentifier(data);
        #     IPAddress = data;
        # elif "@Default Gateway@" in data:
        #     data = splitIdentifier(data);
        #     DefaultGateway = data;
        # elif "@MAC Address@" in data:
        #     data = splitIdentifier(data)
         #     MACAddress = data;
        # elif "Download/Upload" in data:
        #     data = data.split("{")
        #     data = data[1].split("}")
        #     data = data[0].split(",")
        #     upload = data[0]
        #     upload = upload.split("B")
        #     upload = upload[0]
        #     upload = float(upload) * 8
        #     upload = upload / 1000000
        #     # upload = (upload * 8000000)
        #     download = data[0]
        #     download = download.split("B")
        #     download = download[0]
        #     download = float(download) * 8
        #     download = download / 1000000
        #     # download = (download * 8000000)
        #     print(str(upload) + "Mbit/s is upload")
        #     print(str(download) + "Mbit/s is download")

        #else:
            #overall bandwidth
            #handle_message(data)
    conn.close()



while 1:
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(clientthread, (conn,))

