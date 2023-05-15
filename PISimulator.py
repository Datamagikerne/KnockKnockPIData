from time import sleep
from socket import *
from os import listdir
from os.path import isfile, join
from pathlib import Path
print(Path.cwd())
mypath = "C:/Users/olivi/PytonProjects/KnockKnockPI/test_images/"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for filename in onlyfiles:
    print(filename)
broadcastport = 12000
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    index = 0
    while index < 3:
        sleep(4)
        print(onlyfiles[index])
        file = open(mypath + onlyfiles[index], 'rb')
        file_data = file.read(65507)
        while file_data:
            print('sending')
            s.sendto(file_data, ('<broadcast>', broadcastport))
            file_data = file.read(65507)
        file.close()
        print('done')
        index += 1
