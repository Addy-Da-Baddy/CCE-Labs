//Find length of a string in C
#include <stdio.h>
int main(){
    int i;
    int MAX = 100;
    char strng[MAX];
    printf("Enter a string: ");
    gets(strng);
    for (i = 0; strng[i]!='\0'; i++ );
    printf ("Length of Entered String is: %d", i);
    return 0;
}
