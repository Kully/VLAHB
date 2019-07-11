class Compiler:

    def __init__(self, lang, asm):
        self.lang = open(lang, 'r')
        self.asm = open(asm, 'w')
        self.char = None
        self.labels = []
        self.sp = 0

    def __del__(self):
        self.lang.close()
        self.asm.close()

    def feed(self):
        while True:
            self.char = self.lang.read(1)
            if not self.char.isspace():
                break

    def match(self, expected):
        if self.char != expected:
            print("error: expected %s but got %s" % (expected, self.char))
            exit(1)
        self.feed()

    def isdigit(self, value):
        return value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def digit(self):
        chars = []
        while True:
            chars.append(self.char)
            self.feed()
            if not self.isdigit(self.char):
                break
        digit = ''.join(chars)
        self.asm.write("\tLD R[%d] %s\n" % (self.sp, digit))
        self.sp += 1

    def factor(self):
        if self.char == '(':
            self.match('(')
            self.expression()
            self.match(')')
        else:
            self.digit()

    def mul(self):
        self.match('*')
        self.factor()
        self.asm.write("\tMUL R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))
        self.sp -= 1

    def div(self):
        self.match('/')
        self.factor()
        self.asm.write("\tDIV R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))
        self.sp -= 1

    def term(self):
        self.factor()
        while self.char in ['*', '/']:
            if self.char == '*':
                self.mul()
            if self.char == '/':
                self.div()

    def add(self):
        self.match('+')
        self.term()
        self.asm.write("\tADD R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))
        self.sp -= 1

    def sub(self):
        self.match('-')
        self.term()
        self.asm.write("\tSUB R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))
        self.sp -= 1

    def expression(self):
        self.term()
        while self.char in ['+', '-']:
            if self.char == '+':
                self.add()
            if self.char == '-':
                self.sub()

    def islabel(self, ch):
        return self.char.isalnum() or ch == '_'

    def label(self):
        chars = []
        while True:
            chars.append(self.char)
            self.feed()
            if not self.islabel(self.char):
                break
        label = ''.join(chars)
        self.labels.append(label)
        self.asm.write("%s:\n" % label)

    def args(self):
        self.match('(')
        if self.char != ')':
            while True:
                self.expression()
                if self.char == ',':
                    self.match(',')
                else:
                    break
        self.match(')')

    def block(self):
        self.match('{')
        if self.char != '}':
            while True:
                self.expression()
                self.match(';')
                if self.char == '}':
                    break
        self.match('}')

    def function(self):
        self.sp = 0
        self.args()
        self.block()
        self.asm.write("\tLD R[4100] R[%d]\n" % (self.sp - 1))
        self.asm.write("\tRETURN\n\n")

    def ishex(self, value):
        return value in ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

    def word(self):
        chars = []
        while True:
            chars.append(self.char)
            self.feed()
            if not self.ishex(self.char):
                break
        word = ''.join(chars)
        self.asm.write("\t0x%s\n" % word)

    def data(self):
        delim = ','
        while True:
            self.word()
            if self.char == delim:
                self.match(delim)
            else:
                break

    def array(self):
        self.match('[')
        self.match(']')
        self.match('{')
        self.data()
        self.match('}')
        self.asm.write('\n')

    def reset(self):
        self.asm.write("GOTO main\n\n")

    def compile(self):
        self.reset()
        self.feed()
        while self.char:
            self.label()
            if self.char == '[':
                self.array()
            if self.char == '(':
                self.function()
        for label in self.labels:
            print(label)

if __name__ == "__main__":
    Compiler('lang/test.lang', 'asm/test.asm').compile()
