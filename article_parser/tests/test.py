import json
import unittest
from article_parser import transform

class Tester(unittest.TestCase):
    def test(self):
        transform('tests/input.json', 'tests/output.json')
        with open('tests/output.json', 'r') as foutput:
            with open('tests/expected.json', 'r') as fexpected:
                data = json.load(foutput)
                expected = json.load(fexpected)
                assert data == expected
