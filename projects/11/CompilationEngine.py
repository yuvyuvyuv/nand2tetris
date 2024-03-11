"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

START = 1
END = 2

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output_stream = output_stream
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.VMWriter = VMWriter(output_stream)
        self.SymbolTable = SymbolTable()
        self.class_name = ""
        self.subroutine_name = ""
        self.tab_conut = 0
        pass
    
    def write_start(self, input) -> None:
        t = "  " * self.tab_conut
        #self.output_stream.write(t+f"<{input}>\n")
        self.tab_conut +=1
       
    def write_end(self, input) -> None:
        self.tab_conut -=1
        t = "  " * self.tab_conut
        #self.output_stream.write(t+f"</{input}>\n")
        
    def advance(self) -> None:
        self.tokenizer.advance()
        #self.terminal_write()
          
    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.advance()  # Consume the "class" keyword
        self.class_name = self.tokenizer.identifier()
        self.advance()  # Consume the className
        self.advance()  # Consume the "{" keyword
        
        print(self.tokenizer.keyword())
        while self.tokenizer.keyword() in ["static", "field"]:            
            self.compile_class_var_dec()  # Compile the class variable declarations
        
        while self.tokenizer.keyword() in ["constructor", "function", "method"]:            
            self.compile_subroutine()  # Compile the subroutines
        
        self.advance()  # Consume the "}" keyword
        
        #print(self.SymbolTable.subroutine_table)
        #print("class table:----------------------------------------------")
        #print(self.SymbolTable.class_table)
        #print("endfile")
        
    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        var_kind = self.tokenizer.peek_val().upper()
        self.advance()  #  static,field
        var_type = self.tokenizer.peek_val()
        self.advance()  #  variable type
        var_name = self.tokenizer.peek_val()
        self.advance()  #  variable name
        self.SymbolTable.define(var_name,var_type,var_kind)


        while self.tokenizer.peek_val() == ",":
            self.advance()  #  comma ","
            var_name = self.tokenizer.peek_val()
            self.advance()  #  variable name
            self.SymbolTable.define(var_name,var_type,var_kind)
            
        self.advance()  #  the semicolon ";"
          
    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.SymbolTable.start_subroutine()


        subroutine_type = self.tokenizer.keyword()
        self.advance()  #  the subroutine type (method, function, or constructor)

        if subroutine_type == "method":
            self.SymbolTable.define("this", self.class_name,"ARG")
        ret_type = self.tokenizer.keyword()
        self.advance()  # Consume the return type
        self.subroutine_name = self.tokenizer.identifier()
        self.advance()  # Consume the subroutine name

        
        self.advance()  # Consume the opening parenthesis "("
        self.compile_parameter_list()  # Compile the parameter list
        self.advance()  # Consume the closing parenthesis ")"

        self.advance()  # Consume the opening curly brace "{"
        while self.tokenizer.peek_val() == "var":
            self.compile_var_dec()  # Compile the variable declarations

        self.VMWriter.write_function(f"{self.class_name}.{self.subroutine_name}",self.SymbolTable.var_count("VAR"))
        if subroutine_type == "constructor":
            self.VMWriter.write_push("CONST",self.SymbolTable.var_count("FIELD"))
            self.VMWriter.write_call("Memory.alloc",1)
            self.VMWriter.write_pop("POINTER",0)
        elif subroutine_type == "method":
            self.VMWriter.write_push("ARG",0)
            self.VMWriter.write_pop("POINTER",0)
        
        self.compile_statements()  # Compile the statements
        
        self.advance()  # Consume the closing curly brace "}"
        if subroutine_type == "constructor":
            self.VMWriter.write_push("POINTER",0)
        
        if ret_type == "void":
            self.VMWriter.write_push("CONST",0)
        self.VMWriter.write_return()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here
        while self.tokenizer.symbol() != ")":
            var_type = self.tokenizer.keyword()
            self.advance()  # Consume the parameter type
            var_name = self.tokenizer.identifier()
            self.advance()  # Consume the parameter name
            self.SymbolTable.define(var_name, var_type, "ARG")
            if self.tokenizer.symbol() == ",":
                self.advance()  # Consume the comma ","

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
       
        self.advance()  #  var

        var_type = self.tokenizer.peek_val()
        self.advance()  #  variable type
        var_name = self.tokenizer.peek_val()
        self.advance()  #  variable name

        self.SymbolTable.define(var_name,var_type,"VAR")

        while self.tokenizer.peek_val() == ",":
            self.advance()  #  comma ","
            var_name = self.tokenizer.peek_val()
            self.advance()  #  variable name
            self.SymbolTable.define(var_name,var_type,"VAR")

        self.advance()  #  the semicolon ";"
        pass
        
    def compile_statements(self) -> None:
        
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        while self.tokenizer.symbol() != "}":
            token_type = self.tokenizer.keyword()
            if token_type == "let":
                self.compile_let()
            elif token_type == "if":
                self.compile_if()
            elif token_type == "while":
                self.compile_while()
            elif token_type == "do":
                self.compile_do()
            elif token_type == "return":
                self.compile_return()
            else:
                break
        
    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.advance()  # Consume the "do" keyword
        name = self.tokenizer.identifier()
        self.advance() # name
        # Compile the subroutine call
        if self.tokenizer.symbol() == "(":
            self.advance()
            num_of_exp = self.compile_expression_list()
            self.VMWriter.write_call(f"{self.class_name}.{name}",num_of_exp) #maybe not class_name, maybe +1
        elif self.tokenizer.symbol() == ".":
            self.advance() # eat the .
            sub_name = self.tokenizer.identifier()
            self.advance() # eat the name
            self.advance() # eat the (
            num_of_exp = self.compile_expression_list()
            self.VMWriter.write_call(f"{name}.{sub_name}",num_of_exp)
            self.advance() # eat the )
        self.advance()  # Consume the ";" symbol
        print ("do is pver")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.advance()  # Consume the "let" keyword
        var_name = self.tokenizer.peek_val()
        self.advance()  # Consume the variable name
        self.SymbolTable.print_data(var_name)
        if self.tokenizer.peek_val() == "[":
            self.advance()  # Consume the opening square bracket "["
            self.compile_expression()  # Compile the expression inside the square brackets
            self.advance()  # Consume the closing square bracket "]"

        self.advance()  # Consume the equals sign "="
        self.compile_expression()  # Compile the expression on the right side of the equals sign
        self.advance()  # Consume the semicolon ";"

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.advance()  # Consume the "while" keyword
        self.advance()  # Consume the opening parenthesis "("
        self.compile_expression()  # Compile the condition expression
        self.advance()  # Consume the closing parenthesis ")"
        self.advance()  # Consume the opening curly brace "{"
        self.compile_statements()  # Compile the statements inside the while loop
        self.advance()  # Consume the closing curly brace "}"
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.advance()  # Consume the "return" keyword

        if self.tokenizer.symbol() != ";":
            self.compile_expression()  # Compile the expression to be returned

        self.advance()  # Consume the semicolon ";"

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.advance()  # Consume the "if" keyword
        self.advance()  # Consume the opening parenthesis "("
        self.compile_expression()  # Compile the condition expression
        self.advance()  # Consume the closing parenthesis ")"
        self.advance()  # Consume the opening curly brace "{"
        self.compile_statements()  # Compile the statements inside the if block
        self.advance()  # Consume the closing curly brace "}"

        if self.tokenizer.peek_val() == "else":
            self.advance()  # Consume the "else" keyword
            self.advance()  # Consume the opening curly brace "{"
            self.compile_statements()  # Compile the statements inside the else block
            self.advance()  # Consume the closing curly brace "}"       
    


    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()  # Compile the first term of the expression
        op_val = self.tokenizer.symbol()
        while op_val in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            print(op_val, "opexpression_________________________")
            self.advance()  # Consume the operator
            self.compile_term()  # Compile the next term of the expression
            self.VMWriter.write_binary(op_val)
            op_val = self.tokenizer.symbol()            

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        token_type = self.tokenizer.peek_type()
        token_val = self.tokenizer.peek_val()
        print(token_val,token_type, "term_________________________")
        
        if self.tokenizer.int_val() != None: #token is an integer
            self.VMWriter.write_push("CONST",self.tokenizer.int_val())
            self.advance()
        elif self.tokenizer.string_val() != None: #token is a string
            self.VMWriter.write_push("CONST",len(self.tokenizer.string_val()))
            self.VMWriter.write_call("String.new",1)
            for char in self.tokenizer.string_val():
                self.VMWriter.write_push("CONST",ord(char))
                self.VMWriter.write_call("String.appendChar",2) #maybe 1?
            self.advance()
        elif  self.tokenizer.keyword() != None: #token is a keyword
            token_val = self.tokenizer.keyword()
            if token_val == "true":
                self.VMWriter.write_push("CONST",1)
                self.VMWriter.write_arithmetic("NEG")
            elif token_val == "false" or token_val == "null":
                self.VMWriter.write_push("CONST",0)
            elif token_val == "this":
                self.VMWriter.write_push("POINTER",0)
            self.advance()
        elif self.tokenizer.identifier() != None: #token is an identifier
            token_val = self.tokenizer.identifier()
            self.SymbolTable.print_data(token_val)
            self.advance()
            if self.tokenizer.symbol() == "[":
                self.advance()
                self.compile_expression()#needs to be written!!!!!!!
                self.advance()
            elif self.tokenizer.symbol() == "(":
                self.advance()
                self.compile_expression_list()#needs to be written!!!!!!!!
                self.advance()
            elif self.tokenizer.symbol() == ".":
                self.advance()                    
                self.advance()#needs to be written!!!!!!
                self.advance()
                self.compile_expression_list()
                self.advance()
            else:
                self.VMWriter.write_push(self.SymbolTable.kind_of(token_val),self.SymbolTable.index_of(token_val))
        elif self.tokenizer.symbol() != None: #token is symbol - then is
            token_val = self.tokenizer.symbol()
            if token_val == "(":
                self.advance()
                self.compile_expression()
                self.advance()
            else:
                self.advance()
                print(token_val)
                self.compile_term()
                self.VMWriter.write_unary(token_val)

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        num_of_expressions = 0
        while self.tokenizer.symbol() != ")":
            self.compile_expression()
            num_of_expressions += 1
            if self.tokenizer.symbol() == ",":
                self.advance() 
        return num_of_expressions   
