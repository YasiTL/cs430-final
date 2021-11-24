import os

# Every node in the Huffman tree is made up of a character (or characters), the frequency those characters appear,
# and any left/right nodes if they exist. Every node has a Huffman describing it too.
class node:
    def __init__(self, character, frequency, left=None, right=None):
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right
        self.huff = '' # Tree direction 1 or 0

# Creates a dictionary where the keys are any character present in a string, and the values are the frequency that character appeared
# i.e. 'aabbcde' -> {a:3, b:2, c:1, d:1, e:1}
def createFrequencyDict(input):
    dict = {}
    for char in input:
        if char in dict:
            dict[char] += 1
        else:
            dict[char] = 1
    return dict

# Creates a huffman tree with the special nodes we defined 
def createHufman(freq_dict):
    nodes = []

    for key in freq_dict.keys():
        nodes.append(node(key, freq_dict[key]))

    while len(nodes) > 1:
        # Sort the nodes by their values in the dictonary, not by their keys
        nodes = sorted(nodes, key=lambda x: x.frequency)

        # Grab the two smallest items in the list
        left = nodes[0]
        right = nodes[1]

        left.huff = 0
        right.huff = 1

        # create a new node
        new_freq = left.frequency + right.frequency
        new_char = left.character + right.character
        new_node = node(new_char, new_freq, left, right)

        # remove the 2 nodes and add their parent as new node among others
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)
    
    return nodes[0]

# 
def createCodeDict(node, val='', code_dict={}):
    # The Huffman code for current node
    huffman_val = val + str(node.huff)

    if(node.left):
        createCodeDict(node.left, huffman_val, code_dict)
    if(node.right):
        createCodeDict(node.right, huffman_val, code_dict)

    if(not node.left and not node.right):
        code_dict[node.character] = huffman_val
    
    return code_dict

# Do all the work to encode a file, based on the project specifications.
# This code also prints to the command line and makes an encoded output file as per directions.
def encoding(file_path):
    f = open(file_path, "r")
    file_contents = f.read()

    stripped_input = ''
    for char in file_contents:
        if char.isalpha():
            stripped_input += char.lower()
    
    freq_dict = createFrequencyDict(stripped_input)
    root_node = createHufman(freq_dict)
    code_dict = createCodeDict(root_node)

    # Print the letters and their codes to the screen as per instructions
    print(code_dict)

    encoded_string = ''
    for c in stripped_input:
        encoded_string += code_dict[c]
    f = open("encoded_output.txt","w+")
    f.write(encoded_string)
    
    return root_node

# Opens up the encoded_output.txt file and 
def decoding(root_node):
    f = open("encoded_output.txt", "r")
    file_contents = f.read()

    current_node = root_node
    decoded_string = ''

    # Traverse all the 1's and 0's in our encoded string
    for char in file_contents:
        if char == '0':
            current_node = current_node.left
        elif char == '1':
            current_node = current_node.right
        if (current_node.left is None and current_node.right is None):
            decoded_string += current_node.character
            current_node = root_node
        
    f = open("decoded_output.txt","w+")
    f.write(decoded_string)

# DRIVER CODE
print("~ * ~ * CS 430 FINAL PROJECT * ~ * ~ ")
fpath = str(input("Please enter the realitive path to the file you would like to encode: "))
if os.path.isfile(fpath):
    root_node = encoding(fpath)
    # Either need to print tree HERE or within the encoding function.

    user_answer = input("Would you like to decode the file you just encoded? (Y/N): ")
    if user_answer.lower() == 'y':
        decoding(input, root_node)
        print("The result of your decoding is in: \"decoded_output.txt\" ")
    elif user_answer.lower() == 'n':
        print("Thanks. Bye!")
        exit()
else:
    print("Please re-run with a valid path to a file.")
    exit()