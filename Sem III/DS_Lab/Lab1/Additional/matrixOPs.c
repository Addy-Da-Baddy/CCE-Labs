#include <stdio.h>
#include <stdbool.h>

#define MAX_SIZE 10 // Define a maximum size for the matrices

// Function prototypes
void readMatrix(int matrix[MAX_SIZE][MAX_SIZE], int rows, int cols);
void printMatrix(int matrix[MAX_SIZE][MAX_SIZE], int rows, int cols);
void multiplyMatrices(int A[MAX_SIZE][MAX_SIZE], int B[MAX_SIZE][MAX_SIZE], int C[MAX_SIZE][MAX_SIZE], int A_rows, int A_cols, int B_cols);
void addMatrices(int A[MAX_SIZE][MAX_SIZE], int B[MAX_SIZE][MAX_SIZE], int C[MAX_SIZE][MAX_SIZE], int rows, int cols);
bool isMagicSquare(int matrix[MAX_SIZE][MAX_SIZE], int size);

int main() {
    int A[MAX_SIZE][MAX_SIZE], B[MAX_SIZE][MAX_SIZE], C[MAX_SIZE][MAX_SIZE];
    int rowsA, colsA, rowsB, colsB, size;

    // Matrix A
    printf("Enter the number of rows and columns for matrix A: ");
    scanf("%d %d", &rowsA, &colsA);
    printf("Enter elements of matrix A:\n");
    readMatrix(A, rowsA, colsA);

    // Matrix B
    printf("Enter the number of rows and columns for matrix B: ");
    scanf("%d %d", &rowsB, &colsB);
    if (colsA != rowsB) {
        printf("Error: Number of columns in A must be equal to number of rows in B for multiplication.\n");
        return 1;
    }
    printf("Enter elements of matrix B:\n");
    readMatrix(B, rowsB, colsB);

    // Multiply matrices A and B
    printf("Matrix A:\n");
    printMatrix(A, rowsA, colsA);
    printf("Matrix B:\n");
    printMatrix(B, rowsB, colsB);

    printf("Result of A * B:\n");
    multiplyMatrices(A, B, C, rowsA, colsA, colsB);
    printMatrix(C, rowsA, colsB);

    // Add matrices A and B (assuming they are of the same size)
    if (rowsA == rowsB && colsA == colsB) {
        printf("Matrix A + Matrix B:\n");
        addMatrices(A, B, C, rowsA, colsA);
        printMatrix(C, rowsA, colsA);
    } else {
        printf("Error: Matrix dimensions do not match for addition.\n");
    }

    // Check if a square matrix is a magic square
    printf("Enter the size of the square matrix: ");
    scanf("%d", &size);
    if (size > MAX_SIZE) {
        printf("Size exceeds maximum allowed.\n");
        return 1;
    }

    int squareMatrix[MAX_SIZE][MAX_SIZE];
    printf("Enter elements of the square matrix:\n");
    readMatrix(squareMatrix, size, size);

    if (isMagicSquare(squareMatrix, size)) {
        printf("The matrix is a magic square.\n");
    } else {
        printf("The matrix is not a magic square.\n");
    }

    return 0;
}

// Function to read a matrix
void readMatrix(int matrix[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%d", &matrix[i][j]);
        }
    }
}

// Function to print a matrix
void printMatrix(int matrix[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

// Function to multiply two matrices
void multiplyMatrices(int A[MAX_SIZE][MAX_SIZE], int B[MAX_SIZE][MAX_SIZE], int C[MAX_SIZE][MAX_SIZE], int A_rows, int A_cols, int B_cols) {
    for (int i = 0; i < A_rows; i++) {
        for (int j = 0; j < B_cols; j++) {
            C[i][j] = 0;
            for (int k = 0; k < A_cols; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Function to add two matrices
void addMatrices(int A[MAX_SIZE][MAX_SIZE], int B[MAX_SIZE][MAX_SIZE], int C[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }
}

// Function to check if a square matrix is a magic square
bool isMagicSquare(int matrix[MAX_SIZE][MAX_SIZE], int size) {
    int sumDiagonal1 = 0, sumDiagonal2 = 0;
    int sumRow, sumCol;

    // Calculate the sum of the main diagonal
    for (int i = 0; i < size; i++) {
        sumDiagonal1 += matrix[i][i];
    }

    // Calculate the sum of the anti-diagonal
    for (int i = 0; i < size; i++) {
        sumDiagonal2 += matrix[i][size - i - 1];
    }

    if (sumDiagonal1 != sumDiagonal2) {
        return false;
    }

    // Check sums of each row and column
    for (int i = 0; i < size; i++) {
        sumRow = 0;
        sumCol = 0;
        for (int j = 0; j < size; j++) {
            sumRow += matrix[i][j];
            sumCol += matrix[j][i];
        }
        if (sumRow != sumDiagonal1 || sumCol != sumDiagonal1) {
            return false;
        }
    }

    return true;
}
