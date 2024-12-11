#include <stdio.h>
#include <string.h>

int main() {
    char strng[100];
    char subs[50];
    int pos;

    printf("Enter the main string: ");
    gets(strng);

    printf("Enter the substring: ");
    gets(subs);

    printf("Enter the position to insert the substring: ");
    scanf("%d", &pos);

    int strlen = 0, sublen = 0;

    for (int i = 0; strng[i] != '\0'; i++) {
        strlen++;
    }

    for (int i = 0; subs[i] != '\0'; i++) {
        sublen++;
    }

    if (pos < 1 || pos > strlen + 1) {
        printf("Invalid position!\n");
        return 1;
    }

    int index = pos - 1;

    for (int i = strlen - 1; i >= index; i--) {
        strng[i + sublen] = strng[i];
    }

    for (int j = 0; j < sublen; j++) {
        strng[j + index] = subs[j];
    }

    strng[strlen + sublen] = '\0';

    printf("Resulting string: %s\n", strng);

    return 0;
}
