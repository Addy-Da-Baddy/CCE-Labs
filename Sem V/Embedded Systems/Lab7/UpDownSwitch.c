#include <LPC17xx.h>

void delay(void) {
    for (volatile int i = 0; i < 200000; i++);
}

int main(void) {
    unsigned int counter = 0;

    LPC_PINCON->PINSEL0 = 0x00000000;
    LPC_PINCON->PINSEL1 = 0x00000000;
    LPC_PINCON->PINSEL2 = 0x00000000;
    LPC_PINCON->PINSEL3 = 0x00000000;
    LPC_PINCON->PINSEL4 = 0x00000000;

    LPC_GPIO2->FIODIR &= ~(1 << 0);

    LPC_GPIO0->FIODIR |= (0xFF << 15);
    LPC_GPIO0->FIOMASK = ~(0xFF << 15);  

    while (1) {
        if (LPC_GPIO2->FIOPIN & (1 << 0)) {
            counter = (counter + 1) % 256;  
        } else {
            counter = (counter - 1) % 256;  
        }

        LPC_GPIO0->FIOCLR = 0xFF << 15;       
        LPC_GPIO0->FIOSET = counter << 15;    

        delay();
    }
}
