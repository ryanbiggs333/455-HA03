import socket
host = "127.0.0.1"
port = 4560

def send_message(client_socket):
    user_input = input()
    if user_input.startswith("FILE: "):
        file_name = user_input[6:]
        client_socket.send(f"FILE: {file_name}".encode('utf-8'))
        with open(file_name, 'rb') as f:                     
            while True:
                data = f.read(4096)
                if not data:
                    break
                client_socket.send(data)
        
        client_socket.send(b"EOF")  # Send end-of-file marker
        print(f"File {file_name} sent successfully.")
    else:
        client_socket.send(user_input.encode('utf-8'))

def receive_response(client_socket):
    response = client_socket.recv(4096).decode('utf-8')
    if response.startswith("FILE: "):
        file_name = response[6:]
        new_file_name = f"client_copy_{file_name}" 
        with open(new_file_name, 'wb') as f:
            while True:
                data = client_socket.recv(4096)
                if data.endswith(b'EOF'):
                    f.write(data[:-3])  # Write all but the last 3 bytes (EOF marker)
                    break
                f.write(data)
        print(f"Copy of file {file_name} received from server successfully.")
    else:
        print(f"server: {response}")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        send_message(client_socket)
        receive_response(client_socket)
        print() # add newline

if __name__ == "__main__":
    start_client()
