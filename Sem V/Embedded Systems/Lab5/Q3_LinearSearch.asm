        AREA SEARCH, DATA, READONLY
        EXPORT __Vectors

__Vectors
        DCD 0x10001000
        DCD Reset_Handler
        ALIGN

;-----------------------------------------
        AREA mycode, CODE, READONLY
        ENTRY
        EXPORT Reset_Handler

Reset_Handler
        LDR   R0, =ARRAY       ; pointer to array
        LDR   R1, =TARGET      ; pointer to target value
        LDR   R2, [R1]         ; load target value
        LDR   R3, =RESULT      ; pointer to result
        MOV   R4, #0           ; index counter
        MOV   R5, #10          ; array length

Loop
        LDR   R6, [R0], #4     ; load next array element, increment pointer
        CMP   R6, R2
        BEQ   Found

        ADD   R4, R4, #1
        SUBS  R5, R5, #1
        BNE   Loop

        ; Not found
        MOV   R4, #-1
        STR   R4, [R3]
        B Done

Found
        STR   R4, [R3]         ; store index

Done
        B Done

;-----------------------------------------
        AREA mydata, DATA, READWRITE
ARRAY   DCD 10, 22, 35, 47, 52, 61, 73, 84, 91, 100
TARGET  DCD 52
RESULT  DCD 0

        END
