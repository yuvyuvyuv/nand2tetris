"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        
        input_lines = input_file.readlines()
        command_lines = []
        # delete whitespace 
        for line in input_lines:
            line = line[:line.find("//")]
            line = " ".join(line.split())
            if line != "" and line != " ":
                command_lines.append(line)
        
        self.command_lines = command_lines
        self.current_command_counter = 0
        if command_lines != []:
            self.current_command = command_lines[0]
        else:
            self.current_command = None
        pass

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_command_counter < len(self.command_lines)
        pass

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        if self.has_more_commands():
            self.current_command = self.command_lines[self.current_command_counter]
            self.current_command_counter += 1
        pass

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        c_arithmetic_words = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        if self.current_command.split()[0] in c_arithmetic_words:
            return "C_ARITHMETIC"
        elif "push" in self.current_command:
            return "C_PUSH"
        elif "pop" in self.current_command:
            return "C_POP"
        elif "label" in self.current_command:
            return "C_LABEL"
        elif "goto" in self.current_command:
            return "C_GOTO"
        elif "if" in self.current_command:
            return "C_IF"
        elif "function" in self.current_command:
            return "C_FUNCTION"
        elif "return" in self.current_command:
            return "C_RETURN"
        elif "call" in self.current_command:
            return "C_CALL"
        pass

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == "C_ARITHMETIC":
            return self.current_command
        elif self.command_type() != "C_RETURN":
            return self.current_command.split()[1]
        pass

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        two_arg_funcs = ["C_PUSH", "C_POP", "C_FUNCTION" , "C_CALL"]
        if self.command_type() in two_arg_funcs:
            return self.current_command.split()[2]
        pass
