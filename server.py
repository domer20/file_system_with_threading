import pickle
import socket
import threading
import jsonpickle
from anytree import RenderTree
from models import  TNode

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

with open("C:\\Users\\MoezAhmad\\Desktop\\New folder\\file_system_with_threading\\sys.dat", "r") as f:
    data = f.read()
TNode.root, TNode.mem, TNode.free = jsonpickle.loads(data)
TNode.root = TNode.from_dict(TNode.root)
for pre, fill, node in RenderTree(TNode.root):
    treestr = u"%s%s" % (pre, node.name)
    print(treestr.ljust(8), node.blocks)


# Create a lock
lock = threading.Lock()


def handle_client(connection):
    current = TNode.root
    message = ""
    try:

        while True:
            # Receive the data from the client
            data = connection.recv(1024)
            if not data:
                break

            command, *args = pickle.loads(data)
            print(command, *args)

            lock.acquire()
            # Execute the command
            if command == 'create_file':
                message = current.create_file(*args)
            elif command == 'mkdir':
                message = current.mkdir(*args)
            elif command == 'list_dir_contents':
                message = current.list_dir_contents()
            elif command == 'delete_file':
                message = current.delete_file(*args)
            elif command == 'cd':
                message, current = current.cd(*args)
            elif command == 'append_to_file':
                message = current.append_to_file(*args)
            elif command == 'truncate':
                message = current.truncate(*args)
            elif command == 'mem_map':
                TNode.mem_map(TNode.root)
            elif command == 'move':
                message = current.move(*args)
            elif command == 'read':
                message = current.read(*args)
            elif command == 'exit':
                message = "Bye"
                lock.release()
                break
            else:
                message = "Invalid command"
            lock.release()
            # Serialize the response and send it back to the client
            response = pickle.dumps((current, message,TNode.root))
            connection.send(response)
        response = pickle.dumps((current, message, TNode.root))
        connection.send(response)

    finally:
        # Clean up the connection
        connection.close()


while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    print('connection from', client_address)
    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(connection,))
    client_thread.start()

