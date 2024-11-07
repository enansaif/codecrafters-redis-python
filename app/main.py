import socket


def main():
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.listen(5)

    while True:
        client_socket, _ = server_socket.accept()
        message = "+PONG\r\n".encode()
        client_socket.sendall(message)
        client_socket.close()

if __name__ == "__main__":
    main()
