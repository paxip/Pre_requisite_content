from celebrities_births import Date
import unittest
from hypothesis import given
import hypothesis.strategies as st


class Date(unittest.TestCase):
    def test__str__(self):
        date = Date(27, 3, 1991)
        date.__str__(date)
        self.assertMultiLineEqual("27-3-1991","27-3-1991")
        
        
