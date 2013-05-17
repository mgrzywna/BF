# -*- coding: utf-8 -*-

"""
BF interpreter

Cells are one byte integers (values 0 to 255). Memory size is limited to 1 MB.
"""

__author__ = "Michał Grzywna"

import sys

CELL_SIZE = 256
MEMORY_SIZE = 1024 * 1024


class EvalError(Exception):
    pass


def input_callback():
    """Default callback function for input"""
    return sys.stdin.read(1)


def output_callback(text):
    """Default callback function for output"""
    sys.stdout.write(text)


def _clean_source(code):
    """Remove unnecessary characters from BF source code."""
    return filter(lambda char: char in ".,<>+-[]", code)


def _bracketmap(code):
    """
    For each bracket calculate index of matching bracket.

    If number of opening brackets doesn't match number of closing brackets
    it raises an EvalError.
    """
    stack = []
    bracketmap = {}

    for index, char in enumerate(code):
        if char == "[":
            stack.append(index)
        elif char == "]":
            try:
                start_index = stack.pop()
                bracketmap[start_index] = index
                bracketmap[index] = start_index
            except IndexError:
                raise EvalError("Bracket balance error")

    if len(stack) > 0:
        raise EvalError("Bracket balance error")

    return bracketmap


def bfeval(code, _input=input_callback, _output=output_callback):
    """Evaluate BF source code."""
    code = _clean_source(code)
    bracketmap = _bracketmap(code)

    result, memory = [], [0]
    iptr = ptr = 0

    while iptr < len(code):
        # get instruction from code
        instruction = code[iptr]

        # print character
        if instruction == ".": result.append(chr(memory[ptr]))

        # get character
        elif instruction == ",":
            if result: _output("".join(result))
            result = []
            memory[ptr] = ord(_input())

        # move data pointer
        elif instruction == "<":
            if ptr > 0: ptr -= 1
        elif instruction == ">":
            if ptr < MEMORY_SIZE - 1:
                ptr += 1
                if ptr == len(memory): memory.append(0)
            else:
                raise EvalError("Out of memory")

        # increase or decrease cell value
        elif instruction == "+":
            if memory[ptr] < CELL_SIZE - 1: memory[ptr] += 1
            else: memory[ptr] = 0
        elif instruction == "-":
            if memory[ptr] > 0: memory[ptr] -= 1
            else: memory[ptr] = CELL_SIZE - 1

        # jump to matching bracket
        elif ((instruction == "[" and memory[ptr] == 0) or
              (instruction == "]" and memory[ptr] != 0)):
            iptr = bracketmap[iptr]

        # go to next instruction
        iptr += 1

    if result: _output("".join(result))

