'''
Created on Apr 29, 2011

@author: Jim
'''
import unittest
from main import BenfordSingle, BenfordDouble

class Test(unittest.TestCase):

    def test_single_table(self):
        data = "1\n1\n1\n2\n2\n3\n4\n5\n6\nasdfasdfadsa7f \n"
        ben = BenfordSingle()
        table = ben.get_table(data)
        self.assertEqual(table[0][0], 1)
        self.assertEqual(table[8][0], 9)
        self.assertEqual(table[0][1], 30.1)
        self.assertEqual(table[8][1], 4.6)
        self.assertEqual(table[0][2], 30)
        self.assertEqual(table[8][2], 0)
        self.assertAlmostEqual(table[0][3], 0.1, 3)
        self.assertAlmostEqual(table[8][3], 4.6, 3)
    
    def test_double(self):
        pass
    
    def test_split_data(self):
        ben = BenfordDouble()
        output = ben.split_data("Jim, $1,233.00")
        self.assertEqual("Jim", output[0])
        self.assertEqual("1", output[1])
        output = ben.split_data("Jim,")
        self.assertEqual(None, output)
        output = ben.split_data("")
        self.assertEqual(None, output)
        
        lines = "Jim, $1,233.00\n\n\3\nJim\nJim, 2,300".splitlines()
        table = map(ben.split_data, lines)
        table = filter(lambda x: x != None, table)
        self.assertEqual(2, len(table))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()