import socket
from _datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
asset = open("data/data.txt", "r")
lines = asset.readlines()
cred = credentials.Certificate('./LogHub.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def splitIdentifier(data):
    d = data.split("{")
    data = d[1].split("}")
    return data[0]
def convertToTime(date , time , sunormoon):
    sunormoon = sunormoon.split(":")
    newTime = datetime.strptime(" " + time + " " + sunormoon[0] + " " + date, ' %I:%M:%S %p %d/%m/%Y')
    return newTime

def uploadIntoDBIndBW(hostname , time , organization , upload , download):

    document_ref = db.collection(u'IndBW').document()
    document_ref.set({
        u'hostname': hostname,
        u'organizationId': organization,
        u'time': time,
        u'upload': upload,
        u'download': download
    })
    print("Successfully Updated")
#
# for data in lines:
#     if "@Hostname@" in data:
#         data = splitIdentifier(data);
#         Hostname = data;
#     elif "@Organization ID@" in data:
#         data = splitIdentifier(data);
#         OrganizationId = data;
#     elif "@IP Address@" in data:
#         data = splitIdentifier(data);
#         IPAddress = data;
#     elif "@Default Gateway@" in data:
#         data = splitIdentifier(data);
#         DefaultGateway = data;
#     elif "@MAC Address@" in data:
#         data = splitIdentifier(data)
#         MACAddress = data;
#     elif "Download/Upload" in data:
#         data = data.split(" ")
#         bwHostname = data[0]
#         time = convertToTime(data[1] , data[2], data[3])
#         organization = data[4].split(":")
#         organization = organization[0]
#         data = data[5]
#         data = data.split("{")
#         data = data[1].split("}")
#         data = data[0].split(",")
#         upload = data[0]
#         upload = upload.split("B")
#         upload = upload[0]
#         upload = float(upload) * 8
#         upload = upload / 1000000
#         # upload = (upload * 8000000)
#         download = data[0]
#         download = download.split("B")
#         download = download[0]
#         download = float(download) * 8
#         download = download / 1000000
#         # download = (download * 8000000)
#         uploadIntoDBIndBW(bwHostname , time ,organization ,  upload , download)
#         print(str(upload) + "Mbit/s is upload")
#         print(str(download) + "Mbit/s is download")
#     # if MACAddress is not "-1" and DefaultGateway is not "-1" and IPAddress is not "-1" and OrganizationId is not "-1" and Hostname is not "-1":
#     #     addEntryToHostMapping(Hostname, OrganizationId, IPAddress, DefaultGateway, MACAddress)
#     #     MACAddress = "-1"
#     #     DefaultGateway = "-1"
#     #     IPAddress = "-1"
#     #     OrganizationId = "-1"
#  #     Hostname = "-1"


document_ref = db.collection(u'HostMapping').document("SHAMISEN")
print(document_ref.get())