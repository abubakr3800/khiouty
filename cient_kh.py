from socket import *
import threading

#sign in DNS server

name = 'a'
my_ip = '192.168.1.9'
rec_port = 9700

serverName = '192.168.1.9'
serverPort = 9900

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send((name+':'+str(rec_port)).encode())

# Server Reply
reply = clientSocket.recv(1024)
print('From Server: ', reply.decode())
clientSocket.close()

#send message

def sending():
    user = input('to : ')
    message = input('a : ')
    
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(user.encode())
    reply = clientSocket.recv(1024)
    users_ip = list((reply.decode()).split(','))
    clientSocket.close()
    
    for ip in users_ip:
        
        ipp = list((ip).split(':'))
        if ipp[0] == my_ip:
            continue
            
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((ipp[0],int(ipp[1])))
        
        clientSocket.send((name+message).encode())
        clientSocket.close()
    sending()
        
def reciving():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((my_ip, rec_port))
    serverSocket.listen(3)
    while True:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024).decode()
        print(sentence[0]+' : '+sentence[1:]+'\n')
        connectionSocket.close()

t1= threading.Thread(target = sending,daemon=True)
t1.start()
reciving()