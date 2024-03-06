"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

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

        self.tab_conut = 0
        pass

    def terminal_write(self) -> None:
        t = "  " * self.tab_conut
        self.output_stream.write(t+f"<{self.tokenizer.token_type()}> ")
        self.output_stream.write(f"{self.tokenizer.curr_tok[0]} ")
        self.output_stream.write(f"</{self.tokenizer.token_type()}>\n")
    
    def write_start(self, input) -> None:
        t = "  " * self.tab_conut
        self.output_stream.write(t+f"<{input}>\n")
        self.tab_conut +=1
       
    def write_end(self, input) -> None:
        self.tab_conut -=1
        t = "  " * self.tab_conut
        self.output_stream.write(t+f"</{input}>\n")
        
    def advance_and_write(self) -> None:
        self.tokenizer.advance()
        self.terminal_write()
          
    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.write_start("class")
        self.terminal_write()  # Consume the "class" keyword
        
        self.advance_and_write()  # Consume the className
        
        self.advance_and_write()  # Consume the "{" keyword
        
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() in ["static", "field"]:
            self.compile_class_var_dec()  # Compile the class variable declarations
        
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() in ["constructor", "function", "method"]:
            self.compile_subroutine()  # Compile the subroutines
        
        self.advance_and_write()  # Consume the "}" keyword

        self.write_end("class")
        
    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.write_start("classVarDec")  # Start of varDec

        self.advance_and_write()  #  static,field

        self.advance_and_write()  #  variable type

        self.advance_and_write()  #  variable name

        while self.tokenizer.peek_val() == ",":
            self.advance_and_write()  #  comma ","
            self.advance_and_write()  #  variable name
            
        self.advance_and_write()  #  the semicolon ";"
        
        self.write_end("classVarDec")  # End of varDec
  
    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.write_start("subroutineDec")
        self.advance_and_write()  #  the subroutine type (method, function, or constructor)
        self.advance_and_write()  # Consume the return type
        self.advance_and_write()  # Consume the subroutine name
        self.advance_and_write()  # Consume the opening parenthesis "("
        self.compile_parameter_list()  # Compile the parameter list
        self.advance_and_write()  # Consume the closing parenthesis ")"

        #subrotine body
        self.write_start("subroutineBody")

        self.advance_and_write()  # Consume the opening curly brace "{"
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() == "var":
            self.compile_var_dec()  # Compile the variable declarations
        self.compile_statements()  # Compile the statements
        self.advance_and_write()  # Consume the closing curly brace "}"
        self.write_end("subroutineBody")
        self.write_end("subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here
        self.write_start("parameterList")
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() != ")":
            self.advance_and_write()  # Consume the parameter type
            self.advance_and_write()  # Consume the parameter name
            if self.tokenizer.peek_val() == ",":
                self.advance_and_write()  # Consume the comma ","

        self.write_end("parameterList")
        pass

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.write_start("varDec")  # Start of varDec

        self.advance_and_write()  #  var

        self.advance_and_write()  #  variable type

        self.advance_and_write()  #  variable name

        while self.tokenizer.peek_val() == ",":
            self.advance_and_write()  #  comma ","
            self.advance_and_write()  #  variable name
            
        self.advance_and_write()  #  the semicolon ";"
        
        self.write_end("varDec")  # End of varDec
        pass
        
    def compile_statements(self) -> None:
        
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.write_start("statements")
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() != "}":
            token_type = self.tokenizer.peek_val()
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
        self.write_end("statements")
        
    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.write_start("doStatement")
        self.advance_and_write()  # Consume the "do" keyword
        self.advance_and_write() # name
        # Compile the subroutine call
        if self.tokenizer.peek_val() == "(":
            self.advance_and_write()
            self.compile_expression_list()
            self.advance_and_write()
        elif self.tokenizer.peek_val() == ".":
            self.advance_and_write()                    
            self.advance_and_write()
            self.advance_and_write()
            self.compile_expression_list()
            self.advance_and_write()
        self.advance_and_write()  # Consume the ";" symbol
        self.write_end("doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.write_start("letStatement")
        self.advance_and_write()  # Consume the "let" keyword
        self.advance_and_write()  # Consume the variable name

        if self.tokenizer.peek_val() == "[":
            self.advance_and_write()  # Consume the opening square bracket "["
            self.compile_expression()  # Compile the expression inside the square brackets
            self.advance_and_write()  # Consume the closing square bracket "]"

        self.advance_and_write()  # Consume the equals sign "="
        self.compile_expression()  # Compile the expression on the right side of the equals sign
        self.advance_and_write()  # Consume the semicolon ";"
        self.write_end("letStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.write_start("whileStatement")
        self.advance_and_write()  # Consume the "while" keyword
        self.advance_and_write()  # Consume the opening parenthesis "("
        self.compile_expression()  # Compile the condition expression
        self.advance_and_write()  # Consume the closing parenthesis ")"
        self.advance_and_write()  # Consume the opening curly brace "{"
        self.compile_statements()  # Compile the statements inside the while loop
        self.advance_and_write()  # Consume the closing curly brace "}"
        self.write_end("whileStatement")
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.write_start("returnStatement")
        self.advance_and_write()  # Consume the "return" keyword

        if self.tokenizer.peek_val() != ";":
            self.compile_expression()  # Compile the expression to be returned

        self.advance_and_write()  # Consume the semicolon ";"
        self.write_end("returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.write_start("ifStatement")
        self.advance_and_write()  # Consume the "if" keyword
        self.advance_and_write()  # Consume the opening parenthesis "("
        self.compile_expression()  # Compile the condition expression
        self.advance_and_write()  # Consume the closing parenthesis ")"
        self.advance_and_write()  # Consume the opening curly brace "{"
        self.compile_statements()  # Compile the statements inside the if block
        self.advance_and_write()  # Consume the closing curly brace "}"

        if self.tokenizer.peek_val() == "else":
            self.advance_and_write()  # Consume the "else" keyword
            self.advance_and_write()  # Consume the opening curly brace "{"
            self.compile_statements()  # Compile the statements inside the else block
            self.advance_and_write()  # Consume the closing curly brace "}"
        self.write_end("ifStatement")
       
    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.write_start("expression")
        self.compile_term()  # Compile the first term of the expression
        
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.advance_and_write()  # Consume the operator
            self.compile_term()  # Compile the next term of the expression
        self.write_end("expression")
        pass

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
        self.write_start("term")
        token_type = self.tokenizer.peek_token()
        if token_type != None:
            token_type = token_type[1]
            if token_type == "integerConstant":
                self.advance_and_write()
            elif token_type == "stringConstant":
                self.advance_and_write()
            elif token_type == "keyword":
                self.advance_and_write()
            elif token_type == "identifier":
                self.advance_and_write()
                if self.tokenizer.peek_val() == "[":
                    self.advance_and_write()
                    self.compile_expression()
                    self.advance_and_write()
                elif self.tokenizer.peek_val() == "(":
                    self.advance_and_write()
                    self.compile_expression_list()
                    self.advance_and_write()
                elif self.tokenizer.peek_val() == ".":
                    self.advance_and_write()                    
                    self.advance_and_write()
                    self.advance_and_write()
                    self.compile_expression_list()
                    self.advance_and_write()
                    
            elif token_type == "symbol":
                if self.tokenizer.peek_val() == "(":
                    self.advance_and_write()
                    self.compile_expression()
                    self.advance_and_write()
                else:
                    self.advance_and_write()
                    self.compile_term()
        self.write_end("term")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.write_start("expressionList")
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() != ")":
            self.compile_expression()
            if self.tokenizer.has_more_tokens() and self.tokenizer.peek_val() == ",":
                self.advance_and_write()    
        self.write_end("expressionList")
