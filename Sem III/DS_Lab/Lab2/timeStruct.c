#include <stdio.h>
struct Time {
    int hour;
    int minute;
    int second;
};

void readTime(struct Time *t) {
    printf("Enter time (hh mm ss): ");
    scanf("%d %d %d", &t->hour, &t->minute, &t->second);
}

void displayTime(struct Time t) {
    printf("%02d:%02d:%02d\n", t.hour, t.minute, t.second);
}

struct Time addTime(struct Time t1, struct Time t2) {
    struct Time result;
    result.second = (t1.second + t2.second) % 60;
    int carry = (t1.second + t2.second) / 60;

    result.minute = (t1.minute + t2.minute + carry) % 60;
    carry = (t1.minute + t2.minute + carry) / 60;

    result.hour = (t1.hour + t2.hour + carry) % 24;
    return result;
}

struct Time differenceTime(struct Time t1, struct Time t2) {
    struct Time result;

    int totalSeconds1 = t1.hour * 3600 + t1.minute * 60 + t1.second;
    int totalSeconds2 = t2.hour * 3600 + t2.minute * 60 + t2.second;

    int diffSeconds = totalSeconds1 - totalSeconds2;

    if (diffSeconds < 0) {
        diffSeconds = -diffSeconds;
    }


    result.hour = diffSeconds / 3600;
    diffSeconds %= 3600;
    result.minute = diffSeconds / 60;
    result.second = diffSeconds % 60;

    return result;
}

int main() {
    struct Time t1, t2, sum, diff;

    printf("Enter first time:\n");
    readTime(&t1);

    printf("Enter second time:\n");
    readTime(&t2);

    printf("First Time: ");
    displayTime(t1);

    printf("Second Time: ");
    displayTime(t2);

    sum = addTime(t1, t2);
    printf("Sum of times: ");
    displayTime(sum);

    diff = differenceTime(t1, t2);
    printf("Difference of times: ");
    displayTime(diff);

    return 0;
}
