import jsonpickle
from django.apps import AppConfig
import pyparsing as pp

from fileSystem.models import TNode

root = None
mem = None
free = None

def from_dict(data):
    if '__main__.TNode' in str(data):
        # Create a new TNode object with the attributes from the data dictionary
        tnode = TNode(data['name'], data['isfile'], data['blocks'])

        # Recursively convert the children of the TNode to TNode objects
        children = [from_dict(child) for child in data['_NodeMixin__children']]
        tnode.children = children

        # Return the TNode object
        return tnode
    return data
class FilesystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fileSystem'


    def ready(self):
        global root, mem, free

        # Open the sys.dat file and read the TNode object
        with open('C:\\Users\\MoezAhmad\\Desktop\\file_system_with_threading\\server\\fileSystem\\sys.dat', 'r') as file:
            data = file.read()
            root, mem, free = jsonpickle.loads(data)
            root = from_dict(root)

            print(root)