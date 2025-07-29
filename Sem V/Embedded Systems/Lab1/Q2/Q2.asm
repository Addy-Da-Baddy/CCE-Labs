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
    LDR R1, =DST    
	MOV R2, #4
	
Up
	ADD R0, R0, #4
	SUBS R2, R2, #1
	BNE Up;
Exec
	STR R0,[R1]
	LDR R4,[R1]
	LDR R4,[R4]
	

STOP B STOP                
SRC DCD 0xABCDF, 0x12345, 0xDCEF, 0xAB1234, 0x1032, 0x21231223, 0x23FE1A, 0xAB564E, 0x12345, 0xABCDE123
    AREA mydata, DATA, READWRITE
DST DCD 0    


    END
