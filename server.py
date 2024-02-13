import socket
import threading

# Dictionary เพื่อเก็บ client_address เป็น key และชื่อของ client เป็น value
connected_users = {}

# ฟังก์ชันสำหรับการจัดการ client แต่ละตัว
def handle_client(client_socket, client_address):
    num_input_name = 1
    while True:
        # รับ input จาก client
        client_input = client_socket.recv(1024).decode()
        
        # ตรวจสอบว่า client ต้องการจะส่งชื่อของตัวเองหรือไม่
        if num_input_name == 1 and client_input:
            client_socket.send(('Name received by server: {}'.format(client_input)).encode())
            # ส่งชื่อของ client กลับไปยัง client
            connected_users[client_address] = client_input
            print('User {} has joined.'.format(connected_users[client_address]))
            num_input_name = 0
        else:
            # ถ้า client ส่งข้อความ 'exit' ให้หยุดการรับข้อมูล
            if client_input.lower() == 'exit':
                print('User {} is exit'.format(connected_users[client_address], client_input))
                break
            
            if client_input.lower() == 'list':
                # print(list(connected_users.values()))
                connected_users_str = "{}".format(list(connected_users.values()))
                client_socket.send(connected_users_str.encode())
            elif client_input.lower() == 'my name':
                connected_users_str = "{}".format(connected_users[client_address])
                client_socket.send(connected_users_str.encode())
            else:
                print('{}: {}'.format(connected_users[client_address], client_input))
                client_socket.send(("status ok/200").encode())
            
            
            
    
    # ลบข้อมูลของ client ออกจาก dictionary เมื่อ client ปิดการเชื่อมต่อ
    del connected_users[client_address]
    
    # ปิดการเชื่อมต่อ
    client_socket.close()

# สร้าง socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ระบุ host และ port
host = '127.0.0.1'
port = 12345

# Bind address และ port กับ server
server_socket.bind((host, port))

# จำกัดการเชื่อมต่อได้เป็น 5 client พร้อมกัน
server_socket.listen(5)

print('Server listening on {}:{}'.format(host, port))

while True:
    # รอการเชื่อมต่อจาก client
    client_socket, client_address = server_socket.accept()
    
    # เริ่ม thread ใหม่สำหรับการจัดการ client แต่ละตัว
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
