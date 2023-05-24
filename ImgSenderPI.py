# runs on PI
from PIL import Image
from time import sleep
from picamera import PiCamera
from socket import *
from gpiozero import Button

my_path = '/home/pi/Desktop'
img_name = 'qr.jpg'
BROADCAST_TO_PORT = 12000
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

camera = PiCamera()
camera.resolution = (320, 240)
camera.color_effects = (128, 128)
button = Button(2)


def take_img():
    camera.start_preview()
    sleep(3)
    camera.capture(img_name)
    camera.stop_preview()


while True:
    button.wait_for_press()
    take_img()
    image = Image.open(img_name)
    compressed_img_name = 'qrcompressen.jpg'
    image.save(compressed_img_name, optimize=True, quality=10)
    file = open(my_path + compressed_img_name, 'rb')
    file_data = file.read(65507)
    while file_data:
        print('sending')
        s.sendto(file_data, ('<broadcast>', BROADCAST_TO_PORT))
        file_data = file.read(65507)
    file.close()
    print('Done')

