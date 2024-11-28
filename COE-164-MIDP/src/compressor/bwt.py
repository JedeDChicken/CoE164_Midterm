# src/compressor/bwt.py
import unittest

def encode(text: str) -> tuple[str, int]:
    #Transform "text" using Burrows-Wheeler transform and return the result and index, respectively
    #Ensure to append the sentinel character $
    '''
    Steps for BWT Encoding:
    1. Generate cyclic rotations of the text.
    2. Arrange the strings lexographically.
    3. Output the last letters of each string as the BWT.
    '''

    '''
    Step 1: Generate the cyclic rotations of the text.
    - To ease the process, we just store the text that is before the EOF character (meaning in 'na$bana' we will only store 'na$')
    '''
    text += "\0"                                                    #Append "\0" as sentinel char
    cyclic_rotations = {i:text[i:] for i in range(len(text))}

    '''
    Step 2: Arrange the cyclic rotations lexographically.
    - Sort the dictionary using sorted(). Note that it returns a list.
    - Obtain the index of 'banana$' using index()
    '''
    arranged = sorted(cyclic_rotations.items(), key=lambda x:x[1])
    index = arranged.index((0, text))

    '''
    Step 3: Obtained the last letters of each string and output it as the BWT.
    - Initialize a variable for the output string.
    - Let i be the index of the string in the tuple and l be the length of the text.
    - For each tuple, append the (-1)th element of text
    '''
    bwt = ""
    for key, value in arranged:
        bwt += text[key-1]

    return (bwt, index)


def decode(text: str, index: int) -> str:
    #Return the inverse Burrows-Wheeler transform of "text" using the suffix index "index"
    orginal_tuples = [(text[i],i) for i in range(len(text))]

    sorted_tuples = sorted(orginal_tuples, key=lambda element: (element[0], element[1]))

    current_idx = index
    decoded_message = ""

    for i in range(len(text)):
        decoded_message += sorted_tuples[current_idx][0]
        current_idx = sorted_tuples[current_idx][1]

    return decoded_message


#Test Classes- we can comment out other test cases to verify each test individually
#The test cases were manually created by constructing cyclic rotation tables, sorting the rows, and taking the last letters of the rows, via MS Excel
#For decode, the process was just inversed to obtain the original message + the sentinel character
class encode_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = "bananaaa!"
        Expected_Output_1 = ("!aaannb\0aa", 7)
        Test_Case_2 = "Hello, world!"
        Expected_Output_2 = ("!,do\0lHrellwo ", 4)
        Test_Case_3 = "dddddiiirrrroopppppqqqllll"
        Expected_Output_3 = ("l\0dddddiilllqrooppppqqprrri", 1)
        
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
        Test_Case_1 = ("!aaannb\0aa", 7)
        Expected_Output_1 = "bananaaa!\0"
        Test_Case_2 = ("!,do\0lHrellwo ", 4)
        Expected_Output_2 = "Hello, world!\0"
        Test_Case_3 = ("l\0dddddiilllqrooppppqqprrri", 1)
        Expected_Output_3 = "dddddiiirrrroopppppqqqllll\0"
        
        #Function call
        Output_1 = decode(Test_Case_1[0], Test_Case_1[1])
        Output_2 = decode(Test_Case_2[0], Test_Case_2[1])
        Output_3 = decode(Test_Case_3[0], Test_Case_3[1])
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_3, Expected_Output_3)
        pass

#unittest.main(verbosity=2)