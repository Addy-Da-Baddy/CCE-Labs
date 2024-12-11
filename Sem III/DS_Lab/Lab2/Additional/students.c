#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LEN 100
#define MAX_BRANCH_LEN 50
#define MAX_RECORDS 100

typedef struct {
    char name[MAX_NAME_LEN];
    int roll_no;
    char grade;
    char branch[MAX_BRANCH_LEN];
} Student;

void writeStudentRecords(const char *filename, Student students[], int count) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Failed to open file for writing");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < count; i++) {
        fprintf(file, "%s,%d,%c,%s\n", students[i].name, students[i].roll_no, students[i].grade, students[i].branch);
    }

    fclose(file);
}

void readAndSeparateRecords(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Failed to open file for reading");
        exit(EXIT_FAILURE);
    }

    Student students[MAX_RECORDS];
    int count = 0;

    while (fscanf(file, "%[^,],%d,%c,%[^\n]\n", students[count].name, &students[count].roll_no, &students[count].grade, students[count].branch) == 4) {
        count++;
    }
    fclose(file);

    FILE *branchFiles[MAX_RECORDS];
    char branchFileNames[MAX_RECORDS][MAX_BRANCH_LEN + 10];
    for (int i = 0; i < count; i++) {
        int branchIndex = -1;

        for (int j = 0; j < count; j++) {
            if (branchFiles[j] != NULL && strcmp(branchFileNames[j], students[i].branch) == 0) {
                branchIndex = j;
                break;
            }
        }

        if (branchIndex == -1) {
            snprintf(branchFileNames[count], sizeof(branchFileNames[count]), "%s.txt", students[i].branch);
            branchFiles[count] = fopen(branchFileNames[count], "w");
            if (branchFiles[count] == NULL) {
                perror("Failed to open branch file for writing");
                exit(EXIT_FAILURE);
            }
            branchIndex = count++;
        }

        fprintf(branchFiles[branchIndex], "%s,%d,%c\n", students[i].name, students[i].roll_no, students[i].grade);
    }

    for (int i = 0; i < count; i++) {
        if (branchFiles[i] != NULL) {
            fclose(branchFiles[i]);
        }
    }
}

int main() {
    Student students[] = {
        {"John Doe", 101, 'A', "Computer Science"},
        {"Jane Smith", 102, 'B', "Electrical Engineering"},
        {"Alice Johnson", 103, 'A', "Computer Science"},
        {"Bob Brown", 104, 'C', "Mechanical Engineering"},
        {"Charlie Davis", 105, 'B', "Electrical Engineering"}
    };
    int studentCount = sizeof(students) / sizeof(students[0]);

    const char *filename = "students.txt";
    writeStudentRecords(filename, students, studentCount);
    readAndSeparateRecords(filename);

    printf("Student records have been written and separated by branch.\n");

    return 0;
}
