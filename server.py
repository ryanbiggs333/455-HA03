server.pyimport socket
import os
host = "127.0.0.1"
port = 4560

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
print(f"Server listening on {host}:{port}")

def handle_file_transfer(conn, file_name):
    new_file_name = f"server_copy_{file_name}"  
    with open(new_file_name, 'wb') as f:
        while True:
            data = conn.recv(4096)
            if data.endswith(b"EOF"):
                f.write(data[:-3])
                break  # End of file
            f.write(data)
    print(f"File {file_name} received successfully.")

    conn.send(f"FILE: {file_name}".encode('utf-8'))
    with open(new_file_name, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            conn.send(data)
    conn.send(b'EOF')  # Send end-of-file marker
    print(f"Copy of file {file_name} sent back to client successfully.")

while True:
    try:
        conn, addr = server.accept()
        print(f"New connection from {addr}")
        while True:
            message = conn.recv(4096).decode('utf-8')
            if message.startswith("FILE: "):
                file_name = message[6:]
                print(f"Receiving file: {file_name}")
                handle_file_transfer(conn, file_name)
            elif message:
                print()  # add newline
                print(f"{addr}: {message}")  # show client's message

                response = f"echo \"{message}\""
                conn.send(response.encode('utf-8'))  # send response to client
                print(f"me: {response}")  # show server's response
            else:
                conn.close()
                print('No message from client')
                break
            print() # add newline
    except Exception as e:
        print(f"Error: {e}")
        break
