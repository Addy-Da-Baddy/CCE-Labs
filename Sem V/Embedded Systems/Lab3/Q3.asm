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
    LDR R0, =HEX_NUM        ; Address of hex input
    LDR R1, =BCD_RESULT     ; Address to store BCD output
    LDRB R2, [R0]           ; Load hex number (e.g., 0x19)

    MOV R3, R2              ; Copy to R3
    MOV R4, #10
    UDIV R5, R3, R4         ; R5 = R3 / 10 ? tens digit
    MLS R6, R5, R4, R3      ; R6 = R3 - (R5 × 10) ? units digit

    LSL R5, R5, #4          ; Shift tens digit to upper nibble
    ORR R7, R5, R6          ; Combine tens and units ? packed BCD

    STRB R7, [R1]           ; Store result

STOP
    B STOP                  ; Infinite loop

    AREA mydata, DATA, READWRITE
HEX_NUM     DCB 0x19         ; Hex input: 25 in decimal
BCD_RESULT  DCB 0x00         ; Placeholder for BCD result

    END
