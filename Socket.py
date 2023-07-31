#SOCKET PROGRAMMING
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)
print('The server is ready to produce items')

client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)

items = ['student1', 'student2', 'student3', 'student4', 'student5', 'student6', 'student7', 'student8', 'student9', 'student10']
for item in items:
    client_socket.send(item.encode())
    print('Producing:', item)

client_socket.close()
server_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
print('Connected to the server')

while True:
    client_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    item = client_socket.recv(1024).decode()
    if not item:
        break
    print('Consuming:', item)

client_socket.close()