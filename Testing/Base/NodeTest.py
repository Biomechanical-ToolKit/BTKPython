from _btk import btkBase
import unittest

class NodeTest(unittest.TestCase):
    def test_Constructor(self):
        test = btkBase.btkNode('test')
        self.assertEqual(test.name(), 'test')