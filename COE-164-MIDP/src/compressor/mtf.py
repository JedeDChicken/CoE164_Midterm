# src/compressor/mtf.py
import unittest

def encode(text: str, alphabet: str) -> list[int]:
    '''
    Steps for MTF Transform Encoding:
    1. Initialize the list of characters using the list, alphabet.
    2. Initialize the output queue, encoded.
    3. Given a message M, do the following |M| times for each character in M.
        - Find the index from zero of the character in message based on the alphabet list. Push this index to encoded.
        - Remove the same character on the alphabet and reinsert it at the front.
    4. Return the transformed text.
    '''

    encoded = []                                                        # Step 2: Initialize the output queue.
    for i in range(len(text)):
        encoded.append(alphabet.index(text[i]))                         # Step 3.1: Find the index from zero of the character in message based on the alphabet list. Push this index to encoded.
        alphabet.insert(0,alphabet.pop(alphabet.index(text[i])))        # Step 3.2: Remove the same character on the alphabet and reinsert it at the front.

    return encoded                                                      # Step 4: Return the transformed text.


def decode(data: list[int], alphabet: str) -> str:
    '''
    Steps for MTF Transform Decoding:
    1. Get the original pre-sorted alphabet.
    2. Initalize the output queue, decoded.
    3. Given an array of number, data, do the following |data| times for each value in data.
        - Get the character in alphabet corresponding to the index in the element in data. Push this character to decoded.
        - Remove the same character in alphabet and reinsert it at the front.
    4. Return the transformed text.
    '''

    decoded = ""                                                        # Step 2: Initalize the output queue, decoded.
    for i in range(len(data)):
        decoded += alphabet[data[i]]                                    # Step 3.1: Get the character in alphabet corresponding to the index in the element in data. Push this character to decoded.
        alphabet.insert(0,alphabet.pop(data[i]))                        # Step 3.2: Remove the same character in alphabet and reinsert it at the front.

    return decoded                                                      # Step 4: Return the transformed text.


#Test Classes
#The test cases were manually created by sorting the unique characters, constructing the MTF table, and collecting the respective indices, via MS Excel
class encode_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = ("bananaaa!\0", ["\x00", "!", "a", "b", "n"])
        Expected_Output_1 = [3, 3, 4, 1, 1, 1, 0, 0, 4, 4]
        Test_Case_2 = ("Hello, world!\0", ['\x00', ' ', '!', ',', 'H', 'd', 'e', 'l', 'o', 'r', 'w'])
        Expected_Output_2 = [4, 6, 7, 0, 8, 7, 6, 10, 3, 10, 5, 10, 10, 10]
        
        #Function call
        Output_1 = encode(Test_Case_1[0], Test_Case_1[1])
        Output_2 = encode(Test_Case_2[0], Test_Case_2[1])
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        pass

class decode_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = ([3, 3, 4, 1, 1, 1, 0, 0, 4, 4], ["\x00", "!", "a", "b", "n"])
        Expected_Output_1 = "bananaaa!\0"
        Test_Case_2 = ([4, 6, 7, 0, 8, 7, 6, 10, 3, 10, 5, 10, 10, 10], ['\x00', ' ', '!', ',', 'H', 'd', 'e', 'l', 'o', 'r', 'w'])
        Expected_Output_2 = "Hello, world!\0"
        
        #Function call
        Output_1 = decode(Test_Case_1[0], Test_Case_1[1])
        Output_2 = decode(Test_Case_2[0], Test_Case_2[1])
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        pass
    
# unittest.main(verbosity=2)