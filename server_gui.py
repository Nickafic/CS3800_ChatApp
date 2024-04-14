import socket
import threading

SERVER_IP = 'localhost'
PORT = 12345
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):

    print(f"[NEW CONNECTION] Connected.")

    connected = True
    while connected:
        try:
            message = client.recv(1024)
            if message == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            break

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{PORT}")
    while True:
        if len(clients) < 10:
            client, addr = server.accept()
            clients.append(client)

            print(f"[CONNECTION] {addr} connected.")

            broadcast(f"\nNew user joined the chat!".encode(FORMAT))
            client.send('\nConnected to the server!'.encode(FORMAT))

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        else:
            print("[FULL] The server is full. Please try again later.")

if __name__ == "__main__":
    start()
