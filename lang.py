class Compiler:

    def __init__(self, lang, asm):
        self.lang = open(lang, 'r')
        self.asm = open(asm, 'w')
        self.ch = None

    def __del__(self):
        self.lang.close()
        self.asm.close()

    def feed(self):
        while True:
            self.ch = self.lang.read(1)
            if not self.ch.isspace():
                break

    def match(self, expected):
        if self.ch != expected:
            print("error: expected %s" % expected)
            exit(1)
        self.feed()

    def expression(self):
        pass

    def label(self):
        while True:
            print(self.ch)
            self.feed()
            if not self.ch.isalnum():
                break

    def args(self):
        self.match('(')
        delim = ','
        while True:
            self.expression()
            if self.ch == delim:
                self.match(delim)
            else:
                break
        self.match(')')

    def block(self):
        delim = ';'
        while True:
            self.expression()
            if self.ch == delim:
                self.match(delim)
            else:
                break

    def function(self):
        self.args()
        self.match('{')
        self.block()
        self.match('}')

    def ishex(self, value):
        return value in ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

    def word(self):
        while True:
            print(self.ch)
            self.feed()
            if not self.ishex(self.ch):
                break

    def data(self):
        delim = ','
        while True:
            self.word()
            if self.ch == delim:
                self.match(delim)
            else:
                break

    def array(self):
        self.match('[')
        self.match(']')
        self.match('{')
        self.data()
        self.match('}')

    def compile(self):
        self.feed()
        while self.ch:
            self.label()
            if self.ch == '[':
                self.array()
            if self.ch == '(':
                self.function()

if __name__ == "__main__":
    Compiler('lang/test.lang', 'asm/test.asm').compile()
