# src/compressor/huffman.py
import unittest

def encode(text: list[int]) -> tuple[list[int], list[int]]:

    freq_dict = extract_freq_dist(text)

    initial_codebook = huffman_codebook(freq_dict)
    canonical_codebook = canonical_huffman_codebook(initial_codebook)

    output = []
    for element in text:
        for code in canonical_codebook[str(element)]:
            output.append(int(code))
    canon_len = [len(str(canonical_codebook[str(i)])) if str(i) in canonical_codebook else 0 for i in range(10)]

    return (output, canon_len)

def decode(data: list[int], canon_bitlens: list[int]) -> list[int]:

    reversed_canonical_codebook = reconstruct_canonical_codebook(canon_bitlens)

    output_message = []                                               # Stores the output message
    current_decode = ''                                               # Stores the current symbol being decoded

    # Iterates until the end of the text
    while len(data) > 0:

        current_decode = current_decode + str(data[0])                       # Updtaes the current symbol being decoded
        data = data[1:]                                                 # Splices the text list

        # If the current symbol being decoded is in the decodebook, update the output message and reset the current_decode variable
        if current_decode in reversed_canonical_codebook:
            output_message.append(int(reversed_canonical_codebook[current_decode]))
            current_decode = ''

    return output_message

#Test Classes
#The test cases were manually created by taking the Huffman codebook using a different Huffman coding algorithm, constructing the canonicalization table to make the codes closer to each other, via MS Excel
class encode_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = [5, 5, 6, 3, 3, 3, 1, 6, 6]
        Expected_Output_1 = ([1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0], [0, 3, 0, 2, 0, 3, 1, 0, 0, 0])
        Test_Case_2 = [6, 8, 9, 0, 0, 9, 8, 2, 5, 2, 7, 2, 2, 2]
        Expected_Output_2 = ([1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0], [3, 0, 1, 0, 0, 5, 5, 4, 3, 3])
        Test_Case_3 = [3, 1, 0, 4, 1, 9, 0, 0, 7, 0, 8, 1, 0, 9, 1, 9, 0, 0, 9]
        Expected_Output_3 = ([1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0], [2, 2, 0, 4, 4, 0, 0, 4, 4 ,2])
        
        #Function call
        Output_1 = encode(Test_Case_1)
        Output_2 = encode(Test_Case_2)
        Output_3 = encode(Test_Case_3)
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_3, Expected_Output_3)
        pass

class decode_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = ([1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0], [0, 3, 0, 2, 0, 3, 1, 0, 0, 0])
        Expected_Output_1 = [5, 5, 6, 3, 3, 3, 1, 6, 6]
        Test_Case_2 = ([1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0], [3, 0, 1, 0, 0, 5, 5, 4, 3, 3])
        Expected_Output_2 = [6, 8, 9, 0, 0, 9, 8, 2, 5, 2, 7, 2, 2, 2]
        Test_Case_3 = ([1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0], [2, 2, 0, 4, 4, 0, 0, 4, 4 ,2])
        Expected_Output_3 = [3, 1, 0, 4, 1, 9, 0, 0, 7, 0, 8, 1, 0, 9, 1, 9, 0, 0, 9]
        
        #Function call
        Output_1 = decode(Test_Case_1[0], Test_Case_1[1])
        Output_2 = decode(Test_Case_2[0], Test_Case_2[1])
        Output_3 = decode(Test_Case_3[0], Test_Case_3[1])
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_3, Expected_Output_3)
        pass


# def main():

    # bits, canon_len = encode([3, 1, 0, 4, 1, 9, 0, 0, 7, 0, 8, 1, 0, 9, 1, 9, 0, 0, 9])

    # print(canon_len)

    # print(decode(bits,canon_len))

    # unittest.main(verbosity=2)


############ Helper Functions #################

def extract_freq_dist(text):
    """
    Use list comprehension to generate a dictionary with each key being the unique symbols in the text.
    Use the function count() to count the instances of each symbol in the text.
    """
    return {str(i):text.count(i) for i in set(text)}

"""
Implementation for Generating the Huffman Codebook is divided into different parts:
1. Creating a new class node to store the left and right children.
2. Creating the Huffman Tree.
  - Initialize everyone as a node with no left and right values and store it into a list.
  - Sort the list based on the frequency of each node.
  - Obtain the two lowest symbol on the list located at the 1st and 2nd index.
  - Create a new node indicating the left and right children as the 1st and 2nd element of the list, respectively.
  - Remove the two lowest node from the list and append the newly created node.
  - Repeat until only one element is left in the list. This element is the root node.
3. Traversing the tree for the actual Huffman encoding.
  - Implement a recursive function with parameters node and code.
  - Base Case: If the node passed in the recursive function is of type string, return the code.
    - Recall that from Step 2, we created a list of nodes from the string of the symbols.
    - Thus, the lowest part of the tree should be a type string not a class Node.
  - If the base case is not satisfied, get the left and right node and call the function again for both nodes.
    - Update the code by appending "0" and "1" in the recursive call for the left and right node, respectively. 
4. Return the dictionary with the Huffman Codebook.
"""

class Node:
    def __init__(self, left = None, right = None, value = -1):
        self.value = value
        self.left = left
        self.right = right

def huffman_tree(freq_dict):

    # Sort the current list of nodes.
    temp = sorted(freq_dict.items(), key=lambda x:x[1])
    nodes = []

    for element in temp:
        node = Node(None, None, int(element[0]))
        nodes.append((element[0], element[1], node))
    
    # Repeat the process until the list of nodes only has 1 element left.
    while len(nodes) > 1:
        left = nodes[0]                                           # A tuple containing (node, frequency)
        right = nodes[1]
        nodes = nodes[2:]

        node = Node(left[0], right[0])                            # Creating a new node with the two lowest nodes as its children.
        nodes.append((node, left[1]+right[1], node))                    # Append the new node as a tuple.
        nodes = sorted(nodes, key=lambda x:(x[1], x[2].value))                  # Sort it again.

    return nodes

def huffman_traversal(node, code=''):
    # Base Case: If the current node is a string, it means it is a symbol.

    if type(node) is str:
        return {node: code}
    
    # Recursive call for the left and right node.
    codebook = {}
    codebook.update(huffman_traversal(node.left, code+"0"))     # Append "0" to the left node as it has lower frequency
    codebook.update(huffman_traversal(node.right, code+"1"))    # Append "1" to the right node as it has higher frequency

    return codebook

def huffman_codebook(freq_dict):
    # Fill in your code here
    
    # Tree Creation
    nodes = huffman_tree(freq_dict) 
    
    # Tree Traversal for Huffman Code
    return huffman_traversal(nodes[0][0])

def canonical_huffman_codebook(codebook):
    sorted_codebook  = sorted(codebook.items(), key=lambda x:(len(x[1]),int(x[0])))                         # Sort the old mappings by increasing codeword length, and ascending mapped values.

    C_canon = "0"                                                                                           # Intialize C_canon = 0
    canonical_codebook_list = []                                                                            # Iniatilize a list contaning the canonical codebook

    # Note. codebook is a dictionay with "symbol":"code"
    for code in sorted_codebook:
        if len(str(C_canon)) == len(str(code[1])):                                                          # If codeword length is equal to length of C_canon, replace old codeword length with value of C_canon
            canonical_codebook_list.append((code[0], C_canon))
        else:                                                                                               # If codeword length is not equal to the length of C_canon, left shift the bits of C_canon until they have the same length and replace the old codeword length.
            C_canon = C_canon+("0"*(len(str(code[1]))-len(str(C_canon))))
            canonical_codebook_list.append((code[0], C_canon))

        C_canon = format(int(str(C_canon),2)+1, '0'+str(len(C_canon))+'b')                                  # For each mapping in the sorted_codebook, increment C_canon by 1.
    
    canonical_codebook_list = sorted(canonical_codebook_list, key=lambda element: (int(element[0])))        # Sort the codeword by mapped values.

    canonical_codebook = {key:value  for (key,value) in canonical_codebook_list}                            # Create the dictionary.

    return canonical_codebook

def reconstruct_canonical_codebook(canon_bitlens):
    codes = []
    for i in range(10):
        if canon_bitlens[i] != 0: codes.append((str(i), canon_bitlens[i]))                                  # Create a list based on canon_bitlens where each element is a tuple (symbol, canonical length)

    sorted_codes = sorted(codes, key=lambda element: (element[1],int(element[0])))

    C_canon = "0"                                                                                           # Intialize C_canon = 0
    canonical_codebook_list = []                                                                            # Iniatilize a list contaning the canonical codebook

    # Note. reversed codebook is a dictionay with "code":"symbol"
    for code in sorted_codes:
        if len(str(C_canon)) == code[1]:                                                                    # If codeword length is equal to length of C_canon, replace old codeword length with value of C_canon
            canonical_codebook_list.append((code[0], C_canon))                                              
        else:                                                                                               # If codeword length is not equal to the length of C_canon, left shift the bits of C_canon until they have the same length and replace the old codeword length.
            C_canon = C_canon+("0"*((code[1])-len(str(C_canon))))
            canonical_codebook_list.append((code[0], C_canon))

        C_canon = format(int(str(C_canon),2)+1, '0'+str(len(C_canon))+'b')                                  # For each mapping in the sorted_codebook, increment C_canon by 1.
    
    canonical_codebook_list = sorted(canonical_codebook_list, key=lambda element: (int(element[0])))        # Sort the codeword by mapped values.

    reversed_canonical_codebook = {value:key  for (key,value) in canonical_codebook_list}                   # Create the dictionary. Note that the key value pairs are swapped as this will be used for decoding.

    return reversed_canonical_codebook

# main()
# unittest.main(verbosity=2)