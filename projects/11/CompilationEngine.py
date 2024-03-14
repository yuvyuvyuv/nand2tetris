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
        

        self.VMWriter = VMWriter(output_stream)
        self.SymbolTable = SymbolTable()
        self.class_name = ""
        self.subroutine_name = ""
        pass
    
    
    def advance(self) -> None:
        self.tokenizer.advance()

          
    def compile_class(self) -> None:
        """Compiles a complete class.
        class className {
            classVarDec*
            subroutineDec*
        }
        """
        self.advance()  # Consume the "class" keyword
        self.class_name = self.tokenizer.identifier()
        self.advance()  # Consume the className
        self.advance()  # Consume the "{" keyword
        
        while self.tokenizer.keyword() in ["static", "field"]:            
            self.compile_class_var_dec()  # Compile the class variable declarations
        
        while self.tokenizer.keyword() in ["constructor", "function", "method"]:            
            self.compile_subroutine()  # Compile the subroutines
        
        self.advance()  # Consume the "}" keyword
    

    def compile_class_var_dec(self) -> None:
        self.compile_vars()


    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field.

        a decleration of a subroutine

        (constructor|function|method)  (void|type) subroutineName ( paramaterList ){
            varDec*
            statment*
        }
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
        while self.tokenizer.keyword() == "var":
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
            if var_type == None:
                var_type = self.tokenizer.identifier()

            self.advance()  # Consume the parameter type
            var_name = self.tokenizer.identifier()
            self.advance()  # Consume the parameter name
            self.SymbolTable.define(var_name, var_type, "ARG")
            if self.tokenizer.symbol() == ",":
                self.advance()  # Consume the comma ","

    def compile_var_dec(self) -> None:
        self.compile_vars()
    
    def compile_vars(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
       
        var_kind = self.tokenizer.keyword().upper() #  static,field,var
        self.advance()  
        var_type = self.tokenizer.keyword()  #  variable type
        if var_type == None:
            var_type = self.tokenizer.identifier()
            
        self.advance() 
        var_name = self.tokenizer.identifier()  #  variable name

        self.advance() 
        self.SymbolTable.define(var_name,var_type,var_kind)
        # page 20 - mapping vars, location of variable changes its saved adrress
        #!!!!!!

        while self.tokenizer.symbol() == ",":
            self.advance()  #  comma ","
            var_name = self.tokenizer.identifier()
            self.advance()  #  variable name
            self.SymbolTable.define(var_name,var_type,var_kind)
            
        self.advance()  #  the semicolon ";"

    

        
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
        if self.tokenizer.symbol() in ["(","."]:
            self.compile_subroutine_call(name)
        self.VMWriter.write_pop("TEMP",0) #YANK
        self.advance()  # Consume the ";" symbol

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.advance()  # Consume the "let" keyword
        var_name = self.tokenizer.identifier()
        self.advance()  # Consume the variable name

        # needs changing
        if self.tokenizer.symbol() == "[":
            self.compile_array_usage(var_name)
            self.advance()  # Consume the equals sign "="
            self.compile_expression()  # Compile the expression on the right side of the equals sign
            self.VMWriter.write_pop("TEMP",0)
            self.VMWriter.write_pop("POINTER",1)
            self.VMWriter.write_push("TEMP",0)
            self.VMWriter.write_pop("THAT",0)
        else:
            self.advance()  # Consume the equals sign "="
            self.compile_expression()  # Compile the expression on the right side of the equals sign
            self.VMWriter.write_pop(self.SymbolTable.kind_of(var_name),self.SymbolTable.index_of(var_name))

        self.advance()  # Consume the semicolon ";"

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        L1 = "WHILE_START"+str(self.VMWriter.label_counter)
        L2 = "WHILE_END"+str(self.VMWriter.label_counter)
        self.VMWriter.write_label(L1)


        self.advance()  # Consume the "while" keyword
        self.advance()  # Consume the opening parenthesis "("
        self.compile_expression()  # Compile the condition expression

        self.VMWriter.write_arithmetic("NOT")
        self.VMWriter.write_if(L2)
        self.advance()  # Consume the closing parenthesis ")"
        self.advance()  # Consume the opening curly brace "{"
        self.compile_statements()  # Compile the statements inside the while loop
        self.advance()  # Consume the closing curly brace "}"

        self.VMWriter.write_goto(L1)

        self.VMWriter.write_label(L2)
        


    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.advance()  # Consume the "return" keyword
        if self.tokenizer.symbol() != ";":
            self.compile_expression()  # Compile the expression to be returned
        self.VMWriter.write_return()
        self.advance()  # Consume the semicolon ";"

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        L1 = "IF_START"+str(self.VMWriter.label_counter)
        L2 = "IF_END"+str(self.VMWriter.label_counter)


        self.advance()  # Consume the "if" keyword
        self.advance()  # Consume the opening parenthesis "("
        self.compile_expression()  # Compile the condition expression
        
        self.VMWriter.write_arithmetic("NOT")

        self.VMWriter.write_if(L1)
        self.advance()  # Consume the closing parenthesis ")"
        self.advance()  # Consume the opening curly brace "{"
        self.compile_statements()  # Compile the statements inside the if block
        self.advance()  # Consume the closing curly brace "}"

        self.VMWriter.write_goto(L2)
        self.VMWriter.write_label(L1)
        if self.tokenizer.keyword() == "else":
            self.advance()  # Consume the "else" keyword
            self.advance()  # Consume the opening curly brace "{"
            self.compile_statements()  # Compile the statements inside the else block
            self.advance()  # Consume the closing curly brace "}"       
        self.VMWriter.write_label(L2)
        
    


    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()  # Compile the first term of the expression
        op_val = self.tokenizer.symbol()
        while op_val in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
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
            self.advance()
            if self.tokenizer.symbol() == "[":
                self.compile_array_usage(token_val)
                self.VMWriter.write_pop("POINTER",1)
                self.VMWriter.write_push("THAT",0)
                
            elif self.tokenizer.symbol() in ["(","."]: #token is subroutine call
                self.compile_subroutine_call(token_val)
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
                self.compile_term()
                self.VMWriter.write_unary(token_val)

    def compile_array_usage(self,arrName) -> None:
        # push the adrees of arr[exp]
        self.VMWriter.write_push(self.SymbolTable.kind_of(arrName),self.SymbolTable.index_of(arrName))
        self.advance() # eat the [
        self.compile_expression()
        self.VMWriter.write_arithmetic("ADD")
        self.advance()# eat the ]

    def compile_subroutine_call(self, name) -> None:
        """Compiles a subroutine call."""
        # Your code goes here!
        if self.tokenizer.symbol() == "(":
                self.advance()
                self.VMWriter.write_push("POINTER",0)
                num_of_exp = self.compile_expression_list()
                self.VMWriter.write_call(f"{self.class_name}.{name}",num_of_exp+1) #maybe not class_name, maybe +1
                self.advance() # eat the )

        elif self.tokenizer.symbol() == ".":
            self.advance() # eat the .
            sub_name = self.tokenizer.identifier()
            self.advance() # eat the name
            self.advance() # eat the ( 
                  
            meth = 0
            if self.SymbolTable.kind_of(name) != None:
                self.VMWriter.write_push(self.SymbolTable.kind_of(name),self.SymbolTable.index_of(name))
                name = self.SymbolTable.type_of(name)
                meth = 1
            num_of_exp = self.compile_expression_list() + meth

            self.VMWriter.write_call(f"{name}.{sub_name}",num_of_exp)
            self.advance() # eat the )
        pass

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        num_of_expressions = 0
        while self.tokenizer.symbol() != ")":
            self.compile_expression()
            num_of_expressions += 1
            if self.tokenizer.symbol() == ",":
                self.advance() 
        return num_of_expressions   
