import socket
import os

def receive_file_name(client_socket):
    # 接收文件名（假设文件名不超过1024字节）
    file_name = client_socket.recv(1024).decode('utf-8')
    
    # 避免重复
    base, extension = os.path.splitext(file_name)
    counter = 1
    while os.path.exists(file_name):
        file_name = f"{base}_{counter}{extension}"
        counter += 1
    
    print(f"Receiving file: {file_name}")
    return file_name

def receive_file(write_path, client_socket):
    current_directory = os.getcwd()
    write_path = os.path.join(current_directory, write_path)
    with open(write_path, 'wb') as file:
        while True:
            bytes_read = client_socket.recv(1024)
            if not bytes_read:
                break
            file.write(bytes_read)
    print("File has been received.")

def client_program():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Send the file name to the server
    file_name = input("Enter the file name to receive: ")
    client_socket.sendall(file_name.encode())
    
    # Receive the file
    write_path = receive_file_name(client_socket)
    receive_file(write_path, client_socket)

    client_socket.close()

if __name__ == '__main__':
    client_program()