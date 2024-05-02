import socket
import threading
import ssl

SERVER_IP = 'localhost'
PORT = 12345
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

# Set up SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')  # Adjust the paths to your certificate and key

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def broadcast(message, exception_client=None):
    """Send a message to all clients except the sender (exception_client)."""
    for client in clients:
        if client != exception_client:
            try:
                client.send(message.encode(FORMAT))
            except Exception as e:
                print(f"Error sending message: {e}")

def handle_client(client):
    """Handles a new client connection."""
    try:
        username = client.recv(1024).decode(FORMAT)  # Expect the first message to be the username
        welcome_message = f"{username} has joined the chat!"
        broadcast(welcome_message, exception_client=client)  # Notify all other clients
        client.send("Connected to the server!".encode(FORMAT))  # Welcome the new client

        while True:
            message = client.recv(1024).decode(FORMAT)
            if message == "{quit}":
                break
            broadcast(f"{username}: {message}", exception_client=client)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        clients.remove(client)
        client.close()
        leave_message = f"{username} has left the chat."
        broadcast(leave_message)  # Notify all clients that the user has left
        print(f"[DISCONNECTED] {username} disconnected.")

def start():
    """Starts the server."""
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        print(f"[CONNECTION] {addr} connected.")
        # Wrap the client's socket with server's SSL context
        client = context.wrap_socket(client_socket, server_side=True)
        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    start()
