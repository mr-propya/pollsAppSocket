import socket
import threading
import sockets
import json


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.callback = None
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("constructor done")

    def validateLogin(self):
        password = input("Enter password")
        req = sockets.createMessage(password, sockets.SOCKET_REQUEST[0])
        self.socket.send(req.encode("utf-8"))
        res = json.loads(self.socket.recv(1024).decode("utf-8"))
        return res["type"] == sockets.SOCKET_REQUEST[1]

    def attachSocket(self, callback=None):
        self.callback = callback
        self.socket.connect((self.ip, 5000))
        if self.validateLogin():
            threading.Thread(target=self.keepListeningMsg).start()
        else:
            print("Invalid passwords")
            self.socket.send(sockets.createMessage(sockets.SOCKET_REQUEST[2], sockets.SOCKET_REQUEST[4]).encode("utf-8"))



    def keepListeningMsg(self):
        print("started listening")
        while True:
            msg = self.socket.recv(1024).decode("utf-8")
            print("message from thread")
            msg = json.loads(msg)
            self.callback(msg)
            # msg=msg['msg']
            # print('Question: {}'.format(msg['question']))
            # for i in range(len(msg['options'])):
            #     print('{}: {}'.format(i,msg['options'][i]))


    def sendMsgServer(self, msg=None):
            print(msg)
            self.socket.send(msg)


def main():
    Client("192.168.43.47", 5000).attachSocket()


if __name__ == "__main__":
    main()
