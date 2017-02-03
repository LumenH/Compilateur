import AST
from AST import addToClass


operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
    '<' : lambda x,y: 0 if x<y else 1,
    '>' : lambda x,y: 0 if x>y else 1,
    '==' : lambda x,y: 0 if x==y else 1,
    '!=' : lambda x,y: 0 if x!=y else 1
}

_funcs = {}
_vars = {}

_running_function = None


@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.AssignNode)
def execute(self):
    global _running_function
    _funcs[_running_function][1][self.children[0]] = self.children[1].execute()


@addToClass(AST.TokenNode)
def execute(self):
    global _running_function
    if isinstance(self.tok, str):
        if self.tok[0] == '"':
            return self.tok[1:-1]
        try:
            return _funcs[_running_function][1][self.tok]
        except KeyError:
            print("*** Error: Variable %s undefined !" % self.tok)
    return self.tok


@addToClass(AST.CondNode)
def execute(self):
    cond_result = self.children[0].execute()
    if len(self.children) == 2:
        if cond_result != 0:
            self.children[1].execute()
    else:
        if cond_result == 0:
            self.children[1].execute()
        else:
            self.children[2].execute()


if __name__ == "__main__":
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.execute()
    _running_function = "main"
    _funcs['main'][0].execute()