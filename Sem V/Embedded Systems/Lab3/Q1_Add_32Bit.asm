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
        LDR R0, =NUMS         
        MOV R1, #10            
        MOV R2, #0             
        MOV R4, #0             

Loop
        LDR R3, [R0], #4       
        ADDS R2, R2, R3        
        ADC  R4, R4, #0        
        SUBS R1, R1, #1
        BNE Loop

        LDR R5, =RESULT        
        STR R2, [R5]           
        STR R4, [R5, #4]      

        B Stop

Stop    B Stop

NUMS    DCD 0xFFFFFFF0, 0xABCDEF01, 0x80000000, 0x11111111, 0x22222222
        DCD 0x33333333, 0x44444444, 0x55555555, 0x66666666, 0x77777777

        AREA mydata, DATA, READWRITE
RESULT  DCD 0, 0               

        END
