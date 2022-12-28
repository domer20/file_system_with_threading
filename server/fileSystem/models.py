from anytree import NodeMixin


class Base(object):
    foo = 4


class TNode(Base, NodeMixin):
    def __init__(self, name, isfile, blocks, parent=None, children=None):
        super(TNode, self).__init__()
        self.name = name
        self.isfile = isfile
        self.parent = parent
        self.blocks = blocks
        if children:
            self.children = children
