; BC TO HEX


        AREA mycode, CODE, READONLY
        ENTRY
        EXPORT Reset_Handler

Reset_Handler
        LDR   R0, =BCD_INPUT     ; address of input
        LDR   R1, [R0]           ; R1 = 32-bit BCD number
        MOV   R2, #0             ; result = 0
        MOV   R3, #8             ; loop counter = 8 digits

BCD_LOOP
        ; Extract top nibble (MSD first)
        MOV   R4, R1, LSR #28    ; get top 4 bits into R4
        AND   R4, R4, #0xF       ; mask lower nibble

        ; result = result * 10 + digit
        MOV   R5, #10
        MLA   R2, R2, R5, R4     ; R2 = R2*10 + R4

        ; Shift left to bring next nibble
        LSL   R1, R1, #4

        SUBS  R3, R3, #1
        BNE   BCD_LOOP

        ; R2 now contains final HEX value of BCD input
        LDR   R6, =HEX_OUTPUT
        STR   R2, [R6]

DONE    B DONE

;---------------------------
        AREA mydata, DATA, READWRITE
BCD_INPUT   DCD 0x12345678    ; Example BCD input
HEX_OUTPUT  DCD 0             ; Store hex result here











; HEX TO BC


HEX TO BC


     AREA RESET, DATA, READONLY
        EXPORT __Vectors ; Hex to BCD

__Vectors
        DCD 0x10001000
        DCD Reset_Handler
        ALIGN

;-------------------------------------------------
        AREA mycode, CODE, READONLY
        ENTRY
        EXPORT Reset_Handler

Reset_Handler
        LDR   R0, =HEX_NUM      ; input address
        LDR   R1, [R0]          ; load 32-bit hex number
        LDR   R2, =BCD_RESULT   ; output address
        MOV   R3, #0            ; BCD accumulator
        MOV   R4, #0            ; loop counter

;-------------------------
BCD_LOOP
        CMP   R4, #8            ; 8 decimal digits
        BGE   BCD_DONE

        MOV   R5, #10
        UDIV  R6, R1, R5        ; quotient
        MLS   R7, R6, R5, R1    ; remainder = next decimal digit

        LSL   R3, R3, #4        ; shift accumulator left
        ORR   R3, R3, R7        ; insert digit

        MOV   R1, R6            ; next number = quotient
        ADD   R4, R4, #1
        B     BCD_LOOP

;-------------------------
BCD_DONE
        ; Rotate accumulator to correct nibble order
        ROR   R3, R3, #4

        STR   R3, [R2]          ; store 32-bit BCD result

STOP
        B STOP

;-------------------------------------------------
        AREA mydata, DATA, READWRITE
HEX_NUM     DCD 0x12345678      ; example 32-bit input
BCD_RESULT  DCD 0               ; 32-bit BCD output

        END



HEX TO ASCII

AREA RESET, DATA, READONLY
        EXPORT __Vectors

__Vectors
        DCD 0x10001000         ; Initial SP
        DCD Reset_Handler      ; Reset vector
        ALIGN

;----------------------------------------------------
        AREA mycode, CODE, READONLY
        ENTRY
        EXPORT Reset_Handler

Reset_Handler
        LDR   R0, =HEX_INPUT       ; R0 = &HEX_INPUT
        LDR   R1, =ASCII_OUTPUT    ; R1 = &ASCII_OUTPUT
        LDR   R2, [R0]             ; R2 = 32-bit hex input

        MOV   R3, #8               ; loop counter (8 nibbles)

LOOP
        ; Get highest nibble
        MOV   R4, R2, LSR #28      ; top nibble → R4

        ; Convert nibble → ASCII
        CMP   R4, #9
        BCS   HEX_LETTER           ; if R4 >= 10 → A–F
        ADD   R4, R4, #0x30        ; else → '0'–'9'
        B     STORE

HEX_LETTER
        ADD   R4, R4, #0x37        ; 10→'A', 11→'B', …, 15→'F'

STORE
        STRB  R4, [R1], #1         ; store ASCII and post-increment R1
        LSL   R2, R2, #4           ; shift left → bring next nibble
        SUBS  R3, R3, #1           ; decrement loop counter
        BNE   LOOP

DONE
        B DONE                     ; stop forever

;----------------------------------------------------
        AREA mydata, DATA, READWRITE
HEX_INPUT     DCD 0x1234ABCD        ; example input
ASCII_OUTPUT  SPACE 8               ; 8-byte ASCII buffer

        END

ASCII to HEX

        AREA RESET, DATA, READONLY
        EXPORT __Vectors

__Vectors
        DCD 0x10001000         ; Initial SP
        DCD Reset_Handler      ; Reset vector
        ALIGN

;----------------------------------------------------
        AREA mycode, CODE, READONLY
        ENTRY
        EXPORT Reset_Handler

Reset_Handler
        LDR   R0, =ASCII_INPUT      ; R0 = address of ASCII input
        LDR   R1, =HEX_OUTPUT       ; R1 = address of HEX output
        MOV   R2, #0                ; accumulator for result
        MOV   R3, #8                ; loop counter (8 ASCII hex digits)

LOOP_ASCII2HEX
        LDR   R4, [R0], #4          ; load 4 bytes from memory, post-increment pointer
        ; only take the first byte of the word
        MOV   R4, R4, LSR #24       ; top byte = ASCII character

        ; convert ASCII → hex nibble
        CMP   R4, #'9'              ; if R4 <= '9'
        BCS   ASCII_LETTER
        SUB   R4, R4, #'0'          ; '0'-'9' → 0-9
        B      STORE_HEX

ASCII_LETTER
        SUB   R4, R4, #'A'          ; 'A'-'F' → 0-5 offset
        ADD   R4, R4, #10           

STORE_HEX
        LSL   R2, R2, #4            ; shift accumulator left 4 bits
        ORR   R2, R2, R4            ; insert nibble
        SUBS  R3, R3, #1
        BNE   LOOP_ASCII2HEX

        STR   R2, [R1]              ; store 32-bit HEX result

DONE
        B DONE                      

;----------------------------------------------------
        AREA mydata, DATA, READWRITE
ASCII_INPUT   DCD 0x31323334        ; example "1234ABCD" in ASCII (packed 4 bytes each)
HEX_OUTPUT    DCD 0x0

        END


        END
