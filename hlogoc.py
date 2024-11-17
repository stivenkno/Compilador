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
    // A HIgh-LOGO program consists of one or more basic instructions
    start: instruction+			
    
    instruction: basic_instruction | repeat_instruction
    
    basic_instruction: INSTNAME INTNUM
    
    repeat_instruction: REPEAT INTNUM "{" basic_instruction+ "}"

    REPEAT: "REPEAT"
    INSTNAME: "FD" | "RT"
    INTNUM : /-?\d+(\.\d+)?([eE][+-]?\d+)?/

    %ignore /[ \t\n\f\r]+/
"""

firstIteration = True
length = 0
instructions = []

# This function will traverse the AST and you can use it to emit the 
# code you want at every node of it.
def translate_program(ast, out):
    global firstIteration
    global length
    
    if firstIteration:
        
        length = len(ast.children)
        for i in range(0, length):
            instructions.append(ast.children[i].children[0]) 
        #print("Length is:", length)
        firstIteration = False
        #print(instructions)
        
    
    # print("Tree node", ast
    if ast.data == "start":
        out.write("import turtle\n")
        out.write("t = turtle.Turtle()\n")
        # Call the method recursively to visit the children
        for i in instructions:
            translate_program(i, out)
        out.write("turtle.mainloop() \n")       
        
    elif ast.data == "basic_instruction":
        # This will be run when the node is a basic_instruction
        [left, right] = ast.children
        #out.write(left.data + " " + right.data)
        if left.value == "FD":
            out.write("t.forward(")
            out.write(right.value)
            out.write(")\n")
        if left.value == "RT":
            out.write("t.right(")
            out.write(right.value)
            out.write(")\n")
    elif ast.data == "repeat_instruction":
        length = len(ast.children)
        out.write("for i in range("+ast.children[1]+"):\n")
        for i in range (2, length):
            out.write("\t")
            translate_program(ast.children[i], out)
        
              
    else:
        # No implementation fro the node was found
        print("There is nothing to do for ast node ")

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