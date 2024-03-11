"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!
        self.class_table = {}
        self.subroutine_table = {}
        self.index_static = 0
        self.index_field = 0
        self.index_arg = 0
        self.index_var = 0
        pass

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # Your code goes here!
        print(self.subroutine_table)
        self.subroutine_table = {}
        self.index_arg = 0
        self.index_var = 0
        pass
    
    def print_data(self, name: str) -> None:
        #print all the data of variable with name

        if self.type_of(name) == None:
            print("not a variable - ", name)
            return
        print("symbol is - ", name)
        print("kind - ", self.kind_of(name))
        print("type - ", self.type_of(name))
        print("index - ", self.index_of(name), "\n")


    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        # Your code goes here!
        if kind in ["STATIC", "FIELD"]:
            if kind == "STATIC":
                index = self.index_static
                self.index_static += 1
            else:
                index = self.index_field
                self.index_field += 1
            self.class_table[name] = [type, kind, index]
        else:
            if kind == "ARG":
                index = self.index_arg
                self.index_arg += 1
            else:
                index = self.index_var
                self.index_var += 1
            self.subroutine_table[name] = [type, kind, index]
        print("defiend a new variable: ")
        self.print_data(name)
        pass

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        # Your code goes here!
        match kind:
            case "STATIC":
                return self.index_static
            case "FIELD":
                return self.index_field
            case "ARG":
                return self.index_arg
            case "VAR":
                return self.index_var
        pass

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!
        ret = self.subroutine_table.get(name)
        if ret == None:
            ret = self.class_table.get(name)
        if ret == None:
            return ret
        return ret[1]

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # Your code goes here!
        ret = self.subroutine_table.get(name)
        if ret == None:
            ret = self.class_table.get(name)
        if ret == None:
            return ret
        return ret[0]
        pass

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # Your code goes here!
        ret = self.subroutine_table.get(name)
        if ret == None:
            ret = self.class_table.get(name)
        if ret == None:
            return ret
        return ret[2]
        pass
