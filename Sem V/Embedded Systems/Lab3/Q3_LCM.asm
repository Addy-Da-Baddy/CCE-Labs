    AREA RESET, DATA, READONLY ; LCM of Two Numbers
    EXPORT __Vectors

__Vectors
    DCD 0x10001000          
    DCD Reset_Handler
    ALIGN

    AREA mycode, CODE, READONLY
    ENTRY
    EXPORT Reset_Handler

Reset_Handler
    LDR R0, =NUM1
    LDR R1, =NUM2
    LDR R10, =RES
    LDR R4, [R0]            
    LDR R5, [R1]            
    MOV R2, #1              

Loop
    MUL R6, R4, R2         
    UDIV R7, R6, R5         
    MLS R3, R7, R5, R6      
    CMP R3, #0
    BEQ Return             
    ADD R2, R2, #1          
    B Loop

Return
    STR R6, [R10]           

STOP
    B STOP                 
NUM1 DCD 4
NUM2 DCD 6
    AREA mydata, DATA, READWRITE

RES  DCD 0

    END
