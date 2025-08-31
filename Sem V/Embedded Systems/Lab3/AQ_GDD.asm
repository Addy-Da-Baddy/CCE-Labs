        AREA GCD_Prog, CODE, READONLY
        EXPORT Reset_Handler

Reset_Handler
        LDR     R0, =NUM1        ; pointer to first number
        LDR     R1, =NUM2        ; pointer to second number
        LDR     R10, =REST       ; pointer to store result
        LDR     R2, [R0]         ; R2 = NUM1
        LDR     R3, [R1]         ; R3 = NUM2

CMP_Check
        CMP     R2, R3
        BEQ     FIN              ; if equal, done

GCD
        CMP     R2, R3
        BGT     AGTB             ; if R2 > R3
        BLT     BGTA             ; if R2 < R3

AGTB
        SUBS    R2, R2, R3       ; a = a - b
        CMP     R2, R3
        BNE     GCD
        B       FIN

BGTA
        SUBS    R3, R3, R2       ; b = b - a
        CMP     R2, R3
        BNE     GCD
        B       FIN

FIN
        STR     R2, [R10]        ; store GCD
        B       FIN               ; loop forever
