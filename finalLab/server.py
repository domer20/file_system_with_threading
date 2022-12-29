import pickle
import socket
import threading
import jsonpickle
from anytree import RenderTree
import threading



from models import free, mem, root, TNode
from controllers import create_file, mkdir, list_dir_contents, delete_file, cd, append_to_file,  truncate, mem_map, move

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# File system variables


def handle_client(connection):
    current = root
    message = ""
    try:

        while True:
            # Receive the data from the client
            data = connection.recv(1024)
            if not data:
                break

            command, *args = pickle.loads(data)
            print(command,*args)

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
                message = current.truncate()
            elif command == 'mem_map':
                TNode.mem_map(root)
            elif command == 'move':
                message = current.move(*args)
            lock.release()
            # Serialize the response and send it back to the client
            response = pickle.dumps((current, message,root))
            connection.send(response)
            break
    finally:
        # Clean up the connection
        connection.close()



with open("C:\\Users\\MoezAhmad\\Desktop\\finalLab\\sys.dat", "r") as f:
    root, mem, free = jsonpickle.loads(f.read())
    root = TNode.from_dict(root)
    for pre, fill, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8), node.blocks)
# Create a lock
lock = threading.Lock()
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    print('connection from', client_address)
    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(connection,))
    client_thread.start()
