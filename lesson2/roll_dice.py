import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 3001))
server_socket.listen()

print("Server is running on localhost:3003")

while True:
    client_socket, addr = server_socket.accept()
    print(F"Connection from {addr}")
    request = client_socket.recv(1024).decode()

    if (not request) or ('favicon.ico' in request):
        client_socket.close()
        continue

    request_line = request.splitlines()[0]
    http_method, full_path, htttp_version = request_line.split(" ")

    params_dict = {}
    
    if "?" in full_path:
        path, params_str = full_path.split("?")
        key_value_pairs = params_str.split('&')
    
        for pair in key_value_pairs:
            key, value = pair.split("=")
            params_dict[key] = value
    
    else:
        path = full_path
    
    rolls = int(params_dict.get('rolls', '1'))
    sides = int(params_dict.get('sides', '6'))

    response_body = (f"RequestLine: {request_line}\n"
                     f"HTTP Method: {http_method}\n"
                     f"Path: {path}\n"
                     f"Parameters: {params_dict}\n")

    for count in range(rolls):
        roll = random.randint(1, sides)

        response_body += f"Roll #{count + 1}: {roll}\n"

    response = ("HTTP/1.1 200 OK\r\n"
               "Content-Type: text/plain\r\n"
               f"Content-Length: {len(response_body)}\r\n"
               "\r\n"
               f"{response_body}\n")
    
    client_socket.sendall(response.encode())
    client_socket.close()