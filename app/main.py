import socket
import threading
from .parser import RedisParser

def simple_redis_serializer(s):
    return f"${len(s)}\r\n{s}\r\n"

def handle_request(connection):
    redis_parser = RedisParser()
    while True:
        data = connection.recv(1024)
        data = data.decode().lower()
        data = redis_parser.parse(data)
        if type(data) == list and data[0] == 'ping':
            response = "+PONG\r\n"
            connection.sendall(response.encode())
        if type(data) == list and data[0] == 'echo':
            response = simple_redis_serializer(data[-1])
            connection.sendall(response.encode())

def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_request, args=[client_socket])
        thread.start()

if __name__ == "__main__":
    main()
