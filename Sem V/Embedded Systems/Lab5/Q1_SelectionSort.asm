    AREA RESET, DATA, READONLY
    EXPORT __Vectors

__Vectors
    DCD 0x10001000         
    DCD Reset_Handler      
    ALIGN

    AREA mycode, CODE, READONLY
    ENTRY
    EXPORT Reset_Handler


Reset_Handler
    LDR R0, =SRC           
    MOV R1, #10           

    MOV R2, #0            

OuterLoop
    CMP R2, R1
    BGE Done               

    SUB R3, R1, #1        
    CMP R2, R3
    BGE Done              

    MOV R4, R2             
    ADD R5, R0, R2, LSL #2 
    LDR R6, [R5]          

    ADD R7, R2, #1         

InnerLoop
    CMP R7, R1
    BGE Swap               

    ADD R8, R0, R7, LSL #2 
    LDR R9, [R8]           

    CMP R9, R6
    BGE NoChange           

    MOV R4, R7             
    MOV R6, R9             

NoChange
    ADD R7, R7, #1         
    B InnerLoop

Swap
    CMP R4, R2
    BEQ NoSwap             

    
    ADD R5, R0, R2, LSL #2
    ADD R8, R0, R4, LSL #2

    LDR R9, [R5]
    LDR R10, [R8]

    STR R10, [R5]
    STR R9, [R8]

NoSwap
    ADD R2, R2, #1        
    B OuterLoop

Done
    B Done                 

STOP B STOP
    AREA mydata, DATA, READWRITE
SRC DCD 0x00ABCDF, 0x0012345, 0x000DCEF, 0x0AB1234, 0x0001032, 0x21231223, 0x0023FE1A, 0x0AB564E, 0x0012345, 0xABCDE123 

    END
