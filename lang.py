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
        space = False
        while True:
            self.look = self.lang.read(1)
            if not self.look.isspace():
                break
            else:
                space = True
        return space

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
            space = self.feed()
            if space or not self.isdigit(self.look):
                break
        digit = ''.join(chars)
        return digit

    def call(self, ident):
        self.asm.write("\tCALL %s\n" % ident)
        self.asm.write("\tLD R{%d] R[4100]\n" % self.sp)

    def reassign(self, ident):
        self.asm.write("\tLD R{%d] R[%d]\n" % (self.idents[ident], self.sp))

    def ident(self):
        ident = self.string()
        if ident == 'slot':
            string = self.string()
            self.assign(string)
            self.expression()
            self.sp += 1
        elif ident == 'return':
            self.expression()
            self.ret()
        elif self.idents.get(ident) is None:
            self.bomb("'%s' undefined" % ident)
        elif self.look == '(':
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
        self.sp -= 1
        self.asm.write("\tMUL R[%d] R[%d]\n" % (self.sp - 1, self.sp))

    def div(self):
        self.match('/')
        self.factor()
        self.sp -= 1
        self.asm.write("\tDIV R[%d] R[%d]\n" % (self.sp - 1, self.sp))

    def term(self):
        self.factor()
        while self.look in ['*', '/']:
            operate = {
                '*': self.mul,
                '/': self.div,
            }
            operate[self.look]()

    def add(self):
        self.match('+')
        self.term()
        self.sp -= 1
        self.asm.write("\tADD R[%d] R[%d]\n" % (self.sp - 1, self.sp))

    def sub(self):
        self.match('-')
        self.term()
        self.sp -= 1
        self.asm.write("\tSUB R[%d] R[%d]\n" % (self.sp - 1, self.sp))

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
            space = self.feed()
            if space or not self.isstring(self.look):
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
        self.match('-')
        self.match('>')
        self.string()

    def assign(self, string):
        self.match('=')
        if self.idents.get(string) is None:
            self.idents[string] = self.sp
        else:
            self.bomb("%s already defined" % string)

    def block(self):
        before = self.idents.copy()
        self.match('{')
        if self.look != '}':
            while True:
                self.expression()
                self.match(';')
                if self.look == '{':
                    self.block()
                if self.look == '}':
                    break
        self.match('}')
        expired = list(set(self.idents) - set(before))
        for ex in expired:
            del self.idents[ex]

    def ret(self):
        self.asm.write("\tLD R[4100] R[%d]\n" % self.sp)
        self.asm.write("\tRETURN\n")

    def function(self):
        self.sp = 0
        self.args()
        self.block()
        self.asm.write("\tRETURN\n\n")

    def ishex(self, value):
        return value in ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

    def word(self):
        self.match('0')
        self.match('x')
        chars = []
        while True:
            chars.append(self.look)
            self.feed()
            if not self.ishex(self.look):
                break
        word = ''.join(chars)
        return word

    def data(self):
        delim = ','
        while True:
            word = self.word()
            self.asm.write("\t0x%s\n" % word)
            if self.look == delim:
                self.match(delim)
            else:
                break

    def sprite(self):
        self.match('[')
        self.match(']')
        self.match('-')
        self.match('>')
        self.string()
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
                self.sprite()
            if self.look == '(':
                self.function()

if __name__ == "__main__":
    Compiler('lang/test.lang', 'asm/test.asm').compile()
