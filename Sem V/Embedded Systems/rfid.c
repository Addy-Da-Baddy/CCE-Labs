#include <LPC17xx.h>
#include <stdio.h>
#include <string.h>

#define RS_CTRL 0x00000100   // P0.8
#define EN_CTRL 0x00000200   // P0.9
#define DT_CTRL 0x000000F0   // P0.4 to P0.7
#define BUZZER_LED (1 << 21) // P0.21 for buzzer (adjust as needed)
#define MODE_BUTTON (1 << 0) // P2.0 button for mode toggle

#define PRESCALE (25000 - 1)

#define MAX_IDS 20
#define ID_LENGTH 4

// Global variables
unsigned int i, j, k, temp, temp1, temp2;
unsigned int flag, flag1, flag2;
unsigned int row, col;
unsigned int mode = 0; // 0 = Check Mode, 1 = Registration Mode
unsigned int debounceCounter = 0;
unsigned int count;
unsigned long int init_command[] = {
	0x30,  // 8 bit
	0x30,  // 8 bit
	0x30,  // 8 bit
	0x20,  // 4 bit
	0x28,  // use 2 lines
	0x0c,  // display ON
	0x06,  // increment cursor
	0x01,  // clear display
	0x80}; // set first line first position


unsigned char registeredIDs[MAX_IDS][ID_LENGTH];
unsigned int registeredCount = 0;

unsigned char inputID[ID_LENGTH + 1]; // For input buffer + null terminator
unsigned int inputIndex = 0;

unsigned char lcdMsg[17]; // For LCD messages (max 16 chars + null)

// Keypad mapping 4x4 keypad: Rows = P2.10 to P2.13, Cols = P1.23 to P1.26
unsigned char keyMap[4][4] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}
};

unsigned int MatrixMap[4][4] = {
    {0, 1, 2, 3},
    {4, 5, 6, 7},
    {8, 9, 10, 11},
    {12, 13, 14, 15}
};

// Function prototypes
void SystemInit(void);
void SystemCoreClockUpdate(void);
void delayMS(unsigned int);
void delay_lcd(unsigned int);
void display_lcd(unsigned char *);
void lcd_write(void);
void port_write(void);
void input_keyboard(void);
void scan(void);
void buzzer_short(void);
void buzzer_long(void);
void clear_inputID(void);
void check_mode_process(void);
void registration_mode_process(void);
void toggle_mode(void);
int is_button_pressed(void);
int id_exists(unsigned char *id);

// Main function
int main(void)
{
    SystemInit();
    SystemCoreClockUpdate();

    // Configure matrix keypad GPIO
    LPC_PINCON->PINSEL3 = 0;           // P1.23 to P1.26 GPIO (columns)
    LPC_PINCON->PINSEL4 = 0;           // P2.10 to P2.13 GPIO (rows)
    LPC_GPIO2->FIODIR |= 0x00003C00;   // P2.10 - P2.13 as output (rows)
    LPC_GPIO1->FIODIR &= ~(0x07800000); // P1.23 - P1.26 as input (columns)

    // Configure mode button P2.0 as input
    LPC_PINCON->PINSEL4 &= ~(0x3 << 0); // P2.0 as GPIO
    LPC_GPIO2->FIODIR &= ~MODE_BUTTON;  // P2.0 input

    // Configure LCD pins as output
    LPC_GPIO0->FIODIR |= DT_CTRL | RS_CTRL | EN_CTRL;

    // Configure buzzer pin as output
    LPC_GPIO0->FIODIR |= BUZZER_LED;

    // Clear registered IDs and input buffer
    for (i = 0; i < MAX_IDS; i++)
    {
        for (j = 0; j < ID_LENGTH; j++)
            registeredIDs[i][j] = 0;
    }
    clear_inputID();

    // Display welcome message
    display_lcd((unsigned char *)"ID System Ready");
    delayMS(2000);

    while (1)
    {
        // Check mode button
        if (is_button_pressed())
        {
            toggle_mode();

            if (mode == 0)
                display_lcd((unsigned char *)"Check Mode     ");
            else
                display_lcd((unsigned char *)"Registration   ");

            delayMS(500); // debounce delay
            clear_inputID();
            delayMS(1000);
        }

        // Prompt to enter ID
        if (mode == 0)
        {
            display_lcd((unsigned char *)"Enter 4-digit ID");
            check_mode_process();
        }
        else
        {
            display_lcd((unsigned char *)"Enter 4-digit ID");
            registration_mode_process();
        }
    }
}

// Check mode logic
void check_mode_process(void)
{
    unsigned int found;
    clear_inputID();

    while (1)
    {
        input_keyboard();

        if (row == 0 && col == 0) // Accept key (mapped to 'A' or first col?)
        {
            if (inputIndex == ID_LENGTH)
            {
                inputID[ID_LENGTH] = '\0';

                found = id_exists(inputID);
                if (found)
                {
                    display_lcd((unsigned char *)"Matched        ");
                    buzzer_short();
                }
                else
                {
                    display_lcd((unsigned char *)"Not Enrolled   ");
                    buzzer_long();
                }
                delayMS(2000);
                clear_inputID();
                break;
            }
        }
        else if (row == 3 && col == 3) // Cancel or back to main (mapped to 'D')
        {
            clear_inputID();
            break;
        }
        else
        {
            // Get key char if valid digit 0-9
            unsigned char c = keyMap[row][col];
            if (c >= '0' && c <= '9')
            {
                if (inputIndex < ID_LENGTH)
                {
                    inputID[inputIndex++] = c;

                    // Display entered digits
                    for (i = 0; i < inputIndex; i++)
                        lcdMsg[i] = inputID[i];
                    for (; i < 16; i++)
                        lcdMsg[i] = ' ';
                    lcdMsg[i] = '\0';

                    display_lcd(lcdMsg);
                }
            }
        }
    }
}

// Registration mode logic
void registration_mode_process(void)
{
    unsigned int found;
    clear_inputID();

    while (1)
    {
        input_keyboard();

        if (row == 0 && col == 0) // Accept key
        {
            if (inputIndex == ID_LENGTH)
            {
                inputID[ID_LENGTH] = '\0';

                found = id_exists(inputID);
                if (found)
                {
                    display_lcd((unsigned char *)"Already Exists ");
                    buzzer_long();
                }
                else
                {
                    if (registeredCount < MAX_IDS)
                    {
                        for (i = 0; i < ID_LENGTH; i++)
                            registeredIDs[registeredCount][i] = inputID[i];
                        registeredCount++;

                        display_lcd((unsigned char *)"Registered     ");
                        buzzer_short();
                    }
                    else
                    {
                        display_lcd((unsigned char *)"Memory Full    ");
                        buzzer_long();
                    }
                }
                delayMS(2000);
                clear_inputID();
                break;
            }
        }
        else if (row == 3 && col == 3) // Cancel / back to main
        {
            clear_inputID();
            break;
        }
        else
        {
            unsigned char c = keyMap[row][col];
            if (c >= '0' && c <= '9')
            {
                if (inputIndex < ID_LENGTH)
                {
                    inputID[inputIndex++] = c;
                    for (i = 0; i < inputIndex; i++)
                        lcdMsg[i] = inputID[i];
                    for (; i < 16; i++)
                        lcdMsg[i] = ' ';
                    lcdMsg[i] = '\0';

                    display_lcd(lcdMsg);
                }
            }
        }
    }
}

// Clear input buffer
void clear_inputID(void)
{
    for (i = 0; i < ID_LENGTH + 1; i++)
        inputID[i] = 0;
    inputIndex = 0;
}

// Check if ID exists in registered list, returns 1 if found else 0
int id_exists(unsigned char *id)
{
    for (i = 0; i < registeredCount; i++)
    {
        int match = 1;
        for (j = 0; j < ID_LENGTH; j++)
        {
            if (registeredIDs[i][j] != id[j])
            {
                match = 0;
                break;
            }
        }
        if (match)
            return 1;
    }
    return 0;
}

// Toggle mode
void toggle_mode(void)
{
    if (mode == 0)
        mode = 1;
    else
        mode = 0;
}

// Check if mode button pressed with debounce
int is_button_pressed(void)
{
    unsigned int stable = 0;
    unsigned int pressed = 0;

    for (i = 0; i < 20; i++) // sample 20 times
    {
        if ((LPC_GPIO2->FIOPIN & MODE_BUTTON) == 0) // button active low assumed
            pressed++;
        delayMS(10);
    }
    if (pressed > 15)
        stable = 1;
    return stable;
}

// Keypad input scanning - waits for key press and sets row and col globals
void input_keyboard(void)
{
    int Break_flag = 0;
    row = 0;
    col = 0;

    while (1)
    {
        for (row = 0; row < 4; row++)
        {
            if (row == 0)
                temp = 1 << 10;
            else if (row == 1)
                temp = 1 << 11;
            else if (row == 2)
                temp = 1 << 12;
            else if (row == 3)
                temp = 1 << 13;

            LPC_GPIO2->FIOPIN = temp;
            flag = 0;
            delayMS(10);
            scan();
            if (flag == 1)
            {
                Break_flag = 1;
                delayMS(100); // debounce delay on key press
                break;
            }
        }
        if (Break_flag == 1)
            break;
    }
}

// Scan columns for key press and set col variable
void scan(void)
{
    unsigned long temp3;

    temp3 = LPC_GPIO1->FIOPIN;
    temp3 &= 0x07800000; // mask P1.23 to P1.26

    if (temp3 != 0)
    {
        flag = 1;
        if (temp3 == (1 << 23))
            col = 0;
        else if (temp3 == (1 << 24))
            col = 1;
        else if (temp3 == (1 << 25))
            col = 2;
        else if (temp3 == (1 << 26))
            col = 3;
    }
}

// LCD Functions
void display_lcd(unsigned char msg[])
{
    flag1 = 0; // command mode
    for (count = 0; count < 9; count++)
    {
        temp1 = init_command[count];
        lcd_write();
    }
    flag1 = 1; // data mode

    i = 0;
    while (msg[i] != '\0' && i < 16)
    {
        temp1 = msg[i];
        lcd_write();
        i++;
    }
}



void lcd_write(void)
{
    flag2 = (flag1 == 1) ? 0 : ((temp1 == 0x30) || (temp1 == 0x20)) ? 1 : 0;
    temp2 = temp1 & 0xF0;
    port_write();

    if (flag2 == 0)
    {
        temp2 = (temp1 & 0x0F) << 4;
        port_write();
    }
}

void port_write(void)
{
    LPC_GPIO0->FIOCLR = DT_CTRL | RS_CTRL | EN_CTRL; // Clear pins first
    LPC_GPIO0->FIOPIN |= temp2;

    if (flag1 == 0)
        LPC_GPIO0->FIOCLR = RS_CTRL;
    else
        LPC_GPIO0->FIOSET = RS_CTRL;

    LPC_GPIO0->FIOSET = EN_CTRL;
    delay_lcd(25);
    LPC_GPIO0->FIOCLR = EN_CTRL;
    delay_lcd(300000);
}

void delay_lcd(unsigned int r1)
{
    unsigned int r;
    for (r = 0; r < r1; r++)
        ;
    return;
}

// Buzzer short beep (success)
void buzzer_short(void)
{
    LPC_GPIO0->FIOSET = BUZZER_LED;
    delayMS(200);
    LPC_GPIO0->FIOCLR = BUZZER_LED;
}

// Buzzer long beep (error)
void buzzer_long(void)
{
    LPC_GPIO0->FIOSET = BUZZER_LED;
    delayMS(800);
    LPC_GPIO0->FIOCLR = BUZZER_LED;
}

// Timer delay in ms
void delayMS(unsigned int milliseconds)
{
    unsigned int t;
    for (t = 0; t < milliseconds; t++)
    {
        unsigned int u;
        for (u = 0; u < 3000; u++)
            ; // approx 1ms delay at ~48 MHz (adjust if needed)
    }
}
