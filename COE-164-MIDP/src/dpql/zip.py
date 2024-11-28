# src/dpql/zip.py
import unittest
import base64
# import bwt, mtf, rle, huffman
# from modules import dpql, compressor
import os, sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath("COE-164-MIDP"))))
root_folder_compressor = root_folder + "\COE-164-MIDP\src\compressor"
sys.path.insert(0, root_folder_compressor)

root_folder_diro = root_folder + "\COE-164-MIDP\src\dpql"
sys.path.insert(0, root_folder_diro)

import bwt as bwt
import mtf as mtf
import rle as rle
import huffman as huffman
import dpql as dpql

"""
#Get Directory
path = os.getcwd()
filename = 'dpql.py'
filepath = os.path.join(path, filename)
print(filepath)

#Access File
sys.path.insert(1, 'c://Users//danie//Desktop//Codes//Python//164MP//dpql.py')
import dpql

#print(dpql.encode("hello"))
"""

class DpqlzMeta:
    def __init__(self, mlen: int, moffset: int, bwt_idx: int, huf_bitlens: list[int]):
        self.mlen = mlen                    #Length of the obfuscated message "msg" in bytes
        self.moffset = moffset              #Number of bits to exclude or ignore from the end of "msg"
        self.bwt_idx = bwt_idx              #Suffix index associated with the Burrows_Wheeler transform
        self.huf_bitlens = huf_bitlens       #List of 1-byte numbers corresponding to the bit lengths of the derived canonical Huffman codebook

def write(text: str) -> str:
    #Convert "text" into a diropqlz program that outputs "text" and returns it
    diropql_prog = dpql.write(text)
    bwt_encoded, bwt_idx = bwt.encode(diropql_prog)
    mtf_encoded = mtf.encode(bwt_encoded, ['\0','d', 'i', 'l', 'o', 'p', 'q', 'r'])
    rle_encoded = rle.encode(mtf_encoded)
    huff_encoded, huff_bitlens = huffman.encode(rle_encoded)

    moffset = 8 - (len(huff_encoded) % 8)
    mlen = (len(huff_encoded) + moffset) // 8

    meta = DpqlzMeta(mlen, moffset, bwt_idx, huff_bitlens)
    diropqlz = write_with_meta(meta, huff_encoded)

    return diropqlz


def read(prog: str) -> str:
    #Read "prog" as a dirpqlz program, decompress it, interpret it, and return the contents of the output queue
    meta, compressed_prog = read_with_meta(prog)[0], read_with_meta(prog)[1]
    huff_decoded = huffman.decode(compressed_prog, meta.huf_bitlens)
    rle_decoded = rle.decode(huff_decoded)
    mtf_decoded = mtf.decode(rle_decoded, ['\0','d', 'i', 'l', 'o', 'p', 'q', 'r'])
    bwt_decoded = bwt.decode(mtf_decoded, meta.bwt_idx)
    input_str = dpql.read(str(bwt_decoded))

    return input_str


def write_with_meta(meta: DpqlzMeta, prog: list[int]) -> str:
    #Create and return a diropqlz program using "meta" as the metadata and "prog" as a compressed diropql program
    diropqlz_prog = ''
    mlen = meta.mlen
    moffset = meta.moffset
    bwt_idx = meta.bwt_idx
    huffman = meta.huf_bitlens

    mlen_64prog_str = str(format(mlen, '064b'))
    diropqlz_prog += mlen_64prog_str

    moffset_8prog_str = str(format(moffset, '08b'))
    diropqlz_prog += moffset_8prog_str

    bwt_idx_64prog_str = str(format(bwt_idx, '064b'))
    diropqlz_prog += bwt_idx_64prog_str

    for element in huffman:
        element_8prog_str = str(format(element, '08b'))
        diropqlz_prog += element_8prog_str

    for _ctr in range(6):
        element = 0
        element_8prog_str = str(format(element, '08b'))
        diropqlz_prog += element_8prog_str

    for bit in prog:
        bit_string = str(bit)
        diropqlz_prog += bit_string

    add_zero = 0
    while add_zero < moffset:
        diropqlz_prog += '0'
        add_zero += 1

    diropqlz_to_bytes = []
    byte_string = ""
    for character in diropqlz_prog:
        byte_string += str(character)
        if len(byte_string) == 8:  # append until length is 8 to form a byte
            dec_value = int(byte_string, 2)
            diropqlz_to_bytes.append(dec_value)
            byte_string = ""

    base85_diropqlz_prog = base64.b85encode(bytes(diropqlz_to_bytes)).decode('ascii')
    diropqlz_prog_with_meta = "DIROPQLZ" + base85_diropqlz_prog

    return diropqlz_prog_with_meta


def read_with_meta(prog: str) -> tuple[DpqlzMeta, list[int]]:
    #Read "prog" as a diropqlz program and output its metadata and resulting compressed program as a vector of bits, respectively.
    encoded_prog = prog[8:]
    decoded_bytes = list(base64.b85decode(encoded_prog))
    decoded_base85 = "".join(format(byte, "08b") for byte in decoded_bytes)

    mlen_str = decoded_base85[:64]
    moffset_str = decoded_base85[64:72]
    bwt_idx_str = decoded_base85[72:136]
    huffman_str = decoded_base85[136:264]
    obfuscated_str = decoded_base85[264:]

    mlen = int(mlen_str, 2)
    moffset = int(moffset_str, 2)
    bwt_idx = int(bwt_idx_str, 2)

    huffman_bitlens = []
    for i in range(10):
        huff = int(huffman_str[i * 8:(i+1) * 8], 2)
        huffman_bitlens.append(huff)

    prog = [int(binary_digit) for binary_digit in obfuscated_str]
    last_idx = int(mlen * 8 - moffset)
    compressed_prog = prog[:last_idx]

    return (DpqlzMeta(mlen, moffset, bwt_idx, huffman_bitlens), compressed_prog)


#Test Classes
#Basically, the write() and read() functions just set or extract the properties of a DpqlzMeta instance, as well as create or decode a compressed obfuscated msg. 
#They also call the x_with_meta() functions. We can utilize the other modules and submodules as they were already tested thrice.
class write_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = "bananaaa!"
        from_dpql_write_1 = 98*"i" + "or" + 97*"i" + "or" + 110*"i" + "or" + 97*"i" + "or" + 110*"i" + "or" + 97*"i" + "or" + 97*"i" + "or" + 97*"i" + "or" + 33*"i" + "or"
        bwt_1 = bwt.encode(from_dpql_write_1)
        mtf_1 = mtf.encode(bwt_1[0], ['\x00', 'd', 'i', 'l', 'o', 'p', 'q', 'r'])
        rle_1 = rle.encode(mtf_1)
        huffman_1 = huffman.encode(rle_1)
        mlen_1 = (len(huffman_1[0]) + 8 - (len(huffman_1[0]) % 8)) // 8
        moffset_1 = 8 - (len(huffman_1[0]) % 8)
        instance_1 = DpqlzMeta(mlen_1, moffset_1, bwt_1[1], huffman_1[1])
        Expected_Output_1 = write_with_meta(instance_1, huffman_1[0])           #DIROPQLZ000000000C1poj500000836(Y0|W*D1^@;C000000RHt(&TCjzTSAYAfB
        
        Test_Case_2 = "Hello, world!"
        from_dpql_write_2 = 72*"i" + "or" + 101*"i" + "or" + 108*"i" + "or" + 108*"i" + "or" + 111*"i" + "or" + 44*"i" + "or" + 32*"i" + "or" + 119*"i" + "or" + 111*"i" + "or" + 114*"i" + "or" + 108*"i" + "or" + 100*"i" + "or" + 33*"i" + "or"
        bwt_2 = bwt.encode(from_dpql_write_2)
        mtf_2 = mtf.encode(bwt_2[0], ['\x00', 'd', 'i', 'l', 'o', 'p', 'q', 'r'])
        rle_2 = rle.encode(mtf_2)
        huffman_2 = huffman.encode(rle_2)
        mlen_2 = (len(huffman_2[0]) + 8 - (len(huffman_2[0]) % 8)) // 8
        moffset_2 = 8 - (len(huffman_2[0]) % 8)
        instance_2 = DpqlzMeta(mlen_2, moffset_2, bwt_2[1], huffman_2[1])
        Expected_Output_2 = write_with_meta(instance_2, huffman_2[0])           #DIROPQLZ000000000M1^@s600001Qvv}70|W*D1^@;C000000RHuDTU$$8V74uk9f+&6Ce+xHeNO-
        
        Test_Case_3 = "dddddiiirrrroopppppqqqllll"
        from_dpql_write_3 = 5*(100*"i" + "or") + 3*(105*"i" + "or") + 4*(114*"i" + "or") + 2*(111*"i" + "or") + 5*(112*"i" + "or") + 3*(113*"i" + "or") + 4*(108*"i" + "or")
        bwt_3 = bwt.encode(from_dpql_write_3)
        mtf_3 = mtf.encode(bwt_3[0], ['\x00', 'd', 'i', 'l', 'o', 'p', 'q', 'r'])
        rle_3 = rle.encode(mtf_3)
        huffman_3 = huffman.encode(rle_3)
        mlen_3 = (len(huffman_3[0]) + 8 - (len(huffman_3[0]) % 8)) // 8
        moffset_3 = 8 - (len(huffman_3[0]) % 8)
        instance_3 = DpqlzMeta(mlen_3, moffset_3, bwt_3[1], huffman_3[1])
        Expected_Output_3 = write_with_meta(instance_3, huffman_3[0])           #DIROPQLZ000000000L1poj500000`T+t40|W*D1^@;C000000RDSs+S!a*m2E9$8$&cp9l}C=7k~
        
        #Function Calls
        Output_1 = write(Test_Case_1)
        Output_2 = write(Test_Case_2)
        Output_3 = write(Test_Case_3)
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_3, Expected_Output_3)
        pass
    
#Must obtain original msg
class read_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = "DIROPQLZ000000000C1poj500000836(Y0|W*D1^@;C000000RHt(&TCjzTSAYAfB"
        Expected_Output_1 = "bananaaa!"
        Test_Case_2 = "DIROPQLZ000000000M1^@s600001Qvv}70|W*D1^@;C000000RHuDTU$$8V74uk9f+&6Ce+xHeNO-"
        Expected_Output_2 = "Hello, world!"
        Test_Case_3 = "DIROPQLZ000000000L1poj500000`T+t40|W*D1^@;C000000RDSs+S!a*m2E9$8$&cp9l}C=7k~"
        Expected_Output_3 = "dddddiiirrrroopppppqqqllll"
        
        #Function Calls
        Output_1 = read(Test_Case_1)
        Output_2 = read(Test_Case_2)
        Output_3 = read(Test_Case_3)
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_3, Expected_Output_3)
        pass

#The x_with_meta test cases were manually created by utilizing the compression submodules, converting the DpqlzMeta arguments to their respective bit formats, 
#appending zeroes, grouping the bits by 32, using the Base 85 formula to convert each group to a five-character sequence, and also appending DIROPQLZ at start
#For read, each character in the function argument represents a single byte. The metadata and Huffman representation were obtained using the compression modules.
#For read, we compare the properties of instance to the ones obtained using the compression modules, as well as the Huffman representation list.
class write_with_meta_test(unittest.TestCase):
    def test_basic(self):
        """
        Taking advantage of the fact that the arguments for this function are taken from the four compression submodules, 
        and that the compression functions were already verified using three cases, we can utilize the created compression 
        functions to generate the arguments.
        """
        text_1 = 5*"bananaaa!"
        bwt_call_1 = bwt.encode(text_1)
        mtf_call_1 = mtf.encode(bwt_call_1[0], ['\x00', '!', 'a', 'b', 'n'])
        rle_call_1 = rle.encode(mtf_call_1)
        huffman_call_1 = huffman.encode(rle_call_1)
        dpqlz_arg1_1 = (len(huffman_call_1[0]) + 8 - (len(huffman_call_1[0]) % 8)) // 8
        dpqlz_arg2_1 = 8 - (len(huffman_call_1[0]) % 8)    
        arg1_1 = DpqlzMeta(dpqlz_arg1_1, dpqlz_arg2_1, bwt_call_1[1], huffman_call_1[1])
        Test_Case_1 = (arg1_1, huffman_call_1[0])
        Expected_Output_1 = "DIROPQLZ00000000071^@s600000BLV^h1Ox;E00000000000Nz#-PYOc-"
        
        text_2 = 5*"Hello, world!"
        bwt_call_2 = bwt.encode(text_2)
        mtf_call_2 = mtf.encode(bwt_call_2[0], ['\x00', ' ', '!', ',', 'H', 'd', 'e', 'l', 'o', 'r', 'w'])
        rle_call_2 = rle.encode(mtf_call_2)
        huffman_call_2 = huffman.encode(rle_call_2)
        dpqlz_arg1_2 = (len(huffman_call_2[0]) + 8 - (len(huffman_call_2[0]) % 8)) // 8
        dpqlz_arg2_2 = 8 - (len(huffman_call_2[0]) % 8)    
        arg1_2 = DpqlzMeta(dpqlz_arg1_2, dpqlz_arg2_2, bwt_call_2[1], huffman_call_2[1])
        Test_Case_2 = (arg1_2, huffman_call_2[0])
        Expected_Output_2 = "DIROPQLZ000000000E0RR91000006afMT00smG1^@*B000000QV>Ja}T#QIXN*qH9B|"
        
        text_3 = 5*"dddddiiirrrroopppppqqqllll"
        bwt_call_3 = bwt.encode(text_3)
        mtf_call_3 = mtf.encode(bwt_call_3[0], ['\x00', 'd', 'i', 'l', 'o', 'p', 'q', 'r'])
        rle_call_3 = rle.encode(mtf_call_3)
        huffman_call_3 = huffman.encode(rle_call_3)
        dpqlz_arg1_3 = (len(huffman_call_3[0]) + 8 - (len(huffman_call_3[0]) % 8)) // 8
        dpqlz_arg2_3 = 8 - (len(huffman_call_3[0]) % 8)    
        arg1_3 = DpqlzMeta(dpqlz_arg1_3, dpqlz_arg2_3, bwt_call_3[1], huffman_call_3[1])
        Test_Case_3 = (arg1_3, huffman_call_3[0])
        Expected_Output_3 = "DIROPQLZ000000000F1^@s6000001pxvF1qTBF1_cEG000000Mno1$*S!1>UfzsHD4cq"
        
        #Function Calls
        Output_1 = write_with_meta(Test_Case_1[0], Test_Case_1[1])
        Output_2 = write_with_meta(Test_Case_2[0], Test_Case_2[1])
        Output_3 = write_with_meta(Test_Case_3[0], Test_Case_3[1])
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_3, Expected_Output_3)
        pass
    
class read_with_meta_test(unittest.TestCase):
    def test_basic(self):
        text_1 = 5*"bananaaa!"
        bwt_call_1 = bwt.encode(text_1)
        mtf_call_1 = mtf.encode(bwt_call_1[0], ['\x00', '!', 'a', 'b', 'n'])
        rle_call_1 = rle.encode(mtf_call_1)
        huffman_call_1 = huffman.encode(rle_call_1)
        dpqlz_arg1_1 = (len(huffman_call_1[0]) + 8 - (len(huffman_call_1[0]) % 8)) // 8
        dpqlz_arg2_1 = 8 - (len(huffman_call_1[0]) % 8)    
        arg1_1 = DpqlzMeta(dpqlz_arg1_1, dpqlz_arg2_1, bwt_call_1[1], huffman_call_1[1])
        Test_Case_1 = "DIROPQLZ00000000071^@s600000BLV^h1Ox;E00000000000Nz#-PYOc-"
        Expected_Output_1 = huffman_call_1[0]
        Expected_Output_1_1 = dpqlz_arg1_1
        Expected_Output_2_1 = dpqlz_arg2_1
        Expected_Output_3_1 = bwt_call_1[1]
        Expected_Output_4_1 = huffman_call_1[1]
        
        text_2 = 5*"Hello, world!"
        bwt_call_2 = bwt.encode(text_2)
        mtf_call_2 = mtf.encode(bwt_call_2[0], ['\x00', ' ', '!', ',', 'H', 'd', 'e', 'l', 'o', 'r', 'w'])
        rle_call_2 = rle.encode(mtf_call_2)
        huffman_call_2 = huffman.encode(rle_call_2)
        dpqlz_arg1_2 = (len(huffman_call_2[0]) + 8 - (len(huffman_call_2[0]) % 8)) // 8
        dpqlz_arg2_2 = 8 - (len(huffman_call_2[0]) % 8)    
        arg1_2 = DpqlzMeta(dpqlz_arg1_2, dpqlz_arg2_2, bwt_call_2[1], huffman_call_2[1])
        Test_Case_2 = "DIROPQLZ000000000E0RR91000006afMT00smG1^@*B000000QV>Ja}T#QIXN*qH9B|"
        Expected_Output_2 = huffman_call_2[0]
        Expected_Output_1_2 = dpqlz_arg1_2
        Expected_Output_2_2 = dpqlz_arg2_2
        Expected_Output_3_2 = bwt_call_2[1]
        Expected_Output_4_2 = huffman_call_2[1]
        
        text_3 = 5*"dddddiiirrrroopppppqqqllll"
        bwt_call_3 = bwt.encode(text_3)
        mtf_call_3 = mtf.encode(bwt_call_3[0], ['\x00', 'd', 'i', 'l', 'o', 'p', 'q', 'r'])
        rle_call_3 = rle.encode(mtf_call_3)
        huffman_call_3 = huffman.encode(rle_call_3)
        dpqlz_arg1_3 = (len(huffman_call_3[0]) + 8 - (len(huffman_call_3[0]) % 8)) // 8
        dpqlz_arg2_3 = 8 - (len(huffman_call_3[0]) % 8)    
        arg1_3 = DpqlzMeta(dpqlz_arg1_3, dpqlz_arg2_3, bwt_call_3[1], huffman_call_3[1])
        Test_Case_3 = "DIROPQLZ000000000F1^@s6000001pxvF1qTBF1_cEG000000Mno1$*S!1>UfzsHD4cq"
        Expected_Output_3 = huffman_call_3[0]
        Expected_Output_1_3 = dpqlz_arg1_3
        Expected_Output_2_3 = dpqlz_arg2_3
        Expected_Output_3_3 = bwt_call_3[1]
        Expected_Output_4_3 = huffman_call_3[1]
        
        #Function Calls
        Output_1 = read_with_meta(Test_Case_1)[1]
        Output_1_1 = read_with_meta(Test_Case_1)[0].mlen
        Output_2_1 = read_with_meta(Test_Case_1)[0].moffset
        Output_3_1 = read_with_meta(Test_Case_1)[0].bwt_idx
        Output_4_1 = read_with_meta(Test_Case_1)[0].huf_bitlens
        
        Output_2 = read_with_meta(Test_Case_2)[1]
        Output_1_2 = read_with_meta(Test_Case_2)[0].mlen
        Output_2_2 = read_with_meta(Test_Case_2)[0].moffset
        Output_3_2 = read_with_meta(Test_Case_2)[0].bwt_idx
        Output_4_2 = read_with_meta(Test_Case_2)[0].huf_bitlens
        
        Output_3 = read_with_meta(Test_Case_3)[1]
        Output_1_3 = read_with_meta(Test_Case_3)[0].mlen
        Output_2_3 = read_with_meta(Test_Case_3)[0].moffset
        Output_3_3 = read_with_meta(Test_Case_3)[0].bwt_idx
        Output_4_3 = read_with_meta(Test_Case_3)[0].huf_bitlens
    
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_1_1, Expected_Output_1_1)
        self.assertEqual(Output_2_1, Expected_Output_2_1)
        self.assertEqual(Output_3_1, Expected_Output_3_1)
        self.assertEqual(Output_4_1, Expected_Output_4_1)
        
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_1_2, Expected_Output_1_2)
        self.assertEqual(Output_2_2, Expected_Output_2_2)
        self.assertEqual(Output_3_2, Expected_Output_3_2)
        self.assertEqual(Output_4_2, Expected_Output_4_2)
        
        self.assertEqual(Output_3, Expected_Output_3)
        self.assertEqual(Output_1_3, Expected_Output_1_3)
        self.assertEqual(Output_2_3, Expected_Output_2_3)
        self.assertEqual(Output_3_3, Expected_Output_3_3)
        self.assertEqual(Output_4_3, Expected_Output_4_3)
        pass

# unittest.main(verbosity=2)