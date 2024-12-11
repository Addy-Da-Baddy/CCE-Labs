#include <stdio.h>
#define MAX 100

typedef struct Sparse {
    int row;
    int col;
    int val;
} Sparse;

// Function to create the sparse matrix representation
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
    s[0].row = r;  // Store number of rows
    s[0].col = c;  // Store number of columns
    s[0].val = cnt - 1;  // Store the count of non-zero elements
}

// Function to print the sparse matrix
void printSparse(Sparse s[]) {
    printf("First Entry is only info about Sparse Matrix \n");
    printf("<Row, Col, Val>\n");
    for (int i = 0; i <= s[0].val; i++) {
        printf("<%d, %d, %d>\n", s[i].row, s[i].col, s[i].val);
    }
}

// Slow transpose of sparse matrix (not optimal for large matrices)
void slowTranspose(Sparse s[], Sparse trans[]) {
    int cnt = 1;
    for (int i = 0; i < s[0].col; i++) {
        for (int j = 0; j <= s[0].val; j++) {
            if (s[j].col == i) {
                trans[cnt].row = s[j].col;
                trans[cnt].col = s[j].row;
                trans[cnt].val = s[j].val;
                cnt++;
            }
        }
    }
}

// Fast transpose of sparse matrix (optimized)
void fastTranspose(Sparse a[], Sparse b[]) {
    int row_terms[MAX], starting_pos[MAX];
    int num_cols = a[0].col;
    int num_terms = a[0].val;

    // Set b[0] as metadata (rows, cols, non-zero count)
    b[0].row = num_cols;   // Transposed matrix has rows equal to original's columns
    b[0].col = a[0].row;   // Transposed matrix has columns equal to original's rows
    b[0].val = num_terms;  // Number of non-zero elements remains the same

    if (num_terms > 0) {
        // Step 1: Initialize row_terms array to count occurrences of each column
        for (int i = 0; i < num_cols; i++) {
            row_terms[i] = 0;
        }
        for (int i = 1; i <= num_terms; i++) {
            row_terms[a[i].col]++;
        }

        // Step 2: Calculate starting positions for each column in the transposed matrix
        starting_pos[0] = 1;
        for (int i = 1; i < num_cols; i++) {
            starting_pos[i] = starting_pos[i - 1] + row_terms[i - 1];
        }

        // Step 3: Transpose elements from a[] to b[]
        for (int i = 1; i <= num_terms; i++) {
            int j = starting_pos[a[i].col]++;  // Get and increment the starting position
            b[j].row = a[i].col;               // Swap row and column
            b[j].col = a[i].row;
            b[j].val = a[i].val;               // Keep the value the same
        }
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

    Sparse s[(MAX*MAX)/2];  // Allocate space for sparse matrix
    createSparse(s, r, c, arr);
    
    printf("Original Sparse Matrix:\n");
    printSparse(s);

    Sparse trans[(MAX*MAX)/2];  // Allocate space for transposed matrix
    trans[0].row = c;           // Rows and columns are swapped in the transpose
    trans[0].col = r;
    trans[0].val = s[0].val;     // The number of non-zero values remains the same

    // Call fastTranspose function
    fastTranspose(s, trans);

    printf("Transposed Sparse Matrix (Fast Transpose):\n");
    printSparse(trans);

    return 0;
}



