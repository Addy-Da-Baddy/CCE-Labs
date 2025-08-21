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
    MOV R0, #5            
    BL factorial          
    B done                

factorial
    PUSH {R0, LR}         

    CMP R0, #1            
    BLE base_case        

    SUB R0, R0, #1        
    BL factorial          

    POP {R1, LR}          
    MUL R0, R0, R1        
    BX LR                 

base_case
    MOV R0, #1            
    POP {R1, LR}          
    BX LR

done B done                

    AREA mydata, DATA, READWRITE
