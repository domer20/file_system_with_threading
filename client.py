import pickle
import socket
import sys

from anytree import RenderTree

from models import TNode

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

def send_req():
    try:
        while True:
            print("============================")
            message = input("Enter Command: ")
            param = input("Enter name: ")
            if message == "append_to_file" or message == "move" or message == "read":
                if message == "append_to_file":
                    text = input("Enter content: ")
                elif message == "read":
                    text = input("Enter position: ")
                else:
                    text = input("Enter directory: ")
                sock.send(pickle.dumps((message, param, text)))
            else:
                sock.send(pickle.dumps((message, param)))
            data = sock.recv(2**20)
            current, message, root = pickle.loads(data)
            print(message)
            print("*******************")
            print(current.name)
            print("*******************")
            for pre, fill, node in RenderTree(root):
                treestr = u"%s%s" % (pre, node.name)
                print(treestr.ljust(8), node.blocks)
            if message == "Bye":
                break
    except Exception as e:
        print(str(e))
        send_req()

    finally:
        print('closing socket')
        sock.close()

send_req()
