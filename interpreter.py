import copy
from colorama import Fore, Style
import time
from sys import set_int_max_str_digits
class Vector2i:

    def __init__(self, x:int = 0, y:int = 0):
        self.x:int = x
        self.y:int = y
    def __add__(self, o):
        return Vector2i(self.x+o.x,self.y+o.y)
    def __str__(self):
        return f"({self.x},{self.y})"
    def __repr__(self):
        return f"({self.x},{self.y})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y  
    def __mul__(self, o):
        return Vector2i(self.x*o.x,self.y*o.y)

    def __hash__(self):
        return hash((self.x, self.y)) 
class Interpreter:
    def __init__(self, code):
        self.code = code
        self.pos = Vector2i(0,0)
        self.dir = Vector2i(1,1)
        self.is_running = False
        self.debug_printing = True
        self.stack = []
        self.commands = {
            "+": self.do_add,
            "-": self.do_sub,
            "*": self.do_mul,
            "/": self.do_div,
            "%": self.do_mod,

            ":": self.do_dup,#dup
            "~": self.do_swp,#swap
            ".": self.do_pnu,#popoutput
            ",": self.do_pst,#popascii
            "$": self.do_pop,#pop
            "&": self.do_inp,#inputint
            "@": self.do_ro3,#rotate
            "^": self.do_rot,
            "v": self.do_len,#
            "=": self.do_ous,#can pass through once

            #"?": self.do_nop,#conditbounce

            "!": self.do_hlt,#terminate

        }
    def popstack(self, default=0, pos=-1):
        if len(self.stack) <= 0:
            return default
        else:
            return self.stack.pop(pos)
    def do_len(self):
        self.stack.append(len(self.stack))
    def do_ous(self):
        self.code[self.pos.x][self.pos.y] = "#"
    def do_hlt(self):
        self.is_running = False
    def do_inp(self):
        self.stack.append(int(input()))
    def do_ro3(self):
        c = self.popstack()
        b = self.popstack()
        a = self.popstack()
        self.stack.append(c)
        self.stack.append(a)
        self.stack.append(b)
    def do_rot(self):
        a = self.popstack(0,0)
        self.stack.insert(0)
    def do_pop(self):
        self.popstack()
    def do_pnu(self):
        print(((" " * (len(self.code)+10)) if self.debug_printing else "" ) + str(self.popstack()), end=('\n' if self.debug_printing else ''))
    def do_pst(self):
        print(((" " * (len(self.code)+10)) if self.debug_printing else "" ) + chr(self.popstack()), end=('\n' if self.debug_printing else ''))
    def do_dup(self):
        a = self.popstack()
        self.stack.append(a)
        self.stack.append(a)
    def do_swp(self):
        a = self.popstack()
        b = self.popstack()
        self.stack.append(a)
        self.stack.append(b)
    def do_add(self):
        b = self.popstack()
        a = self.popstack()
        self.stack.append(a+b)
    def do_sub(self):
        b = self.popstack()
        a = self.popstack()
        self.stack.append(a-b)
    def do_mul(self):
        b = self.popstack()
        a = self.popstack(1)
        self.stack.append(b*a)
    def do_div(self):
        b = self.popstack(1)
        a = self.popstack()
        self.stack.append(a//b)
    def do_mod(self):
        b = self.popstack(1)
        a = self.popstack()
        self.stack.append(a%b)


    def reverse_array_operation(self,code):
        height = len(code[0]) if code else 0
        width = len(code)
        reversed_code = [['' for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                reversed_code[y][x] = code[x][y]

        return reversed_code
    def print_visual(self):
        newcode = copy.deepcopy(self.code)
        c = "\\" if self.dir.x == self.dir.y else "/" 
        newcode[self.pos.x][self.pos.y] = Fore.YELLOW+c+Style.RESET_ALL
        newcode = self.reverse_array_operation(newcode)

        for row in newcode:
            print(*row, sep='')
    def do_nop(self):
        pass
    def run(self):
        set_int_max_str_digits(0)
        self.is_running = True
        while self.is_running:
            c = self.code[self.pos.x][self.pos.y]
            if c.isnumeric():
                self.stack.append(int(c))
            if c in self.commands:
                self.commands[c]()
            if self.is_running == False:
                return
            next_pos = self.pos+self.dir
            if (next_pos.x >= len(self.code) or next_pos.x < 0) or (self.code[next_pos.x][self.pos.y] in "#?\""):
                should_bounce = True
                if (not(next_pos.x >= len(self.code) or next_pos.x < 0)) and (self.code[next_pos.x][self.pos.y] == "?"):
                    if (len(self.stack) <= 0) or self.stack[-1] == 0:
                        should_bounce = False
                if (not(next_pos.x >= len(self.code) or next_pos.x < 0)) and (self.code[next_pos.x][self.pos.y] == "\""):
                    self.code[next_pos.x][self.pos.y] = "#"
                    should_bounce = False
                if should_bounce:
                    self.dir.x *= -1
            if (next_pos.y >= len(self.code[0]) or next_pos.y < 0) or (self.code[self.pos.x][next_pos.y] in "#?\""):
                should_bounce = True
                if (not(next_pos.y >= len(self.code[0]) or next_pos.y < 0)) and (self.code[self.pos.x][next_pos.y] == "?"):
                    if (len(self.stack) <= 0) or self.stack[-1] == 0:
                        should_bounce = False
                if (not(next_pos.y >= len(self.code[0]) or next_pos.y < 0)) and (self.code[self.pos.x][next_pos.y] == "\""):
                    self.code[self.pos.x][next_pos.y] = "#"
                    should_bounce = False
                if should_bounce:
                    self.dir.y *= -1
            if ((next_pos.y >= len(self.code[0]) or next_pos.y < 0) and (next_pos.x >= len(self.code) or next_pos.x < 0)) or (self.code[self.pos.x][self.pos.y] in "#?\""):
                should_bounce = True
                if (not((next_pos.y >= len(self.code[0]) or next_pos.y < 0) or (next_pos.x >= len(self.code) or next_pos.x < 0))) and (self.code[self.pos.x][self.pos.y] == "?"):
                    if (len(self.stack) <= 0) or self.stack[-1] == 0:
                        should_bounce = False
                if (not((next_pos.y >= len(self.code[0]) or next_pos.y < 0) or (next_pos.x >= len(self.code) or next_pos.x < 0))) and (self.code[self.pos.x][self.pos.y] == "\""):
                    self.code[self.pos.x][self.pos.y] ="#"
                    should_bounce = False
                if should_bounce:
                    self.dir.x *= -1
                    self.dir.y *= -1
            next_pos = self.pos+self.dir
            self.pos = next_pos
            if self.debug_printing:
                self.print_visual()
            #time.sleep(0.1)