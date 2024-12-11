#include <stdio.h>
#include <string.h>
struct student{
    char name[50];
    int roll_no;
    int grade;
};

void read (struct student s[],int num){
    for (int i = 0; i<num; i++){
        printf("Enter name, roll number and grade of student %d: ", i+1);
        scanf("%s%d%d",s[i].name,&s[i].roll_no,&s[i].grade);
    }
}

void display (struct student s[], int num){
       for (int i = 0; i<num; i++){
        printf("Student- %d \n", i+1 );
        printf("Name: %s \nRoll number: %d \nGrade: %d \n ", s[i].name,s[i].roll_no,s[i].grade);
       printf("\n\n");
    }
}

void sort (struct student s[], int num){
    for (int i = 0; i<num;i++){
        for (int j = 0; j<num-1-i;j++){
            if (s[j].roll_no>s[j+1].roll_no){
                struct student temp = s[j];
                s[j] = s[j+1];
                s[j+1] = temp;
            }
        }
    }
}

int main(){
    struct student s1[3];
    read(s1,3);
    display(s1,3);
    printf("After Sorting by Roll Number: \n");
    sort(s1,3);
    display(s1,3);
}
