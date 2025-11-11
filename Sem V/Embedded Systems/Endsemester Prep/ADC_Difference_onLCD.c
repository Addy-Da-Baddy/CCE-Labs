#include <LPC17xx.h>
#include <stdio.h>

//ADC0.5 = P1.31
//ADC0.4 = P1.30

//LCD code for LPC1768
//LCD Pins are p0.23 to p0.26 for data, p0.27 for RS and p0.28 for EN
//Keypad Rows (P2.10–P2.13) Output
// Cols (P1.23–P1.26) Input 

#define EN_CTRL (1 << 28)
#define RS_CTRL (1 << 27)
#define DATA_CTRL (0xF << 23)

unsigned char lcd_buffer;
unsigned char write_buffer;
unsigned int data_mode = 0;

void delay(unsigned int count){
    for (int i = 0; i < count*count; i++);
}

void LCD_init(){
    unsigned char init_commmand[]= {3,3,3,2,2,0x28,0x0C,0x06,0x01,0x80};
    LPC_GPIO0->FIODIR |= (EN_CTRL | RS_CTRL | DATA_CTRL); // Set LCD pins as output
    data_mode = 0;
    for (int i = 0; i < sizeof(init_commmand); i++){
        write_buffer = init_commmand[i];
        lcd_write();
        delay(50000);
    }
}


void lcd_write(){
    lcd_buffer = (write_buffer >> 4) & 0x0F; // Get higher nibble
    port_write();
    delay(50000);
    lcd_buffer = write_buffer & 0x0F; // Get lower nibble
    port_write();
    delay(50000);
}

void port_write(){
    LPC_GPIO0->FIOPIN = lcd_buffer << 23; // Set data pins
    if (data_mode){
        LPC_GPIO0->FIOSET = RS_CTRL; // RS = 1 for data
    } else {
        LPC_GPIO0->FIOCLR = RS_CTRL; // RS = 0 for command
    }
    LPC_GPIO0->FIOSET = EN_CTRL; // EN = 1
    delay(10000);
    LPC_GPIO0->FIOCLR = EN_CTRL; // EN = 0
    delay(10000);
}

void data_write(unsigned char data){
    data_mode = 1;
    write_buffer = data;
    lcd_write();
}

void ADC_init(){
    LPC_PINCON->PINSEL3 |= (3 << 28);
    LPC_PINCON->PINSEL3 |= (3 << 30);
    LPC_SC->PCONP |= (1 << 12); // Power up ADC
    LPC_ADC->ADCR = (1<<21); // ADC Enable Mode
}

unsigned long ADC_read(unsigned char channel){
    LPC->ADC->ADCR &= ~(0xFF); // Clear channel selection
    LPC->ADC->ADCR |= (1 << channel); // Select given channel
    LPC->ADC->ADCR |= (1 << 24); // Start conversion now

    while ((LPC_ADC->ADGDR >> 31)& 1 == 0); // Wait for DONE bit

    unsigned long result = (LPC_ADC->ADGDR >> 4) & 0xFFF; // Extract 12-bit result

    LPC->ADC->ADCR &= ~(7 << 24); // Stop conversion
    return result;

    
}


int main(){
    ADC_Init();
    unsigned long adc_value4, adc_value5;
    unsigned long diff_value;
    unsigned char buffer[20];
    while (1){
        adc_value4 = ADC_read(4);
        adc_value5 = ADC_read(5);
        diff_value = adc_value5 - adc_value4;
        sprintf((char *)buffer, "%lu", diff_value);
        unsigned char message[] = "Diff:";
        for (int i = 0; i < sizeof(message)/sizeof(message[0]); i++){
            data_write(message[i]);
        }
        for (int i = 0; buffer[i] != '\0'; i++){
            data_write(buffer[i]);
        }
    }
}