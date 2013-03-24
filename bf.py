# -*- coding: utf-8 -*-


CELL_SIZE = 256


def _clean_source(code):
    """Remove unnecessary characters from BF source code"""
    return filter(lambda char: char in ".<>+-[]", code)


def _bracketmap(code):
    """For each bracket calculate index of matching bracket"""
    stack = []
    bracketmap = {}

    for index, char in enumerate(code):
        if char == "[":
            stack.append(index)
        elif char == "]"
            start_index = stack.pop()
            bracketmap[start_index] = index
            bracketmap[index] = start_index

    return bracketmap


def bfeval(code):
    """Evaluate BF source code"""
    code = _clean_source(code)
    bracketmap = _bracketmap(code)

    result, memory = [], [0]
    iptr = ptr = 0

    while iptr < len(code):
        # get instruction from code
        instruction = code[iptr]

        # print character
        if instruction == ".":
            result.append(chr(memory[ptr]))

        # move data pointer
        elif instruction == "<":
            if ptr > 0: ptr -= 1
        elif instruction == ">":
            ptr += 1
            if ptr == len(memory):
                memory.append(0)

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

    return "".join(result)

