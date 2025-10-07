#include <LPC17xx.h>
#include <stdlib.h>    // for rand()

#define RS_CTRL (1 << 27)   // P0.27
#define EN_CTRL (1 << 28)   // P0.28
#define DT_CTRL (0xF << 23) // P0.23 - P0.26

unsigned long int temp1 = 0, temp2 = 0, i;
unsigned char flag1 = 0, flag2 = 0;
unsigned char msg[] = {"DIE FACE:"};

void lcd_write(void);
void port_write(void);
void delay_lcd(unsigned int);

unsigned long int init_command[] = {
    0x30, 0x30, 0x30, 0x20, 0x28, 0x0C, 0x06, 0x01, 0x80
};

int main(void)
{
    SystemInit();
    SystemCoreClockUpdate();

    LPC_GPIO0->FIODIR = DT_CTRL | RS_CTRL | EN_CTRL; // LCD pins as output
    LPC_GPIO0->FIODIR &= ~(1 << 4);                  // P0.4 as input (switch)

    flag1 = 0;  // command mode
    for(i = 0; i < 9; i++)
    {
        temp1 = init_command[i];
        lcd_write();
    }

    unsigned int prev_state = 1; // assume not pressed initially
    unsigned int curr_state;
    unsigned int face;

    while(1)
    {
        curr_state = (LPC_GPIO0->FIOPIN & (1 << 4)) ? 1 : 0; // read switch

        if(prev_state == 1 && curr_state == 0) // falling edge detected
        {
            // generate random face (1–6)
            face = (rand() % 6) + 1;

            // clear display
            flag1 = 0;
            temp1 = 0x01;
            lcd_write();

            // move to first line
            temp1 = 0x80;
            lcd_write();

            // write "DIE FACE:"
            flag1 = 1;
            i = 0;
            while(msg[i] != '\0')
            {
                temp1 = msg[i];
                lcd_write();
                i++;
            }

            // move to second line
            flag1 = 0;
            temp1 = 0xC0;
            lcd_write();

            // display the random face
            flag1 = 1;
            temp1 = face + '0';  // convert number → ASCII character
            lcd_write();
        }

        prev_state = curr_state; // update switch state
    }
}

// Send data/command to LCD
void lcd_write(void)
{
    flag2 = (flag1 == 1) ? 0 : ((temp1 == 0x30) || (temp1 == 0x20)) ? 1 : 0;

    // Send higher nibble
    temp2 = temp1 & 0xF0;
    temp2 = temp2 << 19;  // align with P0.23–P0.26
    port_write();

    if(flag2 == 0)
    {
        // Send lower nibble
        temp2 = temp1 & 0x0F;
        temp2 = temp2 << 23;
        port_write();
    }
}

// Helper to write to LCD via GPIO
void port_write(void)
{
    LPC_GPIO0->FIOCLR = DT_CTRL;   // clear data lines
    LPC_GPIO0->FIOSET = temp2;     // set required data bits

    if(flag1 == 0)
        LPC_GPIO0->FIOCLR = RS_CTRL;  // command
    else
        LPC_GPIO0->FIOSET = RS_CTRL;  // data

    LPC_GPIO0->FIOSET = EN_CTRL;      // enable pulse
    delay_lcd(5000);
    LPC_GPIO0->FIOCLR = EN_CTRL;
    delay_lcd(300000);
}

// Simple software delay
void delay_lcd(unsigned int r1)
{
    unsigned long r;
    for(r = 0; r < r1; r++);
}
