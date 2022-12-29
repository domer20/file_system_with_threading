from textwrap import wrap

from anytree import NodeMixin, RenderTree, search


class Base(object):
    foo = 4


class TNode(Base, NodeMixin):
    root = None
    mem = []
    free = []

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
        # Check if a file with the same name already exists in the current directory
        if self.name == "root":
            return "Cannot Create in root"
        for child in self.children:
            if child.name == name and child.isfile:
                return "File already exists"

        # Create a new TNode object with the isfile attribute set to True
        file_node = TNode(name, isfile=True, blocks=[], parent=self)
        return "File created"

    def mkdir(self, name):

        if self.name == "root":
            return "Cannot Create in root"
        # Check if a directory with the same name already exists in the current directory
        for child in self.children:
            if child.name == name and not child.isfile:
                return "Directory already exists"

        # Create a new TNode object with the isfile attribute set to False
        dir_node = TNode(name, isfile=False, blocks=[], parent=self)

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

        for i in self.children:
            if i.name == name and i.isfile == 1:
                for j in i.blocks:
                    TNode.free.append(j)
                i.parent = None
                return "File deleted"

            else:
                return "No such file exists"

    def cd(self, path):
        if path == '..' and self.parent:
            return "current changed", self.parent
        for child in self.children:
            if path == child.name and child.isfile == 0:
                return "current changed", child

        return "No such directory", self

    def append_to_file(self, name, content):
        for child in self.children:
            if name == child.name and child.isfile == 1:
                child.write_to_file(content)
                return "File appended"
        else:
            return "No such file"

    def write_to_file(self, content):
        print("========================")
        print(TNode.mem)
        print("========================")
        ccontent = ""
        print(self.blocks)
        for i in self.blocks:

            ccontent += TNode.mem[i]
        content = ccontent + content
        content_blocks = wrap(content, 128)
        for i in range(len(self.blocks)):
            TNode.mem[i] = content_blocks[i]
        content_blocks = content_blocks[len(self.blocks):]
        for i in content_blocks:
            self.blocks.append(TNode.free[0])
            TNode.mem[TNode.free[0]] = i
            TNode.free.remove(TNode.free[0])
        print("========================")
        print(TNode.mem)
        print("========================")
        return "File appended"

    def truncate(self, name):
        for i in self.children:
            if i.name == name and i.isfile == 1:
                for j in i.blocks:
                    TNode.free.append(j)
                i.blocks = []
                return "File truncated"
            else:
                return "No such file exists"

    def move(self, name, dirname):
        dir = search.findall(TNode.root, lambda node: node.name == dirname)[0]
        for i in self.children:
            if i.name != name or i.isfile == 0:
                return "No such file exists"
            if i.name == name and dir:
                i.parent = dir
                return "File moved"

        if not dir:
            return "Directory not found"

    def read(self,name, position):
        position = int(position)
        print(TNode.mem)
        for i in self.children:
            if i.name == name and i.isfile == 1:
                buffer = ""
                for i in self.blocks:
                    buffer += TNode.mem[i]
                output = buffer[position:]
                return output
            else:
                return "No such file exists"

