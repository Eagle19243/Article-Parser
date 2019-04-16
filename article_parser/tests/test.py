import json
import unittest
from article_parser import transform, parse_one


class Tester(unittest.TestCase):
    def test_json(self):
        transform('tests/input.json', 'tests/output.json')
        with open('tests/output.json', 'r') as foutput:
            with open('tests/expected.json', 'r') as fexpected:
                data = json.load(foutput)
                expected = json.load(fexpected)
                assert data == expected

    def test_regular(self):
        txt = (
            'placeholder text at the beginning'
            '<img a="1" b="2" alt="placeholder" src="#">'
            '<p>This is the caption</p>'
        )
        ans = (
            'placeholder text at the beginning'
            '<div class="image"><img alt="placeholder" src="#"/>'
            '<p class="caption">This is the caption</p></div>'
        )
        assert parse_one(txt) == ans

    def test_img_wrapped(self):
        txt = (
            'placeholder text at the beginning'
            '<div class="test"><img a="1" b="2" alt="placeholder" src="#"></div>'
            '<p>This is the caption</p>'
        )
        ans = (
            'placeholder text at the beginning'
            '<div class="test"><div class="image"><img alt="placeholder" src="#"/>'
            '<p class="caption">This is the caption</p></div></div>'
        )
        assert parse_one(txt) == ans

    def test_caption_wrapped(self):
        txt = (
            'placeholder text at the beginning'
            '<div class="test"><img a="1" b="2" alt="placeholder" src="#"></div>'
            '<em><p>This is the caption</p></em>'
        )
        ans = (
            'placeholder text at the beginning'
            '<div class="test"><div class="image"><img alt="placeholder" src="#"/>'
            '<p class="caption">This is the caption</p></div></div>'
        )
        assert parse_one(txt) == ans

    def test_multiline(self):
        txt = (
            '<a></a>\n<a></a>\n<p>Some text....</p>\n'
            '<div class="test"><img a="1" b="2" alt="placeholder" src="#"></div>'
            '\n\n\n<em><p>This is the caption</p></em>'
        )
        ans = (
            '<a></a>\n<a></a>\n<p>Some text....</p>\n'
            '<div class="test"><div class="image"><img alt="placeholder" src="#"/>'
            '<p class="caption">This is the caption</p></div></div>'
        )
        assert parse_one(txt) == ans
