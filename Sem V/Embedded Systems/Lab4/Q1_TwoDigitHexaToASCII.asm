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
        LDR   R0, =HEX_INPUT       ; input address
        LDR   R1, =ASCII_OUTPUT    ; output address
        LDR   R2, [R0]             ; 32-bit hex number

        MOV   R3, #8               ; loop counter (8 nibbles)

LOOP
        ; extract highest nibble using mask
        MOV   R4, R2, LSR #28      ; move top nibble to lower 4 bits

        ; convert nibble to ASCII
        CMP   R4, #9
        BCS   HEX_LETTER           ; if >9 → 'A'..'F'
        ADD   R4, R4, #0x30        ; '0'..'9'
        B     STORE

HEX_LETTER
        ADD   R4, R4, #0x37        ; 'A'..'F'

STORE
        STRB  R4, [R1], #1         ; store ASCII and increment dest

        ; shift number left by 4 to bring next nibble to top
        LSL   R2, R2, #4

        SUBS  R3, R3, #1           ; decrement counter
        BNE   LOOP                  ; repeat if not done

DONE
        B DONE                      ; infinite loop

;----------------------------------------------------
        AREA mydata, DATA, READWRITE
HEX_INPUT     DCD 0x1234ABCD      ; example input
ASCII_OUTPUT  SPACE 8             ; 8 ASCII characters output

        END
