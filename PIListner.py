from socket import *
from gpiozero import LED, Buzzer
from time import sleep

led = LED(27)
buzzer = Buzzer(17)

port = 12100
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', port))

while True:
    response, server_address = s.recvfrom(65507)
    decoded = response.decode()
    print(decoded)
    if decoded == 'ok':
        led.on()
        buzzer.on()
        sleep(0.2)
        led.off()
        buzzer.off()
