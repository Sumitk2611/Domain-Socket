import socket
import sys


def printContent(filename, data):
    print("\nFilename: ", filename)
    print("Content:\n ", data)
    return

def connect(sk, path):
    try:
        sk.connect(path)
    except socket.error as e:
        print(f"Unable to connect. Error: {e}")
        exit(0)

def send(sk, data):
    try:
        sk.sendall(str.encode(data))
    except socket.error as e:
        print(f"Unable to send data {e}")
        sk.close()

def recv(sk):
    try:
        data = sk.recv(1024)
        return data
    except socket.error as e:
        print(e)
        exit(0)

def main():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    socketpath = "/tmp/socket"

    allfiles = sys.argv[1:]

    #check for valid input
    if not allfiles:
        print("No file name provided")
        exit(0)
    
    connect(s,socketpath)

    try:
        for file in allfiles:
            send(s,file)
            response = recv(s).decode()
            if response == "FILE DOES NOT EXIST" :
                print(response)
                continue  

            file_size = int(response)
            received_content = b""

            while len(received_content) < file_size:
                chunk = recv(s)
                if not chunk:
                    break
                received_content += chunk
            printContent(file, received_content.decode())
    finally:
        print("Closing Socket")
        s.close()    

main()