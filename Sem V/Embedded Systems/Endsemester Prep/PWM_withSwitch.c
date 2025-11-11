#include <LPC17xx.h>

#define PWM_PERIOD 3000

void PWM_Init(void) {
    LPC_SC->PCONP |= (1 << 6);  // Power up PWM1

    // Configure P1.23 as PWM1.4 (PINSEL3 bits 15:14 = 10)
    LPC_PINCON->PINSEL3 &= ~(0x3 << 14);
    LPC_PINCON->PINSEL3 |=  (0x2 << 14);

    LPC_PWM1->PR = 0;               // No prescale
    LPC_PWM1->MR0 = PWM_PERIOD;     // Period value
    LPC_PWM1->MR4 = PWM_PERIOD * 0.75;  // Start with 75% duty

    LPC_PWM1->MCR = (1 << 1);       // Reset on MR0
    LPC_PWM1->PCR = (1 << 12);      // Enable PWM1.4 output
    LPC_PWM1->LER = (1 << 0) | (1 << 4); // Enable latch updates

    LPC_PWM1->TCR = (1 << 3) | (1 << 0); // Enable PWM and counter
}

int main(void) {
    // Initialize PWM
    PWM_Init();

    // Configure P2.0 as GPIO input (switch)
    LPC_PINCON->PINSEL4 &= ~(3 << 0); // P2.0 as GPIO
    LPC_GPIO2->FIODIR &= ~(1 << 0);   // Input

    unsigned int duty;

    while (1) {
        // Read switch (active LOW assumed)
        if (!(LPC_GPIO2->FIOPIN & (1 << 0))) {
            // Switch pressed → 50%
            duty = PWM_PERIOD * 0.5;
        } else {
            // Switch not pressed → 75%
            duty = PWM_PERIOD * 0.75;
        }

        // Update MR4 with new duty
        LPC_PWM1->MR4 = duty;
        LPC_PWM1->LER |= (1 << 4); // Latch the new value
        for (volatile int d = 0; d < 10000; d++); // small debounce delay
    }
}
