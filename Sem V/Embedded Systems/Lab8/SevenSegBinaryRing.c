#include <LPC17xx.h>

const unsigned char binCode[2] = {
    0x3F, // 0
    0x06  // 1
};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 4000; j++);
    }
}

int main() {
    unsigned int pattern;
    unsigned int i;
    unsigned int digit;
    unsigned int cycle;
    unsigned int temp;

    LPC_PINCON->PINSEL0 &= ~(0xFF << 8);     
    LPC_PINCON->PINSEL3 &= ~(0xFF << 14);   

    LPC_GPIO0->FIODIR |= 0xFF << 4;         
    LPC_GPIO1->FIODIR |= 0x0F << 23;        

    pattern = 0x01;  

    while (1) {
        for (cycle = 0; cycle < 125; cycle++) {  
            temp = pattern;

            for (i = 0; i < 4; i++) {
                digit = (temp >> i) & 0x01;

                LPC_GPIO0->FIOCLR = 0xFF << 4;
                LPC_GPIO1->FIOCLR = 0x0F << 23;

                LPC_GPIO0->FIOSET = binCode[digit] << 4;
                LPC_GPIO1->FIOSET = i << 23;

                delay_ms(5);
            }
        }

        pattern = (pattern << 1) & 0x0F;
        if (pattern == 0) {
            pattern = 0x01;
        }
    }
}
