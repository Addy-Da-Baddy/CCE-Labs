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
		MOV R0, #10
		MOV R1, #0x10
		MOV R2, #2_1010
		MOV R2, #4_23
		MOV R4, #-8
STOP 	B STOP
	END