#include <LPC17xx.h>
#include <stdio.h>

#define RS_CTRL (1 << 27)
#define EN_CTRL (1 << 28)
#define DT_CTRL (0xF << 23)

unsigned long int temp1 = 0, temp2 = 0, i;
unsigned char flag1 = 0;
unsigned char msg[] = "ADC Output:";
unsigned char adc_value_str[16];
volatile unsigned int Result = 0;   // Marked volatile since updated in ISR

void lcd_write(void);
void port_write(void);
void delay_lcd(unsigned int);
void lcd_init(void);
void display_adc_result(void);

unsigned long int init_command[] = {
    0x30, 0x30, 0x30, 0x20, 0x28, 0x0C, 0x06, 0x01, 0x80
};

int main(void)
{
    SystemInit();
    SystemCoreClockUpdate();

    LPC_PINCON->PINSEL1 = 3 << 28;  // P0.28 and P0.29 as ADC4
    LPC_GPIO0->FIODIR |= DT_CTRL | RS_CTRL | EN_CTRL;

    lcd_init();

    LPC_SC->PCONP |= (1 << 12);   // Power up ADC

    LPC_ADC->ADCR = (1 << 4) | (1 << 16) | (1 << 21) | (1 << 24);  // ADC4, ADC enable, burst mode, start now

    LPC_ADC->ADINTEN = (1 << 4);  // Enable interrupt on ADC4

    NVIC_EnableIRQ(ADC_IRQn);

    while (1) {}
}

void ADC_IRQHandler(void)
{
    Result = (LPC_ADC->ADGDR >> 4) & 0xFFF;  // Read 12-bit ADC result
    display_adc_result();
}

void display_adc_result(void)
{
    flag1 = 0;
    temp1 = 0x01;   // Clear display command
    lcd_write();
    delay_lcd(600000);  // Longer delay after clear

    temp1 = 0x80;   // Set cursor to first line, first position
    lcd_write();
    delay_lcd(30000);

    flag1 = 1;  // Data mode

    // Print fixed string "ADC Output:"
    i = 0;
    while (msg[i] != '\0')
    {
        temp1 = msg[i];
        lcd_write();
        i++;
    }

    // Print ADC value immediately after fixed string on same line
    sprintf((char *)adc_value_str, " %4d", Result);  // Added space before value for readability
    i = 0;
    while (adc_value_str[i] != '\0')
    {
        temp1 = adc_value_str[i];
        lcd_write();
        i++;
    }

    delay_lcd(1000000);  // Long delay so user can read output
}

void lcd_init(void)
{
    flag1 = 0;
    delay_lcd(500000);
    for (i = 0; i < 9; i++)
    {
        temp1 = init_command[i];
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
    LPC_GPIO0->FIOCLR = DT_CTRL;
    LPC_GPIO0->FIOSET = temp2 & DT_CTRL;

    if (flag1 == 0)
        LPC_GPIO0->FIOCLR = RS_CTRL;
    else
        LPC_GPIO0->FIOSET = RS_CTRL;

    LPC_GPIO0->FIOSET = EN_CTRL;
    delay_lcd(5000);
    LPC_GPIO0->FIOCLR = EN_CTRL;
    delay_lcd(300000);
}

void delay_lcd(unsigned int r1)
{
    volatile unsigned int r;
    for (r = 0; r < r1; r++);
}
