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
    LDR R0, = NUM1
	LDR R1, = NUM2
	MOV R2, #4
	LDR R6, = RES
	MOVS R7, #0
	
Up
	LDR R3, [R0], #4
	LDR R4, [R1], #4
	ADCS R5,R3,R4
	SUB R2,#1
	TEQ R2,#0
	STR R5,[R6], #4
	BNE Up

	
	

STOP B STOP                
NUM1 DCD 0xABCDF12, 0x12345, 0xDCEF, 0xAB1234
NUM2 DCD 0x103221, 0x21231223, 0x23FE1A, 0xAB564E
    AREA mydata, DATA, READWRITE
RES DCD 0,0,0,0    


    END