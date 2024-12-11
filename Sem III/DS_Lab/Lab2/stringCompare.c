#include <stdio.h>
#include <string.h>

int main() {
    int MAX = 100;
    char s1[MAX];
    char s2[MAX];

    printf("Enter the first string: ");
    gets(s1);
    printf("Enter the second string: ");
    gets(s2);

    int i = 0;
    while (s1[i] != '\0' && s2[i] != '\0') {
        if (s1[i] < s2[i]) {
            printf("First string is lexicographically smaller\n");
            return 0;
        } else if (s1[i] > s2[i]) {
            printf("First string is lexicographically larger\n");
            return 0;
        }
        i++;
    }
    if (s1[i] == '\0' && s2[i] != '\0') {
        printf("First string is lexicographically smaller\n");
    } else if (s1[i] != '\0' && s2[i] == '\0') {
        printf("First string is lexicographically larger\n");
    } else {
        printf("The two strings are lexicographically equal\n");
    }

    return 0;
}


