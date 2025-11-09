#include "LPC17xx.h"
#include <stdio.h>
#include <stdint.h>

/* -------- LCD Globals -------- */
int temp1, temp2, flag_command;
int i, r;

/* -------- Pin Configuration --------
   LCD D4–D7 → P0.23–P0.26
   RS → P0.27
   EN → P0.28
   Keypad Rows → P2.10–P2.13 (Outputs)
   Keypad Cols → P1.23–P1.26 (Inputs)
------------------------------------ */

unsigned char keypad_map[4][4] = {
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}
};

/* -------- Function Prototypes -------- */
void delay(int);
void lcd_init(void);
void lcd_cmd(unsigned char);
void lcd_data(unsigned char);
void lcd_string(unsigned char *);
void lcd_clear(void);
void port_wr(void);
void lcd_wr(void);
char get_key(void);

/* -------- LCD Implementation -------- */
void port_wr(void)
{
    int jj;
    LPC_GPIO0->FIOPIN = temp2 << 23;
    if (flag_command == 0)
        LPC_GPIO0->FIOCLR = 1 << 27;   // RS = 0 for command
    else
        LPC_GPIO0->FIOSET = 1 << 27;   // RS = 1 for data

    LPC_GPIO0->FIOSET = 1 << 28;       // EN = 1
    for (jj = 0; jj < 50; jj++);
    LPC_GPIO0->FIOCLR = 1 << 28;       // EN = 0
    for (jj = 0; jj < 10000; jj++);
}

void lcd_wr(void)
{
    temp2 = (temp1 >> 4) & 0xF;
    port_wr();
    temp2 = temp1 & 0xF;
    port_wr();
}

void delay(int r1)
{
    for (r = 0; r < r1; r++);
}

void lcd_cmd(unsigned char cmd)
{
    flag_command = 0;
    temp1 = cmd;
    lcd_wr();
    delay(30000);
}

void lcd_data(unsigned char data)
{
    flag_command = 1;
    temp1 = data;
    lcd_wr();
    delay(30000);
}

void lcd_string(unsigned char *str)
{
    i = 0;
    while (str[i] != '\0') {
        lcd_data(str[i]);
        i++;
    }
}

void lcd_clear(void)
{
    lcd_cmd(0x01);
    delay(50000);
}

void lcd_init(void)
{
    int ii;
    int command_init[9] = {3,3,3,2,2,0x28,0x0C,0x06,0x01};
    flag_command = 0;
    for (ii = 0; ii < 9; ii++) {
        temp1 = command_init[ii];
        lcd_wr();
        delay(30000);
    }
}

/* -------- Keypad Scanning -------- */
char get_key(void)
{
    unsigned long col_data;
    int row, col;

    while (1) {
        for (row = 0; row < 4; row++) {
            LPC_GPIO2->FIOPIN = (1 << (10 + row)); // Activate one row
            delay(1000);

            col_data = (LPC_GPIO1->FIOPIN >> 23) & 0x0F; // Read P1.23–P1.26
            if (col_data) {
                for (col = 0; col < 4; col++) {
                    if (col_data & (1 << col)) {
                        // Wait for release
                        while (((LPC_GPIO1->FIOPIN >> 23) & 0x0F) != 0);
                        delay(50000);
                        return keypad_map[row][col];
                    }
                }
            }
        }
    }
}

/* -------- Main -------- */
int main(void)
{
    char key;

    SystemInit();

    /* LCD Pins as Output */
    LPC_GPIO0->FIODIR |= (0xF << 23) | (1 << 27) | (1 << 28);

    /* Keypad Rows (P2.10–P2.13) Output, Cols (P1.23–P1.26) Input */
    LPC_GPIO2->FIODIR |= (0xF << 10);   // Rows output
    LPC_GPIO1->FIODIR &= ~(0xF << 23);  // Cols input

    lcd_init();
    lcd_clear();
    lcd_string("4x4 Keypad Test");

    while (1) {
        lcd_cmd(0xC0);
        lcd_string("Press Key...");
        key = get_key();
        lcd_clear();
        lcd_string("You Pressed:");
        lcd_cmd(0xC0);
        lcd_data(key);
        delay(2000000);
        lcd_clear();
    }
}
