# src/compressor/rle.py
import unittest

def encode(text: list[int]) -> list[int]:
    '''
    Steps in Encoding for RLE:
    1. Initialize a counter N_zero.
        - Counts the number of zeros encountered. Initially set to 0.
    2. Initialize an output queue L.
    3. Get an array of numbers, text, and do the following |text|+1 times.
        - Check if the current loop index is not greater than |text|-1 and the element is not zero.
            - If the element is equal to zero, increment N_zero.
            - Otherwise,
                - Convert N_zero to binary and add one.
                - Push each digit starting from the LSB bit into L except the MSB.
                - Reset N_zero to zero.
                - Push element+2 into L.
    4. Return the output queue.
    '''

    N_zero = 0                                                      # Step 1: Initialize a counter N_zero.
    L = []                                                          # Step 2: Initialize an output queue L.

    for i in range(len(text)):
        if (i < len(text)-1) and (text[i] == 0):                    # Step 3.1: Check if the current loop index is not greater than |text|-1 and the element is not zero.
            N_zero += 1                                             # Step 3.1.1: If the element is equal to zero, increment N_zero.
        else:
            N_bin = bin(N_zero+1)[2:]                               # Step 3.1.2.1 : Convert N_zero to binary and add one. 

            for k in range(len(N_bin)-1):
                L.append(int(N_bin[len(N_bin)-k-1]))                # Step 3.1.2.2 : Push each digit starting from the LSB bit into L except the MSB.
            
            N_zero = 0                                              # Step 3.1.2.3: Reset N_zero to zero.
            
            L.append(text[i]+2)                                     # Step 3.1.2.4: Push element+2 into L.

    return L                                                        # Step 4: Return the output queue.


def decode(data: list[int]) -> list[int]:
    '''
    Steps in Decoding for RLE:
    1. Initialize a stack, N_zero.
        - Contains the binary representation of the current numebr of zeros that were encoded.
    2. Initialize an output queue S.
    3. Get an array of numbers, data, and do the following |text|+1 times.
        - Check if the current loop index is not greater than |text|-1 and the element is not zero.
            - If the element is equal to zero, prepend the element into N_zero.
            - Otherwise,
                - Prepend a one into N_zero, convert it to its decimal equivalent and subtract by 1.
                - Push the appropriate numebr of zeros equivalent to the new N_zero amount to S.
                - Reset N_zero to zero.
                - Push element-2 into L.
    4. Return the output queue.
    '''

    N_zero = []                                                     # Step 1: Initialize a stack, N_zero.
    S = []                                                          # Step 2: Initialize an output queue S.

    for i in range(len(data)):
        if (i < len(data)-1) and (data[i] == 0 or data[i] == 1):    # Step 3.1.1: If the element is equal to zero, prepend the element into N_zero.
            N_zero.insert(0,str(data[i]))
        else:
            N_zero.insert(0,"1")                                    # Step 3.1.2.1: Prepend a one into N_zero, convert it to its decimal equivalent and subtract by 1.
            N_bin = "".join(N_zero)
            N_int = int(N_bin,2) - 1

            for k in range(N_int):                                  # Step 3.1.2.2: Push the appropriate numebr of zeros equivalent to the new N_zero amount to S.
                S.append(0)
            
            N_zero = []                                             # Step 3.1.2.3: Reset N_zero to zero.

            S.append(data[i]-2)                                     # Step 3.1.2.4: Push element-2 into L.

    return S                                                        # Step 4: Return the output queue.


#Test Classes
#The test cases were manually created by determining the length of the argument list, constructing the RLE table, and counting zeroes and adding twos, via MS Excel
class encode_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = [3, 3, 4, 1, 1, 1, 0, 0, 4, 4]
        Expected_Output_1 = [5, 5, 6, 3, 3, 3, 1, 6, 6]
        Test_Case_2 = [4, 6, 7, 0, 8, 7, 6, 10, 3, 10, 5, 10, 10, 10]
        Expected_Output_2 = [6, 8, 9, 0, 10, 9, 8, 12, 5, 12, 7, 12, 12, 12]
        
        #Function call
        Output_1 = encode(Test_Case_1)
        Output_2 = encode(Test_Case_2)
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        pass

class decode_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = [5, 5, 6, 3, 3, 3, 1, 6, 6]
        Expected_Output_1 = [3, 3, 4, 1, 1, 1, 0, 0, 4, 4]
        Test_Case_2 = [6, 8, 9, 0, 10, 9, 8, 12, 5, 12, 7, 12, 12, 12]
        Expected_Output_2 = [4, 6, 7, 0, 8, 7, 6, 10, 3, 10, 5, 10, 10, 10]
        
        #Function call
        Output_1 = decode(Test_Case_1)
        Output_2 = decode(Test_Case_2)
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        pass
    
# unittest.main(verbosity=2)