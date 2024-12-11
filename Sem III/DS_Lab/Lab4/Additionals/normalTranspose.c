#include <stdio.h>

#define MAX 10

typedef struct {
    int row;
    int col;
    int val;
} Sparse;

void createSparse(Sparse s[], int r, int c, int arr[][MAX]) {
    int cnt = 1;
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            if (arr[i][j] != 0) {
                s[cnt].row = i;
                s[cnt].col = j;
                s[cnt].val = arr[i][j];
                cnt++;
            }
        }
    }
    s[0].row = r;
    s[0].col = c;
    s[0].val = cnt - 1;
}

void printSparse(Sparse s[]) {
    printf("Sparse Matrix:\n");
    for (int i = 0; i <= s[0].val; i++) {
        printf("<%d, %d, %d>\n", s[i].row, s[i].col, s[i].val);
    }
}


void transposeSparse(Sparse s[], Sparse trans[]) {
    int numRows = s[0].row;
    int numCols = s[0].col;
    int numTerms = s[0].val;


    trans[0].row = numCols;
    trans[0].col = numRows;
    trans[0].val = numTerms;

    int k = 1;
    for (int i = 0; i <= numTerms; i++) {
        int row = s[i].row;
        int col = s[i].col;
        int val = s[i].val;
        trans[k].row = col;
        trans[k].col = row;
        trans[k].val = val;
        k++;
    }
}


int main() {
    int arr[MAX][MAX];
    int r, c;

    printf("Enter number of rows and number of columns: ");
    scanf("%d %d", &r, &c);

    printf("Enter the matrix elements:\n");
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            scanf("%d", &arr[i][j]);
        }
    }

    Sparse s[(MAX * MAX) / 2];
    createSparse(s, r, c, arr);

    printf("Original Sparse Matrix:\n");
    printSparse(s);

    Sparse trans[(MAX * MAX) / 2];
    transposeSparse(s, trans);

    printf("Transposed Sparse Matrix:\n");
    printSparse(trans);

    return 0;
}
