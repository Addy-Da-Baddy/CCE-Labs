#include <LPC17xx.h>
#include <stdio.h>

#define RS (1 << 27)
#define EN (1 << 28)
#define DT (0xF << 23)

char keys[4][4] = {
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}
};

unsigned long int temp1 = 0, temp2 = 0;
unsigned char flag1 = 0;
char key;

void lcd_init(void);
void lcd_write(void);
void port_write(void);
void delay_lcd(unsigned int);
void lcd_display_char(char);
char scan_keypad(void);

int main(void)
{
    SystemInit();
    SystemCoreClockUpdate();

    LPC_GPIO0->FIODIR |= DT | RS | EN;  // LCD pins as output
    LPC_GPIO1->FIODIR |= 0x07800000;    // P1.23–P1.26 as output (rows)
    LPC_GPIO1->FIODIR &= ~(0x00780000); // P1.19–P1.22 as input (columns)

    lcd_init();

    while (1)
    {
        key = scan_keypad();
        if (key != 0)
        {
            lcd_display_char(key);
            delay_lcd(1000000);  // Delay to allow user to see character
        }
    }
}

char scan_keypad(void)
{
    int row, col;
    for (row = 0; row < 4; row++)
    {
        LPC_GPIO1->FIOCLR = 0x07800000;  // Clear all rows
        LPC_GPIO1->FIOSET = (1 << (23 + row));  // Set one row high

        for (col = 0; col < 4; col++)
        {
            if (LPC_GPIO1->FIOPIN & (1 << (19 + col)))
            {
                while (LPC_GPIO1->FIOPIN & (1 << (19 + col)));  // Wait for release
                return keys[row][col];
            }
        }
    }
    return 0;
}

void lcd_display_char(char ch)
{
    flag1 = 0;
    temp1 = 0x01;  // Clear display
    lcd_write();
    delay_lcd(600000);

    temp1 = 0x80;  // Cursor to first line
    lcd_write();
    delay_lcd(30000);

    flag1 = 1;
    temp1 = ch;
    lcd_write();
}

void lcd_init(void)
{
    unsigned char init_cmd[] = {0x30, 0x30, 0x30, 0x20, 0x28, 0x0C, 0x06, 0x01, 0x80};
    flag1 = 0;
    delay_lcd(500000);
    for (int i = 0; i < 9; i++)
    {
        temp1 = init_cmd[i];
        lcd_write();
        delay_lcd(50000);
    }
}

void lcd_write(void)
{
    temp2 = ((temp1 >> 4) & 0x0F) << 23;
    port_write();
    temp2 = (temp1 & 0x0F) << 23;
    port_write();
}

void port_write(void)
{
    LPC_GPIO0->FIOCLR = DT;
    LPC_GPIO0->FIOSET = temp2 & DT;

    if (flag1 == 0)
        LPC_GPIO0->FIOCLR = RS;
    else
        LPC_GPIO0->FIOSET = RS;

    LPC_GPIO0->FIOSET = EN;
    delay_lcd(5000);
    LPC_GPIO0->FIOCLR = EN;
    delay_lcd(300000);
}

void delay_lcd(unsigned int r1)
{
    for (volatile unsigned int r = 0; r < r1; r++);
}
