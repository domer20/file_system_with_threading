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
            param = input("Enter Argument: ")
            sock.send(pickle.dumps((message, param)))
            data = sock.recv(1024)
            current, message, root = pickle.loads(data)
            print(message)
            print("*******************")
            print(current.name)
            print("*******************")
            for pre, fill, node in RenderTree(root):
                treestr = u"%s%s" % (pre, node.name)
                print(treestr.ljust(8), node.blocks)
            print("============================")
    except Exception as e:
        print(str(e))
        send_req()

    finally:
        print('closing socket')
        sock.close()

send_req()
