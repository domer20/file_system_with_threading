from anytree import search, RenderTree

from models import TNode, free, mem, root
from textwrap import wrap


def create_file(name, current):
    for i in current.children:
        if i.name == name:
            return "File already exists"

    globals()[name] = TNode(name, 1, [], parent=current)
    return "File created"


def mkdir(name, current):
    for i in current.children:
        if i.name == name:
            return "Directory already exists"
    globals()[name] = TNode(name, 0, [], parent=current)
    return "Directory created"


def list_dir_contents(current):
    dir = ""
    for i in current.children:
        if i.isfile:
            dir += i.name + "   " + "file\n"
        else:
            dir += i.name + "   " + "directory\n"

    return dir


def delete_file(name, current):
    for i in current.children:
        if i.name == name and i.isfile == 1:
            for j in i.blocks:
                free.append(j)
            i.parent = None
            return "File deleted"
        else:
            return "No such file exists"


def cd(path, current):
    new = path
    if new == '..':
        return current.parent
    for child in current.children:
        if new == child.name and child.isfile == 0:
            current = child
            return "current changed"
    else:
        return "No such directory"


def append_to_file(content, current):
    if current.isfile == 1:
        ccontent = ""
        print(current.blocks)
        for i in current.blocks:
            print(mem[i])
            ccontent += mem[i]
        content = ccontent + content
        content_blocks = wrap(content, 128)
        for i in range(len(current.blocks)):
            mem[i] = content_blocks[i]
        content_blocks = content_blocks[len(current.blocks):]
        for i in content_blocks:
            current.blocks.append(free[0])
            mem[free[0]] = i
            free.remove(free[0])
        return "File appended"
    else:
        return "No file is open"


def open_file(name, current):
    for child in current.children:
        if name == child.name and child.isfile == 1:
            return child
    else:
        print("No such file")
        return current


def truncate(current):
    if current.isfile == 1:
        for i in current.blocks:
            free.append(i)
        return "File truncated"
    else:
        return "No file is open"


def mem_map():
    for pre, fill, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8), node.blocks)


def move(name, dirname, current):
    dir = search.findall(root, lambda node: node.name == dirname)[0]
    for i in current.children:
        if i.name == name and dir:
            i.parent = dir
            return "File moved"
    if not dir:
        return "File or directory not found"



def read(position, current):
    buffer = ""
    for i in current.blocks:
        buffer += mem[i]
    output = buffer[position:]
    print(output)


def close(current):
    if current.isfile:
        return current.parent
    else:
        print("no file was open")
        return current
