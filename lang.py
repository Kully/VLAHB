class Compiler:

    def __init__(self, lang, asm):
        self.lang = open(lang, 'r')
        self.asm = open(asm, 'w')
        self.look = None
        self.sp = 0
        self.idents = {}

    def __del__(self):
        self.lang.close()
        self.asm.close()

    def bomb(self, message):
        print("error: " + message)
        exit(1)

    def feed(self):
        while True:
            self.look = self.lang.read(1)
            if not self.look.isspace():
                break

    def match(self, expected):
        if self.look != expected:
            self.bomb("expected '%s' but got %s" % (expected, self.look))
        self.feed()

    def isdigit(self, value):
        return value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def digit(self):
        chars = []
        while True:
            chars.append(self.look)
            self.feed()
            if not self.isdigit(self.look):
                break
        digit = ''.join(chars)
        return digit

    def call(self, ident):
        self.asm.write("\tCALL %s\n" % ident)
        self.asm.write("\tLD R{%d] R[4100]\n" % self.sp)

    def ident(self):
        ident = self.string()
        if self.idents.get(ident) is None:
            self.bomb("'%s' undefined" % ident)
        if self.look == '(':
            self.match('(')
            # ... args.
            self.match(')')
            self.call(ident)
        else:
            self.asm.write("\tLD R[%d] R[%d]\n" % (self.sp, self.idents[ident]))

    def factor(self):
        if self.look == '(':
            self.match('(')
            self.expression()
            self.match(')')
        elif self.look.isalpha():
            self.ident()
        else:
            digit = self.digit()
            self.asm.write("\tLD R[%d] %s\n" % (self.sp, digit))
        self.sp += 1

    def mul(self):
        self.match('*')
        self.factor()
        self.asm.write("\tMUL R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))

    def div(self):
        self.match('/')
        self.factor()
        self.asm.write("\tDIV R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))

    def term(self):
        self.factor()
        while self.look in ['*', '/']:
            operate = {
                '*': self.mul,
                '/': self.div,
            }
            operate[self.look]()
            self.sp -= 1

    def add(self):
        self.match('+')
        self.term()
        self.asm.write("\tADD R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))

    def sub(self):
        self.match('-')
        self.term()
        self.asm.write("\tSUB R[%d] R[%d]\n" % (self.sp - 2, self.sp - 1))

    def expression(self):
        self.term()
        while self.look in ['+', '-']:
            operate = {
                '+': self.add,
                '-': self.sub,
            }
            operate[self.look]()
            self.sp -= 1

    def isstring(self, ch):
        return self.look.isalnum() or ch == '_'

    def string(self):
        chars = []
        while True:
            chars.append(self.look)
            self.feed()
            if not self.isstring(self.look):
                break
        string = ''.join(chars)
        return string

    def label(self):
        label = self.string()
        if self.idents.get(label) is None:
            self.idents[label] = -1
            self.asm.write("%s:\n" % label)
        else:
            self.bomb("label '%s' already defined" % label)

    def args(self):
        self.match('(')
        if self.look != ')':
            while True:
                self.expression()
                if self.look == ',':
                    self.match(',')
                else:
                    break
        self.match(')')

    def assign(self, string):
        if self.idents.get(string) is None:
            self.idents[string] = self.sp
        else:
            self.bomb("%s already defined" % string)

    def block(self):
        strings = []
        self.match('{')
        if self.look != '}':
            while True:
                self.expression()
                if self.look == '@':
                    self.match('@')
                    string = self.string()
                    strings.append(string)
                    self.assign(string)
                self.match(';')
                if self.look == '{':
                    self.block()
                if self.look == '}':
                    break
        self.match('}')
        sp = self.sp
        for string in strings:
            del self.idents[string]
        self.sp -= len(strings)
        return sp

    def function(self):
        self.sp = 0
        self.args()
        sp = self.block()
        self.asm.write("\tLD R[4100] R[%d]\n" % (sp - 1))
        self.asm.write("\tRETURN\n\n")

    def ishex(self, value):
        return value in ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

    def word(self):
        chars = []
        while True:
            chars.append(self.look)
            self.feed()
            if not self.ishex(self.look):
                break
        word = ''.join(chars)
        self.asm.write("\t0x%s\n" % word)

    def data(self):
        delim = ','
        while True:
            self.word()
            if self.look == delim:
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
        while self.look:
            self.label()
            if self.look == '[':
                self.array()
            if self.look == '(':
                self.function()

if __name__ == "__main__":
    Compiler('lang/test.lang', 'asm/test.asm').compile()
