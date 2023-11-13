// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(LOOP)
    @KBD
    D=M
    @BLACK
    D;JGT
    
    (W_loop)
    @D
    M=0
    D=D+1
    @W_loop
    //D-;JMP
    
    @LOOP
    0;JMP
(BLACK)
    //black
    @SCREEN
    D=A
    
(BLOP)
    A=D
    M=-1
    D=D+1
    @BLOP
    0;JMP
    

    @LOOP
    0;JMP
