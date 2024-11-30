import sys
from lark import Lark, tree, Transformer, v_args, Tree, Token

import subprocess,time,os

print(
    r'''
                            _          __________                              _,
                        _.-(_)._     ."          ".      .--""--.          _.-{__}-._
                    .'________'.   | .--------. |    .'        '.      .:-'`____`'-:.
                    [____________] /` |________| `\  /   .'``'.   \    /_.-"`_  _`"-._\
                    /  / .\/. \  \|  / / .\/. \ \  ||  .'/.\/.\'.  |  /`   / .\/. \   `\
                    |  \__/\__/  |\_/  \__/\__/  \_/|  : |_/\_| ;  |  |    \__/\__/    |
                    \            /  \            /   \ '.\    /.' / .-\                /-.
                    /'._  --  _.'\  /'._  --  _.'\   /'. `'--'` .'\/   '._-.__--__.-_.'   \
                    /_   `""""`   _\/_   `""""`   _\ /_  `-./\.-'  _\'.    `""""""""`    .'`\
                    (__/    '|    \ _)_|           |_)_/            \__)|        '       |   |
                    |_____'|_____|   \__________/   |              |;`_________'________`;-'
                    '----------'    '----------'   '--------------'`--------------------`
      __    __  ______        __    __  ______   ______   __    __          __         ______    ______    ______        
/  |  /  |/      |      /  |  /  |/      | /      \ /  |  /  |        /  |       /      \  /      \  /      \       
$$ |  $$ |$$$$$$/       $$ |  $$ |$$$$$$/ /$$$$$$  |$$ |  $$ |        $$ |      /$$$$$$  |/$$$$$$  |/$$$$$$  |      
$$ |__$$ |  $$ |        $$ |__$$ |  $$ |  $$ | _$$/ $$ |__$$ | ______ $$ |      $$ |  $$ |$$ | _$$/ $$ |  $$ |      
$$    $$ |  $$ |        $$    $$ |  $$ |  $$ |/    |$$    $$ |/      |$$ |      $$ |  $$ |$$ |/    |$$ |  $$ |      
$$$$$$$$ |  $$ |        $$$$$$$$ |  $$ |  $$ |$$$$ |$$$$$$$$ |$$$$$$/ $$ |      $$ |  $$ |$$ |$$$$ |$$ |  $$ |      
$$ |  $$ | _$$ |_       $$ |  $$ | _$$ |_ $$ \__$$ |$$ |  $$ |        $$ |_____ $$ \__$$ |$$ \__$$ |$$ \__$$ |      
$$ |  $$ |/ $$   |      $$ |  $$ |/ $$   |$$    $$/ $$ |  $$ |        $$       |$$    $$/ $$    $$/ $$    $$/       
$$/   $$/ $$$$$$/       $$/   $$/ $$$$$$/  $$$$$$/  $$/   $$/         $$$$$$$$/  $$$$$$/   $$$$$$/   $$$$$$/        
                                                                                                                    
                                                                                                                    
                                                                                                                    
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
    start: (command | procedure_declaration)+

    command: TURTLE_ACTION [expression] |         
             | conditional_statement
             | single_iteration
             | double_iteration
             | procedure_invocation                            
               
    procedure_declaration: DEFINE NAME LPAREN parameter_sequence? RPAREN code_sequence

    procedure_invocation: NAME LPAREN argument_sequence? RPAREN
    
    parameter_sequence: NAME (COMMA NAME)*

    argument_sequence: expression (COMMA expression)*

    expression: INTNUM | NAME

    conditional_statement: IF boolean_condition code_sequence (ELSE code_sequence)?

    single_iteration: SINGLE_LOOP VAR IN RANGE_KEYWORD LPAREN range_parameters RPAREN code_sequence
    double_iteration: DOUBLE_LOOP VAR COMMA VAR IN ZIP_KEYWORD LPAREN range_expr COMMA range_expr RPAREN code_sequence

    range_expr: RANGE_KEYWORD LPAREN range_parameters RPAREN

    range_parameters: INTNUM COMMA INTNUM COMMA INTNUM
                     | INTNUM COMMA INTNUM
                     | INTNUM

    boolean_condition: "(" boolean_term ")"

    boolean_term: comparison
                 | NOT boolean_term
                 | boolean_term AND boolean_term
                 | boolean_term OR boolean_term
                 | "(" boolean_term ")"

    comparison: INTNUM COMPARATOR INTNUM

    code_sequence: LBRACE command* RBRACE


    DEFINE: "def"
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    SINGLE_LOOP: "for"
    DOUBLE_LOOP: "for"
    VAR: /[i-z]/
    IN: "in"
    ZIP_KEYWORD: "zip"
    RANGE_KEYWORD: "range"
    LPAREN: "("
    RPAREN: ")"
    COMMA: ","
    IF: "if"
    ELSE: "else"
    LBRACE: "{"
    RBRACE: "}"
    COMPARATOR: "==" | "!=" | "<" | ">" | "<=" | ">="
    NOT: "!"
    AND: "&&"
    OR: "||"
  
    
    INTNUM : /-?\d+(\.\d+)?([eE][+-]?\d+)?/
    TURTLE_ACTION: "FD"|"BK"|"LT"|"RT"|"PD"|"PU"|"WIDTH"
    COMMENT: "#" /[^\n]*/
    MULTILINE_COMMENT: /\/\*(\*(?!\/)|[^*])*\*\//
    

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
    %ignore COMMENT
    %ignore MULTILINE_COMMENT
    
"""

def move_instruction(ast, out, indent):
    
    move = ast[0]
    tree = ast[1]
    
    if tree is not None:
        for child in tree.children:  # Acceder a los hijos del árbol
            if isinstance(child, Token):
                if move == "WIDTH":
                    out.write(f"{indent}t.width({child.value})\n")
                if move == "FD":
                    out.write(f"{indent}t.forward({child.value})\n")
                if move == "BK":
                    out.write(f"{indent}t.backward({child.value})\n")
                if move == "LT":
                    out.write(f"{indent}t.left({child.value})\n")
                if move == "RT":
                    out.write(f"{indent}t.right({child.value})\n")
            elif isinstance(child, Tree):
                print(f"  Child Tree: {child.data}")
    else:
        if move == "PD":
            out.write(f"{indent}t.pendown()\n")
        if move == "PU":
            out.write(f"{indent}t.penup()\n")
   
    
    
    
comparison_map = {
    "==": "==",
    "!=": "!=",
    "<": "<",
    ">": ">",
    "<=": "<=",
    ">=": ">=",
    "!": "not ",
}

def translate_boolean_expression(ast, out=''):
    """Traduce recursivamente expresiones booleanas a Python"""
    if isinstance(ast, Token):
        out+= comparison_map[ast.value] if True else ast.value
        return out

    if ast.data == "boolean_condition":
        return translate_boolean_expression(ast.children[0])

    elif ast.data == "boolean_term":
        if len(ast.children) == 1:
            if isinstance(ast.children[0], Token):
                return ast.children[0].value
            return translate_boolean_expression(ast.children[0])

        # Manejo de NOT
        if ast.children[0] == "!":
            for c in ast.children:
                out = translate_boolean_expression(c, out)

        # Manejo de AND
        elif len(ast.children) == 3 and ast.children[1].type == "AND":
            left = translate_boolean_expression(ast.children[0])
            right = translate_boolean_expression(ast.children[2])
            out += f"({left} and {right})"
            return out

        # Manejo de OR----+
        elif len(ast.children) == 3 and ast.children[1].type == "OR":
            left = translate_boolean_expression(ast.children[0])
            right = translate_boolean_expression(ast.children[2])
            out += f"({left} or {right})"
            return out

    elif ast.data == "comparison":
        left, op, right = ast.children
        out += f"{left.value} {comparison_map[op.value]} {right.value}"
        return out

    return out


def translate_range_parameters(args,out = ""):
    """Traduce los argumentos de range a una cadena Python"""
    if isinstance(args, Token):
        return args.value

    if args.data == "range_parameters":
        for c in args.children:
            out += translate_range_parameters(c,out)
        return out
   


# This function will traverse the AST and you can use it to emit the
# code you want at every node of it.
def translate_program(ast, out, indent_level=0):
    
    print(ast.pretty())

    indent = ' ' * (indent_level)  # 4 spaces per indentation level
    
    if ast.data == "start":
        out.write("import turtle\n")
        out.write("t = turtle.Turtle()\n")
        
        # Primero procesamos todas las definiciones de funciones
        for c in ast.children:
            if isinstance(c, tree.Tree) and c.data == "procedure_declaration":
                translate_program(c, out)

        # Luego procesamos el resto de instrucciones
        for c in ast.children:
            if not (isinstance(c, tree.Tree) and c.data == "procedure_declaration"):
                translate_program(c, out)
        
        
        out.write("turtle.mainloop() \n")
    
    elif ast.data == "command":
        if isinstance(ast.children[0], Token):
            move_instruction(ast.children, out, indent)
        else:
            for c in ast.children:
                translate_program(c, out, indent_level)

    elif ast.data == "code_sequence":
        for i in ast.children:
            if not isinstance(i, Token):
                translate_program(i, out, indent_level)
    
    elif ast.data == "procedure_declaration":
        name = ast.children[1].value
        params = []
        if len(ast.children) > 4:
            parameter_sequence = ast.children[3]
            if parameter_sequence.data == "parameter_sequence":
                params = [param.value for param in parameter_sequence.children if param.type == "NAME"]

        out.write(f"{indent}def {name}({', '.join(params)}):\n")

        block_node = ast.children[-1]
        for instruction in block_node.children:
            if not isinstance(instruction, Token):
                translate_program(instruction, out, indent_level + 1)
        out.write("\n")

    elif ast.data == "procedure_invocation":
        name = ast.children[0].value
        args = []
        if len(ast.children) > 2:
            argument_sequence = ast.children[2].children
            for arg in argument_sequence:
                if not isinstance(arg, Token):
                    args.append(arg.children[0].value)
        out.write(f"{indent}{name}({','.join(args)})\n")

    elif ast.data == "conditional_statement":
        condition = translate_boolean_expression(ast.children[1])
        out.write(f"{indent}if {condition}:\n")
        translate_program(ast.children[2], out, indent_level + 1)
        if len(ast.children) > 3:
            out.write(f"{indent}else:\n")
            translate_program(ast.children[4], out, indent_level + 1)

    elif ast.data == "single_iteration":
        var = ast.children[1].value
        range_parameters = translate_range_parameters(ast.children[5])
        out.write(f"{indent}for {var} in range({range_parameters}):\n")
        translate_program(ast.children[7], out, indent_level + 1)

    elif ast.data == "double_iteration":
        var1 = ast.children[1].value
        var2 = ast.children[3].value
        range_parameters1 = translate_range_parameters(ast.children[7].children[2])
        range_parameters2 = translate_range_parameters(ast.children[9].children[2])
        out.write(f"{indent}for {var1},{var2} in zip(range({range_parameters1}), range({range_parameters2})):\n")
        translate_program(ast.children[11], out, indent_level + 1)
    
    

input = sys.argv[1]
output = sys.argv[1] + str(".py")
parser = Lark(high_logo_grammar)
print("Input file: ", input)
print("Output file: ", output)


with open(input) as inputFile:
    with open(output, 'w') as out:
        ast = parser.parse(inputFile.read())
    
        tree.pydot__tree_to_png(ast, "tree.png")
        tree.pydot__tree_to_dot(ast, "tree.dot", rankdir="TD")
    
        translate_program(ast, out)
        
        print("\nCOMPILACION EXITOSA!\n")

print("El programa se ejecutara automaticamente en 5 segundos...")       
time.sleep(2)
if os.path.exists("program.hlogo.py"):
    print("Ejecutando el archivo generado...")
    subprocess.run(["python", "program.hlogo.py"])
else:
    print("El archivo no se ha generado aún.")

            