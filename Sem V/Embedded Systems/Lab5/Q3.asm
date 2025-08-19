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
    LDR R0, = NUM1        ; R0 = base address of array
    MOV R1, #5           ; R1 = hardcoded array length
    MOV R2, #0            ; R2 = index (i)
    MOV R3, #0xDCEF            ; R3 = target value to search

search_loop
    CMP R2, R1
    BGE not_found         ; if i >= length, not found

    ADD R4, R0, R2, LSL #2 ; R4 = address of array[i]
    LDR R5, [R4]           ; R5 = array[i]

    CMP R5, R3
    BEQ found             ; if array[i] == target, found

    ADD R2, R2, #1         ; i++
    B search_loop

found
    ; R2 contains the index of the found element
    B done

not_found
    MOV R2, #-1           ; R2 = -1 (not found)

done
    B done     
	
	

STOP B STOP                
NUM1 DCD 0xABCDF12, 0x12345, 0xDCEF, 0xAB1234
  


    END