#include <stdio.h>
int main(){
    char str[100];
    printf("Enter String ");
    gets(str);
    printf ("enter position to delete and also length: ");
    int p,l;
    scanf("%d%d",&p,&l);
    int indx = p - 1;
    int delLen = 0;
    for (int i = 0; str[i]!='\0';i++){
        if (i>=indx && i<indx+l){
            continue;
        }
        else{
            str[delLen++] = str[i];
        }
    }
    str[delLen] = '\0';
    puts (str);
}
