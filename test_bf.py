# -*- coding: utf-8 -*

import unittest
from bf import EvalError, _clean_source, _bracketmap, bfeval


class TestBF(unittest.TestCase):

    def test_codecleaning(self):

        codemap = {
            ".": ".",
            "<": "<",
            ">": ">",
            "+": "+",
            "-": "-",
            "[": "[",
            "]": "]",
            ",": "",
            "lorem ipsum": "",
            "abcde.<>+-[]abcde": ".<>+-[]",
            "": ""
        }

        for key, value in codemap.iteritems():
            self.assertEqual(_clean_source(key), value)

    def test_bracketbalance(self):

        codelist = ("[[]", "[]]", "][")

        for item in codelist:
            self.assertRaises(EvalError, _bracketmap, item)

    def test_bracketmap(self):

        codemap = {
            "...[..[....]...]..": ((3, 15), (6, 11)),
            "[]": ((0, 1),)
        }

        for code, pairlist in codemap.iteritems():
            bm = _bracketmap(code)
            for pair in pairlist:
                self.assertEqual(bm[pair[0]], pair[1])
                self.assertEqual(bm[pair[1]], pair[0])

        bm = _bracketmap("")
        self.assertEqual(len(bm), 0)

    def test_helloworld(self):

        code = ("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++.."
                "+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.")

        self.assertEqual(bfeval(code), "Hello World!")

    def test_emptycode(self):
        bfeval("")


if __name__ == "__main__":
    unittest.main()

