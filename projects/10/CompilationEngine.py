"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


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

        pass

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        pass

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        pass

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.tokenizer.advance()  # Consume the subroutine type (method, function, or constructor)
        self.tokenizer.advance()  # Consume the return type
        self.tokenizer.advance()  # Consume the subroutine name
        self.tokenizer.advance()  # Consume the opening parenthesis "("
        self.compile_parameter_list()  # Compile the parameter list
        self.tokenizer.advance()  # Consume the closing parenthesis ")"
        self.tokenizer.advance()  # Consume the opening curly brace "{"
        self.compile_var_dec()  # Compile the variable declarations
        self.compile_statements()  # Compile the statements
        self.tokenizer.advance()  # Consume the closing curly brace "}"

    def peek_token(self) -> str:
        """Returns the next token without consuming it."""
        return self.tokenizer.peek()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes he
        parameters = []
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_token() != ")":
            parameter_type = self.tokenizer.advance()  # Consume the parameter type
            parameter_name = self.tokenizer.advance()  # Consume the parameter name
            parameters.append((parameter_type, parameter_name))
            if self.tokenizer.peek_token() == ",":
                self.tokenizer.advance()  # Consume the comma ","
        self.tokenizer.advance()  # Consume the closing parenthesis ")"
        pass

    def peek_token(self) -> str:
        """Returns the next token without consuming it."""
        return self.tokenizer.peek()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        pass

    def compile_statements(self) -> None:
        
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        while self.tokenizer.has_more_tokens() and self.tokenizer.peek_token() != "}":
            token = self.tokenizer.peek_token()
            if token == "let":
                self.compile_let()
            elif token == "if":
                self.compile_if()
            elif token == "while":
                self.compile_while()
            elif token == "do":
                self.compile_do()
            elif token == "return":
                self.compile_return()
            else:
                break

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.tokenizer.advance()  # Consume the "do" keyword
        self.compile_subroutine()  # Compile the subroutine call
        self.tokenizer.advance()  # Consume the ";" symbol
        pass

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        pass

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        pass

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        pass

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
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
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass
