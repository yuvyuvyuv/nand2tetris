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
@15
D=M
@i
M=D
@14
D=M

    
(LOOP)
    A=D
    
    D=D+1
    @KBD
    D=D-A
    @LOOP
    D;JGE
    @KBD
    D=D+A
    @BLOP
    0;JMP
