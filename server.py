import socket
import threading
import sockets
import hashlib


class Server:
    def __init__(self, port, callBack=None, passwd="abc"):
        self.connections = list()
        self.threads = list()
        self.port = port
        self.passwd = passwd
        self.callBack = callBack
        self.server = socket.socket()
        t = threading.Thread(target=self.startListening)
        t.start()

    def startListening(self):
        print("listening ", self.port)
        self.server.bind(("", self.port))
        self.server.listen(5)
        while True:
            print("attach")
            c, addr = self.server.accept()
            print(addr)
            t = threading.Thread(target=self.handleSocket, args=(c, addr))
            t.start()
            self.connections.append([c, addr, False])
            self.threads.append((t, addr))

    def handleSocket(self, soc, address):
        while True:
            try:
                msg = soc.recv(1024).decode("utf-8")
                dataPacket = {"message": msg }
                dataPacket["ip"] = address
                self.callBack(dataPacket)
            except:
                print("User {} has left the group".format(address))
                try:
                    self.connections.remove([soc, address, True])
                except:
                    self.connections.remove([soc, address, False])

                break
            if msg == "exit)(":
                soc.close()
                break
            msg = "message is {} from ip {}".format(msg, address)
            # self.broadCastMsg(msg)

    def broadCastMsg(self, msg):
        print("broadcastinf ", len(self.connections))
        for s, add, verified in self.connections:
            print(add)
            print(verified)
            if not verified:
                continue
            try:
                s.send(msg.encode("utf-8"))
                print("sent msg: {} to :{}".format(msg, add))
            except Exception as e:
                print(e)
                print("exception")
                pass

    def validate(self, to, isValid):
        for i in range(len(self.connections)):
            if self.connections[i][1] == to:
                self.connections[i][2] = isValid
                token = ""
                msg = sockets.createMessage(token, sockets.SOCKET_REQUEST[2])
                if isValid:
                    msg = sockets.createMessage(token, sockets.SOCKET_REQUEST[1])
                print(sockets.SOCKET_REQUEST)
                print(sockets.SOCKET_REQUEST[0])
                print(sockets.SOCKET_REQUEST[1])
                print("validation \n\n\n {} \n\n\n".format(msg))

                self.connections[i][0].send(msg.encode("utf-8"))
                break

    def disconnect(self, to):
        for i in range(len(self.connections)):
            if self.connections[i][1] == to:
                self.threads[i][0].join()
                self.connections[i][0].close()
                break

def sendMessages():
    while True:
        msg = input("enter msg")
        print(msg)
        ser.broadCastMsg(msg)


ser = None



def main():
    global ser
    ser = Server(500)
    threading.Thread(target=sendMessages).start()


if __name__ == '__main__':
    main()
