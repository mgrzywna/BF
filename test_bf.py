# -*- coding: utf-8 -*-

import unittest
from itertools import repeat
from bf import EvalError, _clean_source, _bracketmap, bfeval


class TextAccumulator(object):

    def __init__(self):
        self.result = []

    def __call__(self, text):
        self.result.append(text)

    def get(self):
        return "".join(self.result)


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
            ",": ",",
            "lorem ipsum": "",
            "abcde.,<>+-[]abcde": ".,<>+-[]",
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

        acc = TextAccumulator()
        bfeval(code, output_callback = acc)
        self.assertEqual(acc.get(), "Hello World!")


    def test_emptycode(self):
        acc = TextAccumulator()
        bfeval("", output_callback = acc)
        self.assertEqual(acc.get(), "")


    def test_cells(self):
        cell_size = 256
        code = ["+" * 67, ".--.", "+" * (cell_size + 1), ".", "-" * (cell_size - 2), "."]
        code = "".join(code)
        acc = TextAccumulator()
        bfeval(code, output_callback = acc)
        self.assertEqual(acc.get(), "CABD")


    def test_memory(self):
        memory_size = 1024
        code = ">" * (memory_size - 1)
        bfeval(code, memory_size = memory_size)
        code = ">" * memory_size
        self.assertRaises(EvalError, bfeval, code, memory_size = memory_size)


if __name__ == "__main__":
    unittest.main()

