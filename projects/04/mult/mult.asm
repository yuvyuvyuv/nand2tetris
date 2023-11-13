// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// Assumes that R0 >= 0, R1 >= 0, and R0 * R1 < 32768.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//// Replace this comment with your code.

// puts 0 in R2
// if R1 < 0 stop else
//      R2 = R2 + R0
//      R1 = R1 - 1

    @2 
    M=0 // R2=0
(LOOP)


    @1
    D=M-1 // D = R1 -1

    @END
    D;JLT // If D<=0 goto END
    @1
    M=D // R1 = R1-1 
    @0
    D=M // D=RAM[0]
    @2
    M=D+M // R2=R2+R0
    
    @LOOP
    0;JMP
    @2
    D=M

    
(END)
    @END
    0;JMP