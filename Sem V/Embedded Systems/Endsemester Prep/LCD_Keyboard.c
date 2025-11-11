//LCD code for LPC1768
//LCD Pins are p0.23 to p0.26 for data, p0.27 for RS and p0.28 for EN
//Keypad Rows (P2.10–P2.13) Output
// Cols (P1.23–P1.26) Input 

#include <LPC17xx.h>
#include <stdio.h>

#define EN_CTRL (1 << 28)
#define RS_CTRL (1 << 27)
#define DATA_CTRL (0xF << 23)

unsigned char lcd_buffer;
unsigned char write_buffer;
unsigned char init_command[] = {3,3,3,2,2,0x28,0x0C,0x06,0x01};
unsigned int command_mode = 0;
unsigned char keymap[4][4] = {
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}
};
unsigned char key_buffer;
void lcd_init(){
    LPC_GPIO0->FIODIR |= (EN_CTRL | RS_CTRL | DATA_CTRL); // Set LCD pins as output
    for (int i = 0; i < sizeof(init_command); i++){
        command_mode = 1;
        write_buffer = init_command[i];
        lcd_write();
        delay(50000);
    }2
}

void keyboard_init(){
    LPC_GPIO2->FIODIR |= (0x0F << 10); // Set rows as output
    LPC_GPIO1->FIODIR &= ~(0x0F << 23); // Set cols as input
}

void key_detect(void) {
    unsigned long col_data;

    // Clear all rows before starting scan
    LPC_GPIO2->FIOCLR = (0x0F << 10);

    for (int row = 0; row < 4; row++) {
        // Activate only the current row
        LPC_GPIO2->FIOSET = (1 << (10 + row));
        delay(1000); // brief settle time

        // Read the column inputs (P1.23–P1.26)
        col_data = (LPC_GPIO1->FIOPIN >> 23) & 0x0F;

        if (col_data) {
            for (int col = 0; col < 4; col++) {
                if (col_data & (1 << col)) {
                    // Debounce delay
                    delay(5000);

                    // Wait until key is released
                    while (((LPC_GPIO1->FIOPIN >> 23) & 0x0F) != 0);

                    // Store key once per press
                    key_buffer = keymap[row][col];

                    // Deactivate the row before returning
                    LPC_GPIO2->FIOCLR = (1 << (10 + row));
                    return;
                }
            }
        }

        // Deactivate the current row before scanning the next
        LPC_GPIO2->FIOCLR = (1 << (10 + row));
    }
}


void data_write(unsigned char data){
    command_mode = 0;
    write_buffer = data;
    lcd_write();
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

    if (command_mode){
        LPC_GPIO0->FIOCLR = RS_CTRL; // RS = 0 for command
    } else {
        LPC_GPIO0->FIOSET = RS_CTRL; // RS = 1 for data
    }
    LPC_GPIO0->FIOSET = EN_CTRL; // EN = 1
    delay(10000);
    LPC_GPIO0->FIOCLR = EN_CTRL; // EN = 0
    delay(10000);

}


void delay(unsigned int count){
    for (int i = 0; i < count; i++);
}




int main(){
    LPC_PINCON->PINSEL0 = 0;
    LPC_PINCON->PINSEL1 = 0;
    LPC_PINCON->PINSEL2 = 0;
    LPC_PINCON->PINSEL3 = 0;
    keyboard_init();
    lcd_init();
    unsigned char message[] = "Keyboard Ready!";
    for (int i = 0; i < sizeof(message)-1; i++){
        data_write(message[i]);
    }
    delay(1000000);
    while (1){
        key_detect();
        if (key_buffer != 0){
            data_write(key_buffer);
            key_buffer = 0;
        }
    }
}


