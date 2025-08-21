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
    LDR R0, =array        
    MOV R1, #10           
    MOV R2, #1            
outer_loop
    CMP R2, R1
    BGE done              
    ADD R3, R0, R2, LSL #2 
    LDR R4, [R3]           
    MOV R5, R2             

inner_loop
    SUB R6, R5, #1
    CMP R6, #0
    BLT insert_key        

    ADD R7, R0, R6, LSL #2 
    LDR R8, [R7]           
    CMP R8, R4
    BLE insert_key        

    ADD R9, R0, R5, LSL #2 
    STR R8, [R9]           
    MOV R5, R6            

    B inner_loop

insert_key
    ADD R10, R0, R5, LSL #2 
    STR R4, [R10]           

    ADD R2, R2, #1         
    B outer_loop

done
    B done                  

STOP B STOP

    AREA mydata, DATA, READWRITE
array
    DCD 5, 3, 7, 2, 9, 6, 1, 8, 4, 0

    END
