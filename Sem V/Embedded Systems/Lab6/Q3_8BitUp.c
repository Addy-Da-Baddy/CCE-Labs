#include <LPC17xx.h>

int main(void) {
    LPC_PINCON->PINSEL2 &= 0x3FFFFFFF;
    LPC_PINCON->PINSEL3 &= 0xFFFF0000;
    LPC_GPIO1->FIODIR |= 0x00FF8000;

    unsigned int base = 0x8000;
    int i = 0;

    while (1) {
        LPC_GPIO1->FIOSET = base << i;
        LPC_GPIO1->FIOCLR = base << i;
        i++;
        if (i == 8) i = 0;
    }
}
//8 Bit Up Counter