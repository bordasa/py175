import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 3003))
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
    http_method, full_path, htttp_version = request_line.split()
    
    if '?' in full_path:
        path = full_path[: full_path.index('?')]
        params_str = full_path[full_path.index('?') + 1: ]
        key_value_pairs = params_str.split('&')
        params = {key: value for key, value in
                    [pair.split('=') for pair in key_value_pairs]}
    
    else:
        path = full_path
        params = {'rolls': '1', 'sides': '6'}

    response_body = f"{request_line}\n"

    for count in range(int(params['rolls'])):
        roll = random.randint(1, int(params['sides']))

        response_body += f"Roll #{count + 1}: {roll}\n"

    response = ("HTTP/1.1 200 OK\r\n"
               "Content-Type: text/plain\r\n"
               f"Content-Length: {len(response_body)}\r\n"
               "\r\n"
               f"{response_body}\n")
    
    client_socket.sendall(response.encode())
    client_socket.close()