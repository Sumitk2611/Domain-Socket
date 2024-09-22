import socket
import os


def content_retriever(filepath):
    content = open(filepath, "r")
    return content.read()

def unbind(socketPath):
    try:
        os.unlink(socketPath)
    except OSError:
        if os.path.exists(socketPath):
            print("Socket path is being used")
            exit(0)

def accept(s):
    try: 
        connection, clientaddr = s.accept()
        return connection
    except socket.error as e:
        print(e)
        exit(0)

def cleanup(connection, socketpath):
    connection.close()
    os.unlink(socketpath)

def bind(sk, path):
    try:
        sk.bind(path)
    except socket.error as e:
        print(e)
        exit(0)

def listen(sk):
    try:
        sk.listen(1)
    except socket.error as e:
        print(F"Socket unable to listen {e}")
        exit(0)

def recv(connection):
    try:
        data = connection.recv(1024)
        return data
    except socket.error as e:
        print(e)
        exit(0)

def send(connection, data):
    try:
        connection.sendall(str.encode(data))
    except socket.error as e:
        print(f"Unable to send data {e}")
        connection.close()

def main():
    socketpath = "/tmp/socket"
    unbind(socketpath)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print("Socket Created")

     
    bind(s, socketpath)
    listen(s)
    

    try:
        while True:
            print("Waiting for Connection")
            if(s): 
                connection = accept(s)
            while True:
                data = recv(connection)
                if data:
                    print("File to read: {!r}".format(data.decode()))

                        #check if file exists
                    if not os.path.isfile(data.decode()):
                        send(connection,"FILE DOES NOT EXIST")
                        continue

                    print("Retrieving Content")

                        #send file size
                    file_size = os.path.getsize(data.decode())
                    send(connection,str(file_size))

                    #read and send back data
                    with open(data.decode(),'r') as file:
                        while chunk := file.read(1024):
                            send(connection,chunk)
                        
                else:
                    print('No more requests\n')
                    break

    except KeyboardInterrupt:
        print("Shutting Server")
        os.unlink(socketpath)
        exit(0)

main()