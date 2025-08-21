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
    ADD R1, R0, #36      
    MOV R4, #5           

Up
    LDR R2, [R0]         
    LDR R3, [R1]         

    STR R3, [R0]         
    STR R2, [R1]         

    ADD R0, R0, #4      
    SUB R1, R1, #4       

    SUBS R4, R4, #1      
    BNE Up               

STOP
    B STOP
             



    AREA mydata, DATA, READWRITE
SRC DCD 0xABCDF, 0x12345, 0xDCEF, 0xAB1234, 0x1032, 0x21231223, 0x23FE1A, 0xAB564E, 0x12345, 0xABCDE123 


    END
	


