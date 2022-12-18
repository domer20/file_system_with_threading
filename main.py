from anytree import NodeMixin, RenderTree, search
import jsonpickle
from textwrap import wrap
import threading
import sys


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


def create_file(name):
    for i in current.children:
        if i.name == name:
            print("File already exists")
            return
    globals()[name] = TNode(name, 1, [], parent=current)
    print("File created")


def mkdir(name):
    for i in current.children:
        if i.name == name:
            print("Directory already exists")
            return
    globals()[name] = TNode(name, 0, [], parent=current)
    print("Directory created")


def list_dir_contents():
    for i in current.children:
        if i.isfile:
            print(i.name + "   " + "file")
        else:
            print(i.name + "   " + "directory")


def delete_file(name):
    for i in current.children:
        if i.name == name and i.isfile == 1:
            for j in i.blocks:
                free.append(j)
            i.parent = None
        else:
            print("No such file exists")


def cd(path):
    new = path
    if new == '..':
        return current.parent
    for child in current.children:
        if new == child.name and child.isfile == 0:
            return child
    else:
        print("No such directory")
        return current


def append_to_file(content):
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
    else:
        print("No file is open")


def open_file(name):
    for child in current.children:
        if name == child.name and child.isfile == 1:
            return child
    else:
        print("No such file")
        return current


def truncate():
    if current.isfile == 1:
        for i in current.blocks:
            free.append(i)
    else:
        print("No file is open")


def mem_map():
    for pre, fill, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8), node.blocks)


def move(name, dirname):
    dir = search.findall(root, lambda node: node.name == dirname)[0]
    for i in current.children:
        if i.name == name and dir:
            i.parent = dir
            print("File moved")
    if not dir:
        print("File or directory not found")


def read(position):
    buffer = ""
    for i in current.blocks:
        buffer += mem[i]
    output = buffer[position:]
    print(output)


def close():
    if current.isfile:
        return current.parent
    else:
        print("no file was open")
        return current


def thread_function(name):
    text_file = open("sample" + str(name + 1) + ".txt", "r")
    with open("output" + str(name + 1) + '.txt', 'w+', encoding="utf-8") as f:
        sys.stdout = f
        lines = text_file.readlines()
        global current
        current = root
        count = 0
        for line in lines:
            count += 1
            temp = eval(line)
            if temp:
                current = temp
        text_file.close()


if __name__ == "__main__":
    # loading data structures from file
    with open('sys.dat', 'r') as file:
        root, mem, free = eval(file.read())
    root = jsonpickle.decode(root)

    # initial settings
    current = root
    cblocks = []
    thread_count = int(input("Enter the number of threads (between 1 and 6): "))
    while 1 >= thread_count or thread_count > 6:
        thread_count = int(input("Invalid input, enter a number between 1 and 6: "))
    threads = list()

    for index in range(thread_count):
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()

    # saving the memory tree in file
    json_string = jsonpickle.encode(root)
    mem_list = [json_string, mem, free]
    with open('sys.dat', 'w') as file:
        file.write(str(mem_list))