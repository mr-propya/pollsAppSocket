import server
import client
import json
import hashlib
import time
import threading

isServer = False
serverInstance = None
clientInstance = None
passwd = ""
sleepTime = 30
results = {}

SOCKET_REQUEST = ("JOIN_REQ", "JOIN_ACK", "JOIN_NAK", "MESSAGE", "EXIT")


def createMessage(msg, request):
    result = dict()
    result["msg"] = msg
    result["type"] = request
    h = hashlib.sha1(json.dumps(result).encode("utf-8"))
    result["checkSum"] = h.hexdigest()
    print(h.hexdigest())
    return json.dumps(result)


def clientCallback(msg):
    index = msg["type"]
    index = SOCKET_REQUEST.index(index)
    if index == 3:
        pass
    print(msg)
    displayMessage(json.loads(msg["msg"]))


def callback(msgDict):
    message = json.loads(msgDict["message"])
    reqType = SOCKET_REQUEST.index(message["type"])
    if reqType == 0:
        authenticated = False
        if passwd == message["msg"]:
            authenticated = True
        print(msgDict, authenticated)
        serverInstance.validate(msgDict["ip"], authenticated)

    if reqType == 3: #message
        ans = json.loads(message["msg"])["ans"]
        print(ans)
        if results.__contains__(ans):
            results[ans] += 1
        else:
            results[ans] = 1
        print(msgDict["ip"])
    if reqType == 4: #exit
        serverInstance.disconnect(msgDict["ip"])


def startServer():
    global passwd
    passwd = input("Set Room's password")
    global serverInstance
    serverInstance = server.Server(5000, callBack=callback)


def startClient():
    ip = input("Enter IP")
    global clientInstance
    clientInstance = client.Client(ip, 5000)
    clientInstance.attachSocket(callback=clientCallback)


options = []


def showResults():
    for k in range(len(options)):
        count = 0
        if results.__contains__(k+1):
            count = results[k+1]
        print("{} : {}".format(options[k], count))


def createQuestion():
    showResults()
    options.clear()
    results.clear()
    input("Start polls")
    qn = input('Enter your question here: ')
    opts = int(input('Enter no. of options: '))
    for i in range(0, opts):
        options.append(input('Option {}: '.format(i+1)))
    question = {'question': qn, 'options': json.dumps(options)}
    print(json.dumps(question))
    return json.dumps(question)


def startQuestion():
    while True:
        question=createQuestion()
        question=createMessage(question,SOCKET_REQUEST[3])
        global serverInstance
        serverInstance.broadCastMsg(question)
        time.sleep(sleepTime)


def displayMessage(message):
    print('Q.) {}'.format(message["question"]))
    for i in (json.loads(message["options"])):
        print('{}: {}'.format(json.loads(message["options"]).index(i)+1,i))
    ans = int(input("Enter your choice"))
    ans = {"ans":ans}
    clientInstance.sendMsgServer(createMessage(json.dumps(ans),SOCKET_REQUEST[3]).encode("utf-8"))



def main():
    # listening = server.Server(500)
    # listening.startListening()
    # print("asas")
    # import time
    # time.sleep(2)
    # print("connecting")
    # client.Client("localhost", 500).attachSocket()
    global isServer
    isServer = (input("Is Server?Y") == 'Y')
    if isServer:
        startServer()
        threading.Thread(target=startQuestion).start()
    else:
        startClient()
    # print(createMessage("assasa", "asa"))


if __name__ == '__main__':
    main()
