import sys
from lark import Lark, tree, Transformer, v_args

print(
    r'''
    < Hi High-LOGO! >
    ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
    '''
)

if (len(sys.argv) != 2):
    print(r'''
          // Wrong number of parameters!      \\
          \\ python hlogoc.py inputfile.hlogo //
          -------------------------------------
          \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
        ''')
# Here we define the grammar. It is tha same as in
# the web IDE. You can work on the grammar there if
# you wish to and then paste it here.
high_logo_grammar = r"""
    start: instruction+

    instruction: MOVEMENT [NUMBER]                                     -> movement
               | "REPEAT" NUMBER code_block                            -> repeat

    code_block: "{" instruction+ "}"

    MOVEMENT: "FD"|"BK"|"LT"|"RT"|"PD"|"PU" 
    COLOR: LETTER+

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

# This function will traverse the AST and you can use it to emit the 
# code you want at every node of it.
def translate_program(ast, out):
    
    if ast.data == "start":
        out.write("import turtle\n")
        out.write("t = turtle.Turtle()\n")
        # Call the method recursively to visit the children
        for i in ast.children:
            translate_program(i, out)
        out.write("turtle.mainloop() \n")
    elif ast.data == "instruction":
        for i in ast.children:
            translate_program(i, out)
    elif ast.data == "movement":
        left = ast.children[0]
        right = ast.children[1] if len(ast.children) > 1 else None
        if left.value == "FD":
            out.write("t.forward(")
            out.write(right.value)
            out.write(")\n")
        if left.value == "RT":
            out.write("t.right(")
            out.write(right.value)
            out.write(")\n")
        if left.value == "PU":
            out.write("t.penup()\n")
        if left.value == "PD":
            out.write("t.pendown()\n")
        if left.value == "LT":
            out.write("t.left(")
            out.write(right.value)
            out.write(")\n")
        if left.value == "WIDTH":
            out.write("t.width(")
            out.write(right.value)
            out.write(")\n")
    elif ast.data == "repeat":
        count,block = ast.children
        print(block)
        out.write("for i in range(")
        out.write(count.value)
        out.write("):\n")
        translate_program(block, out)
    elif ast.data == "code_block":
        for i in ast.children:
            out.write("\t")
            translate_program(i, out)
    elif ast.data == "ifCondition":
        print("condiciones")

input = sys.argv[1]
output = sys.argv[1] + str(".py")
print("Input file: ", input)
parser = Lark(high_logo_grammar)

with open(input) as inputFile:
    with open(output, 'w') as out:
        ast = parser.parse(inputFile.read())
        #print(ast.pretty())
        #tree.pydot__tree_to_png(ast, "tree.png")
        #tree.pydot__tree_to_dot(ast, "tree.dot", rankdir="TD")
        #print (ast)
        translate_program(ast, out)