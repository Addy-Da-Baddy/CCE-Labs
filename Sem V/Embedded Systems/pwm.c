#include <LPC17xx.h>

volatile int val = 1;               
volatile unsigned int duty = 100;  

#define PWM_PERIOD 3000

void PWM_Init(void) {
    LPC_SC->PCONP |= (1 << 6);  

    LPC_PINCON->PINSEL3 &= ~(0x3 << 14);  
    LPC_PINCON->PINSEL3 |=  (0x2 << 14); 

    LPC_PWM1->PR = 0;          
    LPC_PWM1->MR0 = PWM_PERIOD; 
    LPC_PWM1->MR4 = duty;       

    LPC_PWM1->MCR = (1 << 1) | (1 << 0); 

    LPC_PWM1->PCR = (1 << 12);   

    LPC_PWM1->LER = (1 << 0) | (1 << 4); 

    LPC_PWM1->TCR = (1 << 3) | (1 << 0); 
		LPC_PWM1->LER = (1 << 4) | 1 << 0;   


    NVIC_EnableIRQ(PWM1_IRQn);   
}

void PWM1_IRQHandler(void) {
    if (LPC_PWM1->IR & (1 << 0)) { 
        LPC_PWM1->IR = (1 << 0);    

        if (duty >= PWM_PERIOD) {
            val = -1;    
        } else if (duty <= 0) {
            val = 1;     
        }
        duty += val * 100;

        LPC_PWM1->MR4 = duty;       
    }
}

int main(void) {
    PWM_Init();

    while (1) {
    }
}
