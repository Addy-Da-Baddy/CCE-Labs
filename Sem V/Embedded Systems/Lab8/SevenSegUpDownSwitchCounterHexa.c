#include <LPC17xx.h>

const unsigned char hexCode[16] = {
    0x3F, 0x06, 0x5B, 0x4F,
    0x66, 0x6D, 0x7D, 0x07,
    0x7F, 0x6F, 0x77, 0x7C,
    0x39, 0x5E, 0x79, 0x71
};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 4000; j++);
    }
}

int main() {
    unsigned int count;
    unsigned int i;
    unsigned int temp;
    unsigned int digit;
    unsigned int cycle;
    unsigned int switchState;

    LPC_PINCON->PINSEL0 &= ~(0xFF << 8);    
    LPC_PINCON->PINSEL3 &= ~(0xFF << 14);   
    LPC_PINCON->PINSEL4 &= ~(0x3 << 0);      

    LPC_GPIO0->FIODIR |= 0xFF << 4;        
    LPC_GPIO1->FIODIR |= 0x0F << 23;        
    LPC_GPIO2->FIODIR &= ~(1 << 0);         

    count = 0;

    while (1) {
        switchState = !(LPC_GPIO2->FIOPIN & (1 << 0));  

        for (cycle = 0; cycle < 125; cycle++) {  
            temp = count;

            for (i = 0; i < 4; i++) {
                digit = temp % 16;
                temp = temp / 16;

                LPC_GPIO0->FIOCLR = 0xFF << 4;
                LPC_GPIO1->FIOCLR = 0x0F << 23;

                LPC_GPIO0->FIOSET = hexCode[digit] << 4;
                LPC_GPIO1->FIOSET = i << 23;

                delay_ms(5);
            }
        }

        if (!switchState) {
            count = (count + 1) % 0x10000;
        } else {
            count = (count == 0) ? 0xFFFF : count - 1;
        }
    }
}