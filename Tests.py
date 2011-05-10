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
        data = "Jim, 100\n\nDave, $4,400\n\n3\nJim, 200\n\nJim,\n\nDave, 200"
        ben = BenfordDouble()
        table = ben.get_table(data)
        self.assertEqual("Digits", table[0][0])
        self.assertEqual(1, table[0][1])
        self.assertEqual(9, table[0][9])
        self.assertEqual("Benford", table[1][0])
        self.assertEqual(30.1, table[1][1])
        self.assertEqual(4.6, table[1][9])
        self.assertEqual("Dave", table[2][0])
        self.assertEqual(50, table[2][2])
        self.assertEqual("Jim", table[3][0])
        self.assertEqual(50, table[3][1])
        self.assertEqual(0, table[3][3])
    
    def test_flip(self):
        table = [[1, 2, 3],['A','B','C']]
        ben = BenfordDouble()
        flipped = ben.flip_table(table)
        self.assertEqual(1, flipped[0][0])
        self.assertEqual(2, flipped[1][0])
        self.assertEqual(3, flipped[2][0])
        self.assertEqual('A', flipped[0][1])
        self.assertEqual('B', flipped[1][1])
        self.assertEqual('C', flipped[2][1])
    
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