// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// Assumes that R0 >= 0, R1 >= 0, and R0 * R1 < 32768.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//// Replace this comment with your code.

// puts 0 in R2
// loop R0 times
//      R2 = R2 + R1 

// adds 1+...+100.
    @i // i refers to some mem. location.
    M=1 // i=1
    @sum // sum refers to some mem. location.
    M=0 // sum=0
(LOOP)
    @i
    D=M // D=i
    @1
    D=D-M // D=i-RAM[1]
    @END
    D;JGT // If (i-100)>0 goto END
    @0
    D=M // D=RAM[0]
    @sum
    M=D+M // sum=sum+i
    @i
    M=M+1 // i=i+1
    @LOOP
    0;JMP
    @sum
    D=M
    @2
    M=D
(end)
    @end
    0;JMP