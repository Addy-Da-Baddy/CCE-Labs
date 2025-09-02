#include <LPC17xx.h>

int main(void) {
    LPC_PINCON->PINSEL2 &= 0x3FFFFFFF;
    LPC_PINCON->PINSEL3 &= 0xFFFF0000;
    LPC_GPIO1->FIODIR |= 0x00FF8000;

    while (1) {
        unsigned int x = 0x8000;
        for (int i = 0; i < 9; i++) {
            LPC_GPIO1->FIOSET = x;
            x = x << 1;
        }

        x = 0x8000;
        for (int i = 0; i < 9; i++) {
            LPC_GPIO1->FIOCLR = x;
            x = x << 1;
        }
    }
}
