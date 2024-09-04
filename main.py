from socket import *
import sys

PORT = 12000 # def to 12000 for port
try:
    if sys.argv[1]:
        PORT = int(sys.argv[1])
except Exception:
    print("No port provided, using default of 12000")

SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)

# Enable reuse of the address
SERVER_SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

SERVER_SOCKET.bind(("", PORT)) # still no idea what "" param is
SERVER_SOCKET.listen(1) # open connection

def main():
    while True:
        print('Ready to serve...')
        conn_socket, addr = SERVER_SOCKET.accept()
        if conn_socket: # if connection made
            try:
                message = conn_socket.recv(1024).decode() # get message sent by client (max 1024 bytes) and decode
                filename = message.split()[1]
                outputdata = ""
                with open(filename[1:], "r") as f:
                    outputdata = f.read()

                # send http headers
                headers = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(outputdata)}\r\n\r\n'

                conn_socket.send(headers.encode())
                conn_socket.send(outputdata.encode())
                conn_socket.send("\r\n".encode())

                conn_socket.close()

            except IOError: # error thrown if file doesnt exist
                # 404 error
                htmlData = ""
                with open("404.html", "r") as f:
                    htmlData = f.read()

                headers = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(htmlData)}\r\n\r\n'

                conn_socket.send(headers.encode())
                conn_socket.send(htmlData.encode())

                conn_socket.close()


if __name__ == "__main__":
    try:
        # see if main runs ok
        main()
    except Exception as e:
        # handle any exceptions (not very well but whatever)
        print(e)
    finally:
        # terminate and close everything whether success or fail
        SERVER_SOCKET.close()
