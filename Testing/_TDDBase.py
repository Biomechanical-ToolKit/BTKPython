import unittest

import NodeTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NodeTest.NodeTest))
    return suite