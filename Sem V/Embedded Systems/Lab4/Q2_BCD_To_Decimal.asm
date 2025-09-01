    AREA RESET, DATA, READONLY ; Hex = (Upper nibble >> 4) � 10 + (Lower nibble & 0x0F)
 
    EXPORT __Vectors ; BCD TO HEX

__Vectors
    DCD 0x10001000
    DCD Reset_Handler
    ALIGN

    AREA mycode, CODE, READONLY
    ENTRY
    EXPORT Reset_Handler

Reset_Handler
    LDR R0, =BCD_NUM       
    LDR R1, =HEX_RESULT    
    LDRB R2, [R0]          

    MOV R3, R2, LSR #4     
    MUL R3, R3, #10        

    AND R4, R2, #0x0F      

    ADD R5, R3, R4         

    STRB R5, [R1]          

STOP
    B STOP                 

    AREA mydata, DATA, READWRITE
BCD_NUM     DCB 0x25       
HEX_RESULT  DCB 0x00        

    END
