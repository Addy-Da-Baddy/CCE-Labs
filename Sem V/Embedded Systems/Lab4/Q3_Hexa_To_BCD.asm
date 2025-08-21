    AREA RESET, DATA, READONLY
    EXPORT __Vectors ; Hex to BCD

__Vectors
    DCD 0x10001000
    DCD Reset_Handler
    ALIGN

    AREA mycode, CODE, READONLY
    ENTRY
    EXPORT Reset_Handler

Reset_Handler
    LDR R0, =HEX_NUM        
    LDR R1, =BCD_RESULT    
    LDRB R2, [R0]           

    MOV R3, R2              
    MOV R4, #10
    UDIV R5, R3, R4         
    MLS R6, R5, R4, R3      

    LSL R5, R5, #4          
    ORR R7, R5, R6          

    STRB R7, [R1]           

STOP
    B STOP                  

    AREA mydata, DATA, READWRITE
HEX_NUM     DCB 0x19         
BCD_RESULT  DCB 0x00         

    END
