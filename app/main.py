import socket
import threading
from .parser import RedisParser

def simple_redis_serializer(data):
    if data == None:
        return "$-1\r\n"
    if type(data) == int:
        return f":{str(int)}\r\n"
    return f"${len(data)}\r\n{data}\r\n"

def handle_request(connection):
    redis_parser = RedisParser()
    db = {}
    while True:
        data = connection.recv(1024)
        data = data.decode().lower()
        data = redis_parser.parse(data)
        if data[0] == 'ping':
            response = "+PONG\r\n"
            connection.sendall(response.encode())
        if data[0] == 'echo':
            response = simple_redis_serializer(data[-1])
            connection.sendall(response.encode())
        if data[0] == 'set':
            _, key, value = data
            db[key] = value
            response = "+OK\r\n"
            connection.sendall(response.encode())
        if data[0] == 'get':
            _, key = data
            value = db.get(key, None)
            response = simple_redis_serializer(value)
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
