#include <LPC17xx.h>
#include <stdio.h>

//PWM Channel PWMM1.4 on P1.23

int main(){
    LPC_SC->PCONP | = 0xFFFFFFFF; // Power to all peripherals
    LPC_PINCON->PINSEL3 |= (2 << 14); // P1.23 as PWM1.4
    LPC_PWM1->MCR = (1<<1) } (1 <<0);
    LPC_PWM1->PCR = (1 << 12);
    LPC_PWM1->TCR = (1 << 0) | (1 << 3); // Enable PWM and Counter
    LPC_PWM1->MR0 = 4000;
    LPC_PWM1->MR4 = 0;
    LPC_PWM1->LER = (1 << 0) | (1 << 4);
    NVIC_EnableIRQ(PWM1_IRQn);
    while (1){
    }
}

void PWM1_IRQHandler(void){
    if LPC_PWM1->IR & (1 << 0)){
        LPC_PWM1->IR = (1 << 0); // Clear interrupt flag
        static int direction = 1;
        if (direction == 1){
            LPC_PWM1->MR4 += 200;
            if (LPC_PWM1->MR4 >= LPC_PWM1->MR0){
                direction = 0;
            }
        } else {
            LPC_PWM1->MR4 -= 200;
            if (LPC_PWM1->MR4 <= 0){
                direction = 1;
            }
        }
        LPC_PWM1->LER |= (1 << 4); // Update MR4
    }
}