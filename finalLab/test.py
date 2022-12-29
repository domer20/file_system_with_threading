import jsonpickle
from anytree import RenderTree, NodeMixin

from models import TNode

# mem and free objects
mem = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None, 12: None, 13: None, 14: None, 15: None, 16: None, 17: None, 18: None, 19: None, 20: None, 21: None, 22: None, 23: None, 24: None, 25: None, 26: None, 27: None, 28: None, 29: None, 30: None, 31: None, 32: None, 33: None, 34: None, 35: None, 36: None, 37: None, 38: None, 39: None, 40: None, 41: None, 42: None, 43: None, 44: None, 45: None, 46: None, 47: None, 48: None, 49: None, 50: None, 51: None, 52: None, 53: None, 54: None, 55: None, 56: None, 57: None, 58: None, 59: None, 60: None, 61: None, 62: None, 63: None, 64: None, 65: None, 66: None, 67: None, 68: None, 69: None, 70: None, 71: None, 72: None, 73: None, 74: None, 75: None, 76: None, 77: None, 78: None, 79: None, 80: None, 81: None, 82: None, 83: None, 84: None, 85: None, 86: None, 87: None, 88: None, 89: None, 90: None, 91: None, 92: None, 93: None, 94: None, 95: None, 96: None, 97: None, 98: None, 99: None, 100: None, 101: None, 102: None, 103: None, 104: None, 105: None, 106: None, 107: None, 108: None, 109: None, 110: None, 111: None, 112: None, 113: None, 114: None, 115: None, 116: None, 117: None, 118: None, 119: None, 120: None, 121: None, 122: None, 123: None, 124: None, 125: None, 126: None, 127: None, 128: None, 129: None, 130: None, 131: None, 132: None, 133: None, 134: None, 135: None, 136: None, 137: None, 138: None, 139: None, 140: None, 141: None, 142: None, 143: None, 144: None, 145: None, 146: None, 147: None, 148: None, 149: None, 150: None, 151: None, 152: None, 153: None, 154: None, 155: None, 156: None, 157: None, 158: None, 159: None, 160: None, 161: None, 162: None, 163: None, 164: None, 165: None, 166: None, 167: None, 168: None, 169: None, 170: None, 171: None, 172: None, 173: None, 174: None, 175: None, 176: None, 177: None, 178: None, 179: None, 180: None, 181: None, 182: None, 183: None, 184: None, 185: None, 186: None, 187: None, 188: None, 189: None, 190: None, 191: None, 192: None, 193: None, 194: None, 195: None, 196: None, 197: None, 198: None, 199: None}
free = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199]

root = TNode('root', 0, [])
print(type(root.children))
# Serialize the object to a JSON string using jsonpickle
json_string = jsonpickle.encode(root)

# Print the JSON string
print(json_string)

with open('C:\\Users\\MoezAhmad\\Desktop\\finalLab\\sys.dat', 'r') as file:
    data = file.read()
    root,mem,free = jsonpickle.decode(data)
    print(type(root.children))

for pre, fill, node in RenderTree(root):
    treestr = u"%s%s" % (pre, node.name)
    print(treestr.ljust(8), node.blocks)

# Save the objects to a file
# with open('C:\\Users\\MoezAhmad\\Desktop\\finalLab\\sys.dat', 'w') as file:
#     data = [root, mem, free]
#
#     encoded = jsonpickle.encode(data, unpicklable=False)
#     file.write(encoded)