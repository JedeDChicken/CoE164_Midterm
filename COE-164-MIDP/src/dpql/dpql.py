# src/dpql/dpql.py
import unittest
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath("COE-164-MIDP"))))
sys.path.append(root_folder)

def write(text: str) -> str:
    #Convert "text" into a diropql program that outputs "text" and returns it
    dpql_prog = ""

    for character in text:
        ascii_code = ord(character)
        if ascii_code <= 128:
            dpql_prog += "i" * ascii_code
        else:
            dpql_prog += "d" * (255 - ascii_code)
        dpql_prog += "or"

    return dpql_prog

def read(prog: str) -> str:
    #Read "prog" as a diropql program, interpret it, and return the contents of the output queue
    mem_cell = [0] * 10000
    mp, ip = 0, 0
    oq, p_ip, q_ip = [], [], []
    next_ip = False
    prog_chars = list(prog)

    while ip < len(prog_chars):
        cmd = prog_chars[ip]

        if cmd == 'i' and not next_ip:
            if mem_cell[mp] == 255:
                mem_cell[mp] = 0
            else:
                mem_cell[mp] += 1
        elif cmd == 'd' and not next_ip:
            if mem_cell[mp] == 0:
                mem_cell[mp] = 255
            else:
                mem_cell[mp] -= 1
        elif cmd == 'r' and not next_ip:
            if mp == 9999:
                mp = 0
            else:
                mp += 1
        elif cmd == 'l' and not next_ip:
            if mp == 0:
                mp = 9999
            else:
                mp -= 1
        elif cmd == 'o' and not next_ip:
            ascii_char = chr(mem_cell[mp])
            oq.append(ascii_char)
        elif cmd == 'p':
            p_ip.append(ip)
            if mem_cell[mp] == 0:
                if not next_ip:
                    next_ip = True
            else:
                pass
        elif cmd == 'q':
            q_ip.append(ip)
            if next_ip == True:
                if len(p_ip) == len(q_ip):
                    p_ip.clear()
                    q_ip.clear()
                    next_ip == False
                elif mem_cell[mp] != 0:
                    ip = p_ip.pop()
                    p_ip.append(ip)
                    q_ip.pop()
                else:
                    pass
        ip += 1

    read_output = ''.join(str(element) for element in oq)
    return read_output


#Test Classes
#ASCII Table from- http://facweb.cs.depaul.edu/sjost/it212/documents/ascii-pr.htm, and- https://www.ascii-code.com/
#The test cases were manually created by appending n i's for each character in text, where n is the ASCII decimal, and also appending or's in between characters to indicate push to oq and move mp
class write_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = "bananaaa!"
        Expected_Output_1 = 98*"i" + "or" + 97*"i" + "or" + 110*"i" + "or" + 97*"i" + "or" + 110*"i" + "or" + 97*"i" + "or" + 97*"i" + "or" + 97*"i" + "or" + 33*"i" + "or"
        Test_Case_2 = "Hello, world!"
        Expected_Output_2 = 72*"i" + "or" + 101*"i" + "or" + 108*"i" + "or" + 108*"i" + "or" + 111*"i" + "or" + 44*"i" + "or" + 32*"i" + "or" + 119*"i" + "or" + 111*"i" + "or" + 114*"i" + "or" + 108*"i" + "or" + 100*"i" + "or" + 33*"i" + "or"
        Test_Case_3 = "dddddiiirrrroopppppqqqllll"
        Expected_Output_3 = 5*(100*"i" + "or") + 3*(105*"i" + "or") + 4*(114*"i" + "or") + 2*(111*"i" + "or") + 5*(112*"i" + "or") + 3*(113*"i" + "or") + 4*(108*"i" + "or")
        
        #Function Calls
        Output_1 = write(Test_Case_1)
        Output_2 = write(Test_Case_2)
        Output_3 = write(Test_Case_3)
        
        #Assertions
        self.assertEqual(Output_1, Expected_Output_1)
        self.assertEqual(Output_2, Expected_Output_2)
        self.assertEqual(Output_3, Expected_Output_3)
        pass

class read_test(unittest.TestCase):
    def test_basic(self):
        Test_Case_1 = 98*"i" + "or" + 97*"i" + "or" + 110*"i" + "or" + 97*"i" + "or" + 110*"i" + "or" + 97*"i" + "or" + 97*"i" + "or" + 97*"i" + "or" + 33*"i" + "or"
        Expected_Output_1 = "bananaaa!"
        Test_Case_2 = 72*"i" + "or" + 101*"i" + "or" + 108*"i" + "or" + 108*"i" + "or" + 111*"i" + "or" + 44*"i" + "or" + 32*"i" + "or" + 119*"i" + "or" + 111*"i" + "or" + 114*"i" + "or" + 108*"i" + "or" + 100*"i" + "or" + 33*"i" + "or"
        Expected_Output_2 = "Hello, world!"
        Test_Case_3 = 5*(100*"i" + "or") + 3*(105*"i" + "or") + 4*(114*"i" + "or") + 2*(111*"i" + "or") + 5*(112*"i" + "or") + 3*(113*"i" + "or") + 4*(108*"i" + "or")
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
    
# unittest.main(verbosity=2)