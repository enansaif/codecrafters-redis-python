import socket
import threading

def handle_request(connection):
    response = "+PONG\r\n".encode()
    with connection:
        connected = True
        while connected:
            data = connection.recv(512)
            data_str = data.decode().lower()
            if "ping" in data_str:
                connection.sendall(response)

def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_request, args=[client_socket])
        thread.start()

if __name__ == "__main__":
    main()
