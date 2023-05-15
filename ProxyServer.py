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

REST_URL = "http://localhost:5093/api/arrivals"
UDP_IP = "255.255.255.255"

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = ('', serverPort)
serverSocket.bind(serverAddress)

resport = 12100
respSocket = socket(AF_INET, SOCK_DGRAM)
Piservername = '192.168.104.140'

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
            "arrivalTime": ArrivalTime,
            "qrCode": id,
            "name": ''
        }
        print(id)
        print(ArrivalTime)
        response = requests.post(REST_URL, json=data)
        print(response)
        if response.ok:
            responseOK = 'ok'
            respSocket.sendto(responseOK.encode(),(Piservername, resport))
        if response.status_code == 400:
            responseBadR = '400 Bad request'
            print('400 Bad request.....')
            respSocket.sendto(responseBadR.encode(), (Piservername, resport))

        count += 1
    except:
        print('Not a qr code')
        response = 'not a QR code'
        respSocket.sendto(response.encode(), (Piservername, resport))


