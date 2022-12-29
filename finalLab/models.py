from textwrap import wrap

from anytree import NodeMixin, RenderTree, search


class Base(object):
    foo = 4


free = []
mem = []
root = None


class TNode(Base, NodeMixin):
    def __init__(self, name, isfile, blocks, parent=None, children=None):
        super(TNode, self).__init__()
        self.name = name
        self.isfile = isfile
        self.parent = parent
        self.blocks = blocks
        if children:
            self.children = children

    @staticmethod
    def from_dict(data):
        if '__main__.TNode' in str(data):
            # Create a new TNode object with the attributes from the data dictionary
            tnode = TNode(data['name'], data['isfile'], data['blocks'])

            # Recursively convert the children of the TNode to TNode objects
            children = [TNode.from_dict(child) for child in data['children']]
            tnode.children = children

            # Return the TNode object
            return tnode
        return data

    @staticmethod
    def mem_map(root):
        for pre, fill, node in RenderTree(root):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), node.blocks)

    def create_file(self, name):
        global current
        # Check if a file with the same name already exists in the current directory
        if self.name =="root":
            return "Cannot Create in root"
        for child in self.children:
            if child.name == name and child.isfile :
                return "File already exists"

        # Create a new TNode object with the isfile attribute set to True
        file_node = TNode(name, isfile=True, blocks=[], parent=self)
        current = self
        return "File created"

    def mkdir(self, name):
        global current
        if self.name =="root":
            return "Cannot Create in root"
        # Check if a directory with the same name already exists in the current directory
        for child in self.children:
            if child.name == name and not child.isfile:
                return "Directory already exists"

        # Create a new TNode object with the isfile attribute set to False
        dir_node = TNode(name, isfile=False, blocks=[], parent=self)
        current = self

        return "Directory created"

    def list_dir_contents(self):
        dir = ""
        # Iterate over the children of the current directory
        for child in self.children:
            # Print the name and type of the child
            if child.isfile:
                dir += child.name + "   " + "file\n"
            else:
                dir += child.name + "   " + "directory\n"
        return dir

    def delete_file(self, name):
        global current
        for i in self.children:
            if i.name == name and i.isfile == 1:
                for j in i.blocks:
                    free.append(j)
                i.parent = None
                return "File deleted"
                current = self
            else:
                return "No such file exists"

    def cd(self, path):

        if path == '..':
            return self.parent
        for child in self.children:
            if path == child.name and child.isfile == 0:
                return "current changed", child
        else:
            return "No such directory"

    def append_to_file(self, content):

        if self.isfile == 1:
            ccontent = ""
            print(self.blocks)
            for i in self.blocks:
                print(mem[i])
                ccontent += mem[i]
            content = ccontent + content
            content_blocks = wrap(content, 128)
            for i in range(len(self.blocks)):
                mem[i] = content_blocks[i]
            content_blocks = content_blocks[len(self.blocks):]
            for i in content_blocks:
                self.blocks.append(free[0])
                mem[free[0]] = i
                free.remove(free[0])

            return "File appended"
        else:
            return "No file is open"

    def truncate(self):
        if self.isfile == 1:
            for i in self.blocks:
                free.append(i)

            return "File truncated"
        else:
            return "No file is open"

    def move(self, name, dirname):
        dir = search.findall(root, lambda node: node.name == dirname)[0]
        for i in self.children:
            if i.name != name or i.isfile == 0:
                return "No such file exists"
            if i.name == name and dir:
                i.parent = dir
                return "File moved"

        if not dir:
            return "Directory not found"
