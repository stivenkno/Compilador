import sys
from lark import Lark, tree, Transformer, v_args, Tree, Token

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

# Here we define the grammar. It is the same as in
# the web IDE. You can work on the grammar there if
# you wish to and then paste it here.
high_logo_grammar = r"""
    start: instruction+

    instruction: MOVEMENT [NUMBER]                                     -> movement
               | "REPEAT" NUMBER code_block                            -> repeat
               | "IF" "(" condition ")" code_block ["ELSE" code_block] -> if

    condition: comparison 
              | NOT condition 
              | condition AND condition 
              | condition OR condition 
              | "(" condition ")"

    comparison: NUMBER CMP NUMBER

    AND: "and"
    OR: "or"
    NOT: "!"
    CMP: "==" | "!=" | "<" | ">" | "<=" | ">="

    code_block: "{" instruction+ "}"

    MOVEMENT: "FD"|"BK"|"LT"|"RT"|"PD"|"PU"

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

def translate_condition(ast, out):
    print(ast)
    
    if isinstance(ast, Tree):
        if ast.data == "condition":
            for i in ast.children:
                translate_condition(i, out)
        elif ast.data == "comparison":
            left = ast.children[0]
            right = ast.children[2]
            out.write("(" + left.value)
            out.write(ast.children[1].value)
            out.write(right.value + ")")
        elif ast.data == "NOT":
            out.write(ast.children[1].value)
        elif ast.data == "AND":
            out.write(ast.children[0].value)
            out.write(" and ")
            out.write(ast.children[1].value)
        elif ast.data == "OR":
            out.write(ast.children[0].value)
            out.write(" or ")
            out.write(ast.children[1].value)
    elif isinstance(ast, Token):
        out.write(ast.value)

# This function will traverse the AST and you can use it to emit the
# code you want at every node of it.
def translate_program(ast, out, indent_level=0):
    indent = ' ' * (indent_level * 4)  # 4 spaces per indentation level
    
    if ast.data == "start":
        out.write("import turtle\n")
        out.write("t = turtle.Turtle()\n")
        # Call the method recursively to visit the children
        for i in ast.children:
            translate_program(i, out, indent_level + 1)
        out.write("turtle.mainloop() \n")
    
    elif ast.data == "instruction":
        for i in ast.children:
            translate_program(i, out, indent_level)
    
    elif ast.data == "movement":
        left = ast.children[0]
        right = ast.children[1] if len(ast.children) > 1 else None
        if left.value == "FD":
            out.write(f"{indent}t.forward({right.value})\n")
        if left.value == "RT":
            out.write(f"{indent}t.right({right.value})\n")
        if left.value == "PU":
            out.write(f"{indent}t.penup()\n")
        if left.value == "PD":
            out.write(f"{indent}t.pendown()\n")
        if left.value == "LT":
            out.write(f"{indent}t.left({right.value})\n")
        if left.value == "WIDTH":
            out.write(f"{indent}t.width({right.value})\n")
    
    elif ast.data == "repeat":
        count, block = ast.children
        out.write(f"{indent}for i in range({count.value}):\n")
        translate_program(block, out, indent_level + 1)
    
    elif ast.data == "code_block":
        for i in ast.children:
            out.write(f"{indent}\t")
            translate_program(i, out, indent_level + 1)
    
    elif ast.data == "if":
        condition, block1, block2 = ast.children
        out.write(f"{indent}if (")
        translate_condition(condition, out)
        out.write("):\n")
        translate_program(block1, out, indent_level + 1)
        if block2:
            out.write(f"{indent}else:\n")
            translate_program(block2, out, indent_level + 1)

input = sys.argv[1]
output = sys.argv[1] + str(".py")
print("Input file: ", input)
parser = Lark(high_logo_grammar, start='start')

with open(input) as inputFile:
    with open(output, 'w') as out:
        ast = parser.parse(inputFile.read())
        print(ast.pretty())
        tree.pydot__tree_to_png(ast, "tree.png")
        #tree.pydot__tree_to_dot(ast, "tree.dot", rankdir="TD")
        #print (ast)
        translate_program(ast, out)
import sys
from lark import Lark, tree, Transformer, v_args, Tree, Token

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

# Here we define the grammar. It is the same as in
# the web IDE. You can work on the grammar there if
# you wish to and then paste it here.
high_logo_grammar = r"""
    start: instruction+

    instruction: MOVEMENT [NUMBER]                                     -> movement
               | "REPEAT" NUMBER code_block                            -> repeat
               | "IF" "(" condition ")" code_block ["ELSE" code_block] -> if

    condition: comparison 
              | NOT condition 
              | condition AND condition 
              | condition OR condition 
              | "(" condition ")"

    comparison: NUMBER CMP NUMBER

    AND: "and"
    OR: "or"
    NOT: "!"
    CMP: "==" | "!=" | "<" | ">" | "<=" | ">="

    code_block: "{" instruction+ "}"

    MOVEMENT: "FD"|"BK"|"LT"|"RT"|"PD"|"PU"

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

def translate_condition(ast, out):
    print(ast)
    
    if isinstance(ast, Tree):
        if ast.data == "condition":
            for i in ast.children:
                translate_condition(i, out)
        elif ast.data == "comparison":
            left = ast.children[0]
            right = ast.children[2]
            out.write("(" + left.value)
            out.write(ast.children[1].value)
            out.write(right.value + ")")
        elif ast.data == "NOT":
            out.write(ast.children[1].value)
        elif ast.data == "AND":
            out.write(ast.children[0].value)
            out.write(" and ")
            out.write(ast.children[1].value)
        elif ast.data == "OR":
            out.write(ast.children[0].value)
            out.write(" or ")
            out.write(ast.children[1].value)
    elif isinstance(ast, Token):
        out.write(ast.value)

# This function will traverse the AST and you can use it to emit the
# code you want at every node of it.
def translate_program(ast, out, indent_level=-1):

    indent = ' ' * (indent_level)  # 4 spaces per indentation level
    
    if ast.data == "start":
        out.write("import turtle\n")
        out.write("t = turtle.Turtle()\n")
        # Call the method recursively to visit the children
        for i in ast.children:
            translate_program(i, out, indent_level + 1)
        out.write("turtle.mainloop() \n")
    
    elif ast.data == "instruction":
        for i in ast.children:
            translate_program(i, out, indent_level)
    
    elif ast.data == "movement":
        left = ast.children[0]
        right = ast.children[1] if len(ast.children) > 1 else None
        if left.value == "FD":
            out.write(f"{indent}t.forward({right.value})\n")
        if left.value == "RT":
            out.write(f"{indent}t.right({right.value})\n")
        if left.value == "PU":
            out.write(f"{indent}t.penup()\n")
        if left.value == "PD":
            out.write(f"{indent}t.pendown()\n")
        if left.value == "LT":
            out.write(f"{indent}t.left({right.value})\n")
        if left.value == "WIDTH":
            out.write(f"{indent}t.width({right.value})\n")
    
    elif ast.data == "repeat":
        count, block = ast.children
        out.write(f"{indent}for i in range({count.value}):\n")
        translate_program(block, out, indent_level + 1)
    
    elif ast.data == "code_block":
        for i in ast.children:
            out.write(f"{indent}")
            translate_program(i, out, indent_level + 1)
    
    elif ast.data == "if":
        condition, block1, block2 = ast.children
        out.write(f"{indent}if (")
        translate_condition(condition, out)
        out.write("):\n")
        translate_program(block1, out, indent_level + 1)
        if block2:
            out.write(f"{indent}else:\n")
            translate_program(block2, out, indent_level + 1)

input = sys.argv[1]
output = sys.argv[1] + str(".py")
print("Input file: ", input)
parser = Lark(high_logo_grammar, start='start')

with open(input) as inputFile:
    with open(output, 'w') as out:
        ast = parser.parse(inputFile.read())
        print(ast.pretty())
        tree.pydot__tree_to_png(ast, "tree.png")
        #tree.pydot__tree_to_dot(ast, "tree.dot", rankdir="TD")
        #print (ast)
        translate_program(ast, out)
