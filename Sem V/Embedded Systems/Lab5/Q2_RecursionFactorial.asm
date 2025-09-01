        AREA RESET, DATA, READONLY
        EXPORT __Vectors

__Vectors
        DCD 0x10001000
        DCD Reset_Handler
        ALIGN

;----------------------------------------------------
        AREA mycode, CODE, READONLY
        ENTRY
        EXPORT Reset_Handler

Reset_Handler
        LDR   R0, =NUM      ; load address of number
        LDR   R0, [R0]      ; load number to R0
        BL    FACTORIAL      ; call factorial
        LDR   R1, =RESULT
        STR   R0, [R1]      ; store result

STOP B STOP

;----------------------------------------------------
; Recursive factorial function
; Input: R0 = n
; Output: R0 = n!
FACTORIAL
        CMP   R0, #1
        BLE   FACT_END      ; if n <= 1, return 1

        PUSH  {R0, LR}      ; save n and return address

        SUB   R0, R0, #1    ; n-1
        BL    FACTORIAL      ; recursive call

        POP   {R1, LR}      ; restore n and return address
        MUL   R0, R0, R1    ; n * factorial(n-1)
        BX    LR

FACT_END
        MOV   R0, #1
        BX    LR

;----------------------------------------------------
        AREA mydata, DATA, READWRITE
NUM     DCD 5            ; calculate 5!
RESULT  DCD 0

        END



