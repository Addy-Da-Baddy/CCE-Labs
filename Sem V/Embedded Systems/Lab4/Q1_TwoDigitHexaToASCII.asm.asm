    AREA RESET, DATA, READONLY ; Two Digit hexa to ASCII
    EXPORT __Vectors

__Vectors
    DCD 0x10001000
    DCD Reset_Handler
    ALIGN

    AREA mycode, CODE, READONLY
    ENTRY
    EXPORT Reset_Handler

Reset_Handler
    LDR R1, =HEX_INPUT      
    LDRB R1, [R1]           

    LDR R3, =ASCII_OUTPUT   
    MOV R10, #2             

UP
    AND R2, R1, #0x0F       

    CMP R2, #9
    BCS NUMERIC             
    ADD R2, R2, #0x07      

NUMERIC
    ADD R2, R2, #0x30       

    STRB R2, [R3], #1       
    LSR R1, R1, #4          
    SUBS R10, R10, #1      
    BNE UP                  

STOP
    B STOP

    AREA mydata, DATA, READWRITE
HEX_INPUT     DCB 0xAF             
ASCII_OUTPUT  SPACE 2              

    END
