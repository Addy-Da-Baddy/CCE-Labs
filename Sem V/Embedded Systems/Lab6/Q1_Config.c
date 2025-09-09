//Program to configure pins P0.4 to P0.11 as GPIO outputs in LPC1768

#include <LPC17xx.h>

int main(void) {
    LPC_PINCON->PINSEL0 &= ~(0xFFFFFFFF);
		LPC_GPIO0->FIODIR |= 0xFF << 4;
		LPC_GPIO0->FIOMASK = ~(0xFF << 4);

    while (1) {
        LPC_GPIO0->FIOSET = 0xFF << 4;
        LPC_GPIO0->FIOCLR = 0xFF << 4;
    }
}
