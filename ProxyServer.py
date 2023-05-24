#Recieve images from raspberry PI
#saves images and looks for QRCode
#sends data to Rest
#sends reponse back to Raspberry PI
import requests
from socket import *
from pyzbar.pyzbar import decode
import cv2

REST_URL = "https://knockknockrestapi.azurewebsites.net/api/arrivals"

#Server socket recieves data from PI
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = ('', serverPort)
serverSocket.bind(serverAddress)

#respSocket sends reponse from Rest to PI
resport = 12100
respSocket = socket(AF_INET, SOCK_DGRAM)
Piservername = '192.168.104.140'
testServername = '127.0.0.1'

print("The server is ready")
count = 1


def recieve_img():
    file = open(f'c:/temp/qr{count}.jpg', 'wb')
    filedata, clientAddress = serverSocket.recvfrom(65507)
    print("Receiving...")
    file.write(filedata)
    file.close()


def get_data():
    img = cv2.imread(f'c:/temp/qr{count}.jpg')
    student_id = decode(img)[0].data.decode('utf-8')
    data = {
        "qrCode": student_id,
        "name": "string"
    }
    print('QR-code data: ' + id)
    return data


def get_response(rest_response):
    if rest_response.ok:
        responseOK = 'ok'
        print((responseOK))
        respSocket.sendto(responseOK.encode(), (Piservername, resport))
        respSocket.sendto(responseOK.encode(), (testServername, resport))
    if rest_response.status_code == 400:
        responseBadR = '400 Bad request'
        print(responseBadR)
        respSocket.sendto(responseBadR.encode(), (Piservername, resport))
        respSocket.sendto(responseBadR.encode(), (testServername, resport))


while True:
    recieve_img()
    try:
        response = requests.post(REST_URL, json=get_data())
        get_response(response)
        count += 1
    except:
        response = 'not a QR code'
        print(response)
        respSocket.sendto(response.encode(), (Piservername, resport))
        respSocket.sendto(response.encode(), (testServername, resport))

