// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

//R0 = max
//R1 = max index
//R2 = min
//R3 = min index

//loop the whole list find the 
//i is index
@14
D=M
@i
M=D-1//start 1 before so that we can inc i in the start of the loop 
@15
D=M

    
(LOOP)
    @i
    M=M+1
    A=M //i++

    D=M
    @0
    D=D-M
    @MAX
    D;JGT //check if Arr[i] > max
    
    @i
    A = M 
    D=M
    @2
    D=D-M
    @MIN
    D;JLT //check if Arr[i] < min
    @CHECK
    0;JMP
    
    (MAX)
    @0
    M = M+D
    @i
    D = M
    @1
    M = D
    @CHECK
    0;JMP

    (MIN)
    @2
    M = M+D
    @i
    D = M
    @3
    M = D
    
    (CHECK)
    @14
    D=M
    @15
    D=D+M
    @i
    D=D-M
    @SWAP
    D;JLE

    @LOOP
    0;JMP

    (SWAP)
    @0
    D = M
    @3
    A = M
    M = D
    @2
    D = M
    @1
    A = M
    M = D


    (END)
    @END
    0;JMP

    (SWAP)
    @0
    D = M
    @3
    A = M
    M = D
    @2
    D = M
    @1
    A = M
    M = D


    (END)
    @END
    0;JMP