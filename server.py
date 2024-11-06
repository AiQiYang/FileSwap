import socket
import os

def send_file(file_path, client_socket):
    with open(file_path, 'rb') as file:
        # 获取文件名
        file_name = os.path.basename(file_path)
        # 发送文件名
        client_socket.sendall(file_name.encode('utf-8'))
        
        bytes_read = file.read(1024)
        while bytes_read:
            client_socket.sendall(bytes_read)
            bytes_read = file.read(1024)
    print("File has been sent.")

def server_program():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server is listening on port:", port)

    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    
    # Receive the file name from the client
    file_name = conn.recv(1024).decode()
    print(f"Client requested file: {file_name}")
    
    # Check if the file exists
    if os.path.exists(file_name):
        send_file(file_name, conn)
    else:
        print("File does not exist.")
    
    conn.close()
    server_socket.close()

if __name__ == '__main__':
    server_program()