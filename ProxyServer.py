#Recieve images from raspberry PI
#saves images and looks for QRCode
#sends data to Rest
#sends reponse back to Raspberry PI
import requests
import datetime
import pytz
from socket import *
from pyzbar.pyzbar import decode
import cv2

REST_URL = "https://knockknockrest2.azurewebsites.net/api/arrivals"
UDP_IP = "255.255.255.255"

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = ('', serverPort)
serverSocket.bind(serverAddress)

resport = 12100
respSocket = socket(AF_INET, SOCK_DGRAM)
Piservername = '192.168.104.140'
testServername = '127.0.0.1'

print("The server is ready")
count = 1
cet = pytz.timezone('CET')
while True:
    file = open(f'c:/temp/qr{count}.jpg', 'wb')
    filedata, clientAddress = serverSocket.recvfrom(65507)
    print(clientAddress)
    print("Receiving...")
    file.write(filedata)
    file.close()
    try:
        img = cv2.imread(f'c:/temp/qr{count}.jpg')
        id = decode(img)[0].data.decode('utf-8')
        ArrivalTime = datetime.datetime.now(cet).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "id": 0,
            "arrivalTime": ArrivalTime,
            "qrCode": id,
            "name": "string"
        }
        print(id)
        print(ArrivalTime)
        response = requests.post(REST_URL, json=data)
        # print(response.text)
        if response.ok:
            responseOK = 'ok'
            print((responseOK))
            respSocket.sendto(responseOK.encode(), (Piservername, resport))
            respSocket.sendto(responseOK.encode(), (testServername, resport))
        if response.status_code == 400:
            responseBadR = '400 Bad request'
            print(responseBadR)
            respSocket.sendto(responseBadR.encode(), (Piservername, resport))
            respSocket.sendto(responseBadR.encode(), (testServername, resport))

        count += 1
    except:
        print('Not a qr code')
        response = 'not a QR code'
        respSocket.sendto(response.encode(), (Piservername, resport))
        respSocket.sendto(response.encode(), (testServername, resport))



