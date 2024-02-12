"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output = output_stream
        self.symbols = {
            "add": "M=D+M",
            "sub": "M=M-D",
            "and": "M=M&D",
            "or": "M=M|D",
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "gt": "D;JGT",
            "lt": "D;JLT",
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
            "constant": "",
            "static": "",
            "pointer": "@3",
            "temp": "@5"
        }
        self.label_counter = 0
        self.set_file_name(output_stream.name)

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """

        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.file_name = filename[filename.rindex("\\") + 1:filename.rindex('.')]

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        output = []
        if command in ["add", "sub", "and", "or"]:
            # Pop Stack into D.
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            # Access to Stack[-1]
            output.append("@SP")
            output.append("A=M-1")
            # Use the Arithmetic Operator
            output.append(self.symbols[command])
    
        elif command in ["neg", "not"]:
            # Access to Stack[-1]
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
        elif command in ["eq", "gt", "lt"]:
            jump_label = "CompLabel" + str(self.label_counter)
            self.label_counter += 1
            # Pop Stack into D.
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            # Access to Stack[-1]
            output.append("@SP")
            output.append("A=M-1")
            # Calculate the difference
            output.append("D=M-D")
            output.append("M=-1")
            # Load the jump label into A.
            output.append("@" + jump_label)
            # Jump if the statement is True.
            # Else update the Stack to False.
            output.append(self.symbols[command])
            # Set the Stack[-1] to False
            output.append("@SP")
            output.append("A=M-1")
            output.append("M=0")
            # Jump label for the True state.
            output.append("(" + jump_label + ")")
        for line in output:
            self.output.write(f"{line}\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index   (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

        output = []
        if command == "C_PUSH":
            if segment == "constant":
                output.append("@" + str(index))
                output.append("D=A")
                output.append("@SP")
                output.append("AM=M+1")
                output.append("A=A-1")
                output.append("M=D")
            elif segment in ["local", "argument", "this", "that", "temp", "pointer"]:
                # Put the index value into D.
                output.append("@" + str(index))
                output.append("D=A")
                # Put the base value into A.
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    # Resolve where the segment refers to.
                    output.append(self.symbols[segment])
                    output.append("A=M")
                # Calculate the source address into A.
                output.append("A=D+A")
                # Put the source value into D.
                output.append("D=M")
                # Put D value into where SP points to.
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                # Increment the stack pointer.
                output.append("@SP")
                output.append("M=M+1")
            elif segment == "static":
                # Calculate the source address into A.
                output.append("@" + self.file_name + "." + str(index))
                # Put the source value into D.
                output.append("D=M")
                # Put D value into where SP points to.
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                # Increment the stack pointer.
                output.append("@SP")
                output.append("M=M+1")
        elif command == "C_POP":
            if segment in ["local", "argument", "this", "that", "temp", "pointer"]:
                # Put the index value into D.
                output.append("@" + str(index))
                output.append("D=A")
                # Put the base value into A.
                if segment == "temp" or segment == "pointer":
                    output.append(self.symbols[segment])
                else:
                    # Resolve where the segment refers to.
                    output.append(self.symbols[segment])
                    output.append("A=M")
                # Calculate the source address into D.
                output.append("D=D+A")
                # Put D value into R13 for future use.
                output.append("@R13")
                output.append("M=D")
                # Pop stack value into D.
                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                # Put D value into where R13 points to.
                output.append("@R13")
                output.append("A=M")
                output.append("M=D")
            elif segment == "static":
                # Pop stack value into D.
                output.append("@SP")
                output.append("AM=M-1")
                output.append("D=M")
                # Put the source address into A.
                output.append("@" + self.file_name + "." + str(index))
                # Put D value into static address.
                output.append("M=D")


        for line in output:
            self.output.write(f"{line}\n")

        
    
    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        label = self.file_name+'.'+label
        self.output.write(f"({label})\n")
        pass
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        self.output.write(f"@{label}\n0;JMP\n")

        pass
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        self.output.write(f"@SP\nAM=M-1\nD=M\n@{label}\nD;JNE\n")
        pass
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        function_name = self.file_name+'.'+function_name
        self.output.write(f"({function_name})\n")
        for i in range(int(n_vars)):
            self.output.write("@0\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n")
        pass
    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        self.output.write(f"@{self.file_name}.{function_name}$ret.{self.label_counter}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output.write("@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output.write("@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output.write(f"@{int(n_args)+5}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n")
        self.output.write("@SP\nD=M\n@LCL\nM=D\n")
        self.output.write(f"@{function_name}\n0;JMP\n")
        self.output.write(f"({self.file_name}.{function_name}$ret.{self.label_counter})\n")
        self.label_counter += 1

        pass
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        self.output.write("@LCL\nD=M\n@R13\nM=D\n")  # Save LCL in R13
        self.output.write("@5\nA=D-A\nD=M\n@R14\nM=D\n")  # Save return address in R14
        self.output.write("@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n")  # Set return value to caller's stack
        self.output.write("@ARG\nD=M+1\n@SP\nM=D\n")  # Reset SP of the caller
        self.output.write("@R13\nAM=M-1\nD=M\n@THAT\nM=D\n")  # Restore THAT
        self.output.write("@R13\nAM=M-1\nD=M\n@THIS\nM=D\n")  # Restore THIS
        self.output.write("@R13\nAM=M-1\nD=M\n@ARG\nM=D\n")  # Restore ARG
        self.output.write("@R13\nAM=M-1\nD=M\n@LCL\nM=D\n")  # Restore LCL
        self.output.write("@R14\nA=M\n0;JMP\n")  # Jump to return address
        pass
