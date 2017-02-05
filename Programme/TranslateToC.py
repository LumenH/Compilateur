import AST
from AST import addToClass


variable = dict()

@addToClass(AST.EntryNode)
def execute(self):
    try:
        file.write("    ")
        file.write("scanf(")
        for c in self.children:
            c.execute()
        file.write(");\n")
    except NameError:
        print("La balise programme n'est pas présente ! ")


@addToClass(AST.PrintNode)
def execute(self):
    try:
        file.write("    ")
        file.write("printf(")
        for c in self.children:
            c.execute()
        file.write(");\n")
    except NameError:
        print("La balise programme n'est pas présente ! ")


@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.ProgNode)
def execute(self):
    global file
    global tabulation

    filename = self.name[1:-1]
    print("Creation de : " + filename + ".c")
    file = open(filename + ".c", 'w')
    file.write("#include <stdio.h>\n\n")
    file.write("int main(void)\n")
    file.write("{\n")

    for c in self.children:
        c.execute()

    file.write("\n    " + "return 0;\n")
    file.write("}")
    file.close()


@addToClass(AST.AssignNode)
def execute(self):
    try:
        file.write("    ")
        if str(self.children[1]) not in variable:
            variable[str(self.children[1])] = self.children[0].tok
            self.children[0].execute()

        self.children[1].execute()
        file.write(" = ")
        self.children[2].execute()

        file.write(";\n")
    except NameError:
        print("La balise programme n'est pas présente ! ")


@addToClass(AST.WhileNode)
def execute(self):
    try:
        var = set()
        for c in self.children[1].children:
            if isinstance(c, AST.AssignNode):
                if str(c.children[1]) not in variable:
                    var.add(str(c.children[1]))

        file.write("\n    " + self.type + "(")
        self.children[0].execute()
        file.write(")\n")
        file.write("    {\n")
        file.write("    ")
        self.children[1].execute()
        file.write("    }\n")


        for element in var:
            variable.pop(element)
        var.clear()
    except NameError:
        print("La balise programme n'est pas présente ! ")


@addToClass(AST.ForNode)
def execute(self):
    try:
        var = set()
        for c in self.children[1].children:
            if isinstance(c, AST.AssignNode):
                if str(c.children[1]) not in variable:
                    var.add(str(c.children[1]))

        file.write("\n    " + self.type + "(")
        if str(self.children[0]) not in variable:
            file.write("int ")
        self.children[0].execute()
        if str(self.children[0]) not in variable:
            file.write(" = 0 ")
        file.write("; ")
        self.children[1].execute()
        file.write("; ")
        self.children[0].execute()
        file.write(" += ")
        #add gestion erreur si variable iterator et variable iterer !=
        self.children[2].execute()
        file.write(")\n")
        file.write("    {\n")
        file.write("    ")
        self.children[3].execute()
        file.write("    }\n")

        for element in var:
            variable.pop(element)
        var.clear()
    except NameError:
        print("La balise programme n'est pas présente ! ")

@addToClass(AST.CondNode)
def execute(self):
    try:
        var = set()
        for c in self.children[1].children:
            if isinstance(c, AST.AssignNode):
                if str(c.children[1]) not in variable:
                    var.add(str(c.children[1]))

        a = str(self.children[0].children[0])
        b = str(self.children[0].children[1])
        if a[0] == "'":
            a = a[1:-2]
        else:
            a = a[0:-3]
        if b[0] == "'":
            b = b[1:-2]
        else:
            b = b[0:-3]
        type = self.type
        comparateur = str(self.children[0])
        if comparateur[0] == "=" or comparateur[0] == "!":
            comparateur = comparateur[0:2]
        else:
            comparateur = comparateur[0]

        file.write("    " + type + "(" + a + " " + comparateur + " " + b + ")\n")
        file.write("    {\n")
        file.write("    ")
        self.children[1].execute()

        if len(self.children) > 2:

            for c in self.children[2].children:
                if isinstance(c, AST.AssignNode):
                    if str(c.children[1]) not in variable:
                        var.add(str(c.children[1]))

            file.write("    }")
            file.write("\n    else\n")
            file.write("    {\n")
            file.write("    ")
            self.children[2].execute()

        file.write("    }\n")

        for element in var:
            variable.pop(element)
        var.clear()
    except NameError:
        print("La balise programme n'est pas présente ! ")


@addToClass(AST.OpNode)
def execute(self):
    try:
        if len(self.children) >= 2:
            self.children[0].execute()
            file.write(" " + self.op + " ")
            self.children[1].execute()
        else:
            file.write(self.op)
            self.children[0].execute()
    except NameError:
        print("La balise programme n'est pas présente ! ")


@addToClass(AST.TokenNode)
def execute(self):
    try:
        ok = False
        for c, cnext in zip(str(self.tok), str(self.tok)[1:]):
            if c == "\"":
                if cnext == ",":
                    ok = True

        if ok:
            file.write(str(self.tok)[0:-1])
        else:
            file.write(str(self.tok))
    except NameError:
        print("La balise programme n'est pas présente ! ")


@addToClass(AST.TypeNode)
def execute(self):
    try:
        file.write(str(self.tok) + " ")
    except NameError:
        print("La balise programme n'est pas présente ! ")


if __name__ == "__main__":
    from parser import parse
    import sys

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print("Debut de la conversion vers le langage C")
    ast.execute()
    print("La traduction est terminée")