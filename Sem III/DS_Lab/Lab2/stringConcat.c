//Concatenate 2 strings
#include <stdio.h>
int main(){
    int MAX = 100;
    char s1[2*MAX];
    char s2[MAX];
    int ls1,ls2,i;
    printf("Enter the first string: ");
    gets(s1);
    printf("Enter the second string: ");
    gets(s2);
    for (i = 0; s1[i]!='\0'; i++);
    ls1 = i;
    ls2 = 0;
    for (i = ls1; s2[ls2]!='\0'; i++){
        s1[i] = s2[ls2++];
    }
    s1[i] = '\0';
    printf("Concatenated String: ");
    puts(s1);
}
