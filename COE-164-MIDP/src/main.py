# src/main.py
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath("COE-164-MIDP"))))        # Obtain the path for the folder \COE-164-MIDP
root_folder_compressor = root_folder + "\COE-164-MIDP\src\compressor"
sys.path.insert(0, root_folder_compressor)                                                              # Append the path for the compressor folder in sys.path

root_folder_diro = root_folder + "\COE-164-MIDP\src\dpql"
sys.path.insert(0, root_folder_diro)                                                                    # Append the path for the diropql folder in sys.path

import bwt as bwt
import mtf as mtf
import rle as rle
import huffman as huffman
import dpql as dpql
import zip as zip

def test_encode():
    '''
    Test call for the Obfuscator.
    - Uses the text "Hello, World!"
    - Uses zip.write() to obtain the obfuscated and zipped message.
    - Must return "DIROPQLZ000000000M1^@s600001GXVky0|W*D1^@;C000000R8K2t2V-Hn?Y?zcBKx=mc-hGzApd".
    '''

    text = "Hello, World!"
    dpqlz_text = zip.write(text)

    print("Input text: ",text)
    print("Encoded and zipped text: ")
    print(" ",dpqlz_text)

def test_decode():
    '''
    Test call for the Obfuscator.
    - Uses the text "DIROPQLZ000000000M1^@s600001GXVky0|W*D1^@;C000000R8K2t2V-Hn?Y?zcBKx=mc-hGzApd"
    - Uses zip.read() to obtain the unzipped and deobfuscated message.
    - Must return "Hello, World!"
    '''

    text = "DIROPQLZ000000000M1^@s600001GXVky0|W*D1^@;C000000R8K2t2V-Hn?Y?zcBKx=mc-hGzApd"
    orig_text = zip.read(text)

    print("Input text: ",text)
    print("Unzipped and decoded text: ")
    print(" ",orig_text)

def main():
    '''
    Main function for running the test function calls.
    '''

    print("Testing Message Obfuscator:")
    print()
    test_encode()
    
    print("------------------------------")

    print("Testing Message Deobfuscator")
    print()
    test_decode()

main()                                                                                                  # Run the main() function.