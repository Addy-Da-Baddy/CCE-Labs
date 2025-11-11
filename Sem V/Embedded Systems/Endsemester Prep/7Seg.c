#include <LPC17xx.h>
#include <stdio.h>
//P0.4 – P0.11 → Segment lines (a–g + DP) for 7-segment display

//P1.23 – P1.26 → Digit select lines (for 4-digit multiplexing)

//P2.0 → Push button input (mode-change / increment control)

void init(){
    LPC_PINCON->PINSEL0 = 0;
    LPC_PINCON->PINSEL3 = 0;
    LPC_PINCON->PINSEL4 = 0;

    LPC_GPIO0->FIODIR |= (0xFF<<4); 
    LPC_GPIO1->FIODIR |= (0x0F<<23); 
    LPC_GPIO2->FIODIR &= ~(1<<0);   
}

void delay(unsigned int count){
    for(int i=0;i<count;i++);
}

unsigned char hexCode[10] = {0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F};

unsigned int counter_var = 0;
unsigned char pressTimes = 0;

void increaseVar(){
    unsigned int max_val;
    switch(pressTimes){
        case 0: max_val = 10; break;
        case 1: max_val = 100; break;
        case 2: max_val = 1000; break;
        default: max_val = 10000; break;
    }
    counter_var = (counter_var + 1) % max_val;
}

int main(){
    init();
    unsigned char prevState = 1; // 1 = not pressed
    unsigned int temp, digit;
    unsigned int cycle;

    while(1){
        unsigned char currState = (LPC_GPIO2->FIOPIN & (1<<0)) ? 1 : 0;

        if(prevState==0 && currState==1){ 
            pressTimes = (pressTimes + 1) % 4; 
        }
        prevState = currState;

        for(cycle=0; cycle<125; cycle++){
            temp = counter_var;
            for(int i=0;i<4;i++){
                digit = temp % 10;
                temp /= 10;

                LPC_GPIO1->FIOCLR = 0x0F << 23;
                LPC_GPIO0->FIOCLR = 0xFF << 4;

                LPC_GPIO0->FIOSET = hexCode[digit] << 4;
                LPC_GPIO1->FIOSET = i << 23; 

                delay(1000);
            }
        }

        increaseVar(); 
    }
}
