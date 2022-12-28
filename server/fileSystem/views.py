import jsonpickle
from anytree import RenderTree, search
from django.http import HttpResponse
from textwrap import wrap
from fileSystem.apps import root, mem, free
from fileSystem.models import TNode

current = root

def index(request):
    return HttpResponse("Hello, world. Wellcome to Logical File System")




def open_file(name):
    for child in current.children:
        if name == child.name and child.isfile == 1:
            return HttpResponse(jsonpickle.encode(child))
    else:
        return HttpResponse("No such file")
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





def create_file(request, name):
    for i in current.children:
        if i.name == name:
            print("File already exists")
            return
    globals()[name] = TNode(name, 1, [], parent=current)
    return HttpResponse(f"{name} created")

def mkdir(request, name):
    for i in current.children:
        if i.name == name:
            print("Directory already exists")
            return
    globals()[name] = TNode(name, 0, [], parent=current)
    return HttpResponse(f"{name} created")

def list_dir_contents(request):
    contents = []
    for i in current.children:
        contents.append((i.name,str(i.isfile)))
    if len(contents) == 0:
        return HttpResponse("Directory is empty")
    return HttpResponse(contents)

def delete_file(request, name):
    for i in current.children:
        if i.name == name and i.isfile == 1:
            for j in i.blocks:
                free.append(j)
            i.parent = None
            return HttpResponse(f"{name} Deleted")
        else:
            return HttpResponse("No such file exists")



def cd(request, path):
    global current
    new = path
    if new == '..' and current != root:
        current = current.parent
        return HttpResponse(current.parent.name)
    for child in current.children:
        if new == child.name and child.isfile == 0:
            current = child
            return HttpResponse(child.name)
    else:
        return HttpResponse("Invalid Path")


def append_to_file(request, content):
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
        return HttpResponse(f"{content} appended")
    else:
        return HttpResponse("No file is open")


def truncate(request):
    if current.isfile == 1:
        for i in current.blocks:
            free.append(i)
        return HttpResponse("File Truncated")
    else:
        return HttpResponse("No file is open")


def mem_map(request):

    for pre, fill, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8), node.blocks)
    return HttpResponse("root")


def move(request, name, dirname):
    dir = search.findall(root, lambda node: node.name == dirname)[0]
    for i in current.children:
        if i.name == name and dir:
            i.parent = dir
            return HttpResponse("File moved")
    if not dir:
        return HttpResponse("File or directory not found")



