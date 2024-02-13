import socket

# สร้าง socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ระบุ host และ port ของ server
host = '127.0.0.1'
port = 12345

# เชื่อมต่อกับ server
client_socket.connect((host, port))

print('Connected to server at {}:{}'.format(host, port))

# Input ชื่อของตัวเอง
client_name = input("Enter your name: ")

# ส่งชื่อของตัวเองไปยัง server
client_socket.send(client_name.encode())

# รับข้อความยืนยันจาก server
server_response = client_socket.recv(1024).decode()
print('Server response:', server_response)

while True:
    client_input = input("input: ")
    
    client_socket.send(client_input.encode())
    
    if client_input.lower() == 'exit':
        break
    
    server_response = client_socket.recv(1024).decode()
    print('Server response:', server_response)

# ปิดการเชื่อมต่อ
client_socket.close()
