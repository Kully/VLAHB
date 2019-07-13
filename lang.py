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
        self.asm.write("\tGOTO %s\n" % ident)
        self.asm.write("\tLD R[%d] R[4100]\n" % self.sp)

    def pass_args(self, ident):
        expected = self.lookup(ident)
        self.match('(')
        count = 0
        if self.look != ')':
            while True:
                self.expression()
                self.sp += 1
                count += 1
                if self.look == ',':
                    self.match(',')
                else:
                    break
        if expected != count:
            self.bomb("%s: expected %d args but got %d" % (ident, expected, count))
        self.sp -= count
        self.asm.write("\tPUSH\n")
        for which in range(count):
            self.asm.write("\tLD R[%d] R[%d]\n" % (which, self.sp + which))
        self.match(')')

    def lookup(self, ident):
        if self.idents.get(ident) is None:
            self.bomb("'%s' undefined" % ident)
        return self.idents.get(ident)

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
        elif self.look == '(':
            self.pass_args(ident)
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

    def insert(self, ident, value):
        if self.idents.get(ident) is None:
            self.idents[ident] = value
        else:
            self.bomb("'%s' already defined" % ident)

    def declare_args(self, ident_label):
        arg_count = 0
        self.match('(')
        if self.look != ')':
            while True:
                typeof = self.string()
                ident = self.string()
                self.sp += 1
                arg_count += 1
                if self.look == ',':
                    self.match(',')
                else:
                    break
        self.match(')')
        self.annotate()
        self.insert(ident_label, arg_count)

    def assign(self, string):
        self.match('=')
        self.insert(string, self.sp)

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
        self.sp -= len(expired)

    def ret(self):
        self.asm.write("\tLD R[4100] R[%d]\n" % self.sp)
        self.asm.write("\tRETURN\n")

    def function(self, ident):
        self.sp = 0
        self.declare_args(ident)
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

    def data(self, ident):
        delim = ','
        count = 0
        while True:
            word = self.word()
            self.asm.write("\t0x%s\n" % word)
            count += 1
            if self.look == delim:
                self.match(delim)
            else:
                break
        self.idents[ident] = count

    def annotate(self):
        self.match('-')
        self.match('>')
        self.string()

    def sprite(self, ident):
        self.match('[')
        self.match(']')
        self.annotate()
        self.match('{')
        self.data(ident)
        self.match('}')
        self.asm.write('\n')

    def reset(self):
        self.asm.write("GOTO main\n\n")

    def dump(self):
        for key, value in self.idents.items():
            print(key, value)

    def compile(self):
        self.reset()
        self.feed()
        while self.look:
            ident = self.string()
            self.asm.write("%s:\n" % ident)
            if self.look == '[':
                self.sprite(ident)
            if self.look == '(':
                self.function(ident)
        self.dump()

if __name__ == "__main__":
    Compiler('lang/test.lang', 'asm/test.asm').compile()
