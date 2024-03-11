"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """

        input_lines = input_stream.read().splitlines()
        self.tokens = self.tokenize(input_lines)
        self.curr_index = 0
        self.curr_tok = self.tokens[self.curr_index]
        self.len = len(self.tokens)

       
    def tokenize(self, input_lines) -> list:
        
        keyword_token = ['class','constructor','function','method'
                         ,'field','static','var','int','char'
                         ,'boolean','void','true','false','null'
                         ,'this','let','do','if','else','while','return']
        symbol_token = ['{','}' , '(' , ')' , '[' , ']' , '.' 
                         , ',' , ';' , '+' ,'-' , '*' , '/' , '&'
                         , '|' , '<' , '>' , '=' , '~' , '^' , '#']

        # integerConstant_token  A decimal number in the range 0-32767.
        # StringConstant: '"' A sequence of Unicode characters not including double quote or newline '"'
        # identifier: A sequence of letters, digits, and underscore ('_') not 
        #          starting with a digit. You can assume keywords cannot be
        #          identifiers, so 'self' cannot be an identifier, etc'.
        tokens = []
        comment_flag = False
        string_const_flag = False
        for line in input_lines:
            buffer = ""
            int_mode = False
            skip = 0
            for i in range(len(line)):
                c = line[i]
                if skip > 0:
                    skip -= 1
                    continue

                # alot of edge cases

                # find end of string const
                if string_const_flag:
                    # if end of string const, append string buffer and clean
                    if c == "\"":
                        string_const_flag = False
                        tokens.append((buffer,"stringConstant"))
                        buffer = ""
                        continue
                    # add to string buffer
                    buffer += c
                    continue
                # start of string
                if c == "\"":
                    if not comment_flag:
                        string_const_flag = True
                    continue

                # find end of mult line comment
                if comment_flag:
                    if c == "*":
                        if i < len(line)-1:
                            next = line[i+1]
                            if next == "/":
                                comment_flag = False
                                skip = 1
                                continue
                    continue

                # find start of comment 
                if c == "/":
                    if i < len(line)-1:
                        next = line[i+1]
                        # check if multi line
                        if next == "*":
                            comment_flag = True
                            skip = 1
                            continue
                        # check if oneliner
                        elif next == "/":
                            comment_flag = False
                            break

                # nomore edge cases

                if int_mode:
                    if not self.str_is_int(c):
                        tokens.append((buffer,"integerConstant"))
                        buffer = ""
                        int_mode = False


                # check if symbol token
                if c in symbol_token:
                    if buffer != "":
                        if buffer in keyword_token:
                            tokens.append((buffer,"keyword"))
                        elif self.str_is_int(buffer):
                            tokens.append((buffer,"integerConstant"))
                        else:
                            tokens.append((buffer,"identifier"))
                        buffer = ""
                    tokens.append((c,"symbol"))
                    
                    continue
                
                # if whitespace end of buffer and check cases
                if c.isspace():
                    if buffer == "":
                        continue
                    if buffer in keyword_token:
                        tokens.append((buffer,"keyword"))
                    elif self.str_is_int(buffer):
                        tokens.append((buffer,"integerConstant"))
                    else:
                        tokens.append((buffer,"identifier"))
                    buffer = ""
                    continue
                
                if self.str_is_int(c) and buffer == "":
                    int_mode = True
                

                        

                buffer += c

        return tokens


    def str_is_int(self, s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False
    
    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return self.curr_index + 1 < self.len
        pass

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        if self.has_more_tokens():
            self.curr_index += 1
            self.curr_tok = self.tokens[self.curr_index]
        
        pass
        
    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "keyword", "symbol", "identifier", "integerConstant", "stringConstant"
        """
        # Your code goes here!
        return self.curr_tok[1]
        pass

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "keyword".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        if self.token_type() == "keyword":
            return self.curr_tok[0]

        pass

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "symbol".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        if self.token_type() == "symbol":
            return self.curr_tok[0]

        pass

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "identifier".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!        
        if self.token_type() == "identifier":
            return self.curr_tok[0]

        pass

    def int_val(self) -> int:
        
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "integerConstant".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        if self.token_type() == "integerConstant":
            return int(self.curr_tok[0])
        pass

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "stringConstant".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        if self.token_type() == "stringConstant":
            return int(self.curr_tok[0])

        pass
    def peek_token(self) -> str:
        """Returns the next token without consuming it."""
        if not self.has_more_tokens():
            return (None,None)
        return self.tokens[self.curr_index+1]
    def peek_val(self) -> str:
        """Returns the next token without consuming it."""
        if not self.has_more_tokens():
            return None
        return self.tokens[self.curr_index+1][0]
    def peek_type(self) -> str:
        """Returns the next token without consuming it."""
        if not self.has_more_tokens():
            return None
        return self.tokens[self.curr_index+1][1]