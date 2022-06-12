from encodings import utf_8
from socket import *
import time
import subprocess
from .utils import print_str_map

from Serialisation import serialize, deserialize
import signal
import os


PID = None


class Network():
    def __init__(self, map, createur, servip):
        self.createur = createur
        self.map = map
        self.not_ready = True
        self.newmap = []
        


        if self.createur:
            PORT = 5000
        else:
            PORT = 5002
        ADDR = "127.0.0.1"
        listeningAddr = (ADDR, PORT)


        print('je tente de bind')
        self.sockfd = socket(AF_INET, SOCK_DGRAM)
        self.sockfd.bind(listeningAddr)
        self.sockfd.setblocking(0)

        msg_connect = "/connect"
        msg_map = "/askmap"
        

        

        if self.createur:
            process = subprocess.Popen(['./socketenc_main', '/'], shell=True)
        else:
            process = subprocess.Popen(['./socketenc_2 ' + str(servip), '/'], shell=True)

        global PID
        PID = int(process.pid)
        signal.signal(signal.SIGINT, self.quit_c)
        time.sleep(1)

        if self.createur:
            self.serverAddr = ("127.0.0.1", 5001)
        else:
            self.serverAddr = ("127.0.0.1", 5003)
        print('sending to serv: ' + str(self.serverAddr))
        self.sockfd.sendto(msg_connect.encode("utf8"), self.serverAddr)
        



    def listen(self):
        try:
            data = self.sockfd.recvfrom(128)[0]
            data = data.decode("utf8")
            data = data[:-1]
            print("received message: " + str(data))
            if data == "/askmap":
                map_list = self.map.stra_map
                #print_str_map(map_list)
                for ligne in map_list:
                    print(str(ligne))
                    msg_send_map = "/sendmap " + str(ligne)
                    self.send_action(msg_send_map)
                self.send_action("/endmap")
            elif data[:8] == "/sendmap":
                self.newmap.append(str(data[9:]))
            elif data[:7] == "/endmap":
                print_str_map(self.newmap)
                self.not_ready = False
            else:
                deserialize(data, self.map)
        except BlockingIOError:
            pass
    
    

    def send_action(self, action):
        self.sockfd.sendto(action.encode("utf-8"), self.serverAddr)
        print('action envoyé: ' + str(action))


    def quit_c(self, numero, frame):
        global PID
        os.kill(PID + 1, numero)
        exit()