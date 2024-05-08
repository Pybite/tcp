import threading
import socket
# Input any HOST IP and PORT
HOST: str = 'LOCALHOST'
PORT: int = 9595

ct = []
n = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

s.listen(3)
print(f"listening on {HOST}", '\n')

def broadcast(msg):
    for x in ct:
        x.send(msg)

def handler(client):
    while True:
        try:
           msg = client.recv(1024)
           broadcast(msg)
           
        except:
           i = ct.index(client)
           ct.remove(client)
           client.close()
           usr = n[i]
           broadcast(f"{usr} has left ...".encode('utf-8'))
           n.remove(usr)
           break


def r():
    while True:
        client, addr = s.accept()
        print(f"Connected: {addr}", '\n')

        client.send('TRUE'.encode('utf-8'))
        m = client.recv(1024).decode('utf-8')

    
        ct.append(client)
        n.append(m)
        print(f"{addr[0]} is now {m}", '\n')

        broadcast(f"{m} joined the room ...".encode('utf-8'))

        client.send('Connected to the server'.encode('utf-8'))

        t = threading.Thread(target=handler, args=(client,))
        t.start()

r()


