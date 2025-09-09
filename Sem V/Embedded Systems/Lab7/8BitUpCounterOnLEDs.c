#include <LPC17xx.h>


void delay(void) {
		unsigned int i ;
    for (i = 0; i < 200000; i++);
}

int main(void) {
	   unsigned int counter = 0;

    LPC_PINCON->PINSEL0 &= ~(0xFFFFFFFF);

    LPC_GPIO0->FIODIR |= (0xFF << 4);

    LPC_GPIO0->FIOMASK = ~(0xFF << 4);


    while (1) {
        LPC_GPIO0->FIOCLR = 0xFF << 4;  
        LPC_GPIO0->FIOSET = (counter << 4);

        delay();

        counter = (counter + 1)% 256;
    }
}
