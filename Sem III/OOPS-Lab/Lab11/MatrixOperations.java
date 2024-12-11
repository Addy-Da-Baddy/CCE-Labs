import java.util.Random;

class Matrix {
    private int[][] matrix;
    private int rows;
    private int cols;

    public Matrix(int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
        this.matrix = new int[rows][cols];
        populateMatrix();
    }

    // Method to populate the matrix with random values
    private void populateMatrix() {
        Random random = new Random();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = random.nextInt(10); // Random values between 0 and 99
            }
        }
    }

    // Display the matrix elements
    public synchronized void displayMatrix() {
        System.out.println("Matrix:");
        for (int[] row : matrix) {
            for (int value : row) {
                System.out.print(value + "\t");
            }
            System.out.println();
        }
    }

    // Display the transpose of the matrix
    public synchronized void displayTranspose() {
        System.out.println("Transpose:");
        for (int j = 0; j < cols; j++) {
            for (int i = 0; i < rows; i++) {
                System.out.print(matrix[i][j] + "\t");
            }
            System.out.println();
        }
    }

    // Find and display the maximum value in the matrix
    public synchronized void displayMaxValue() {
        int max = matrix[0][0];
        for (int[] row : matrix) {
            for (int value : row) {
                if (value > max) {
                    max = value;
                }
            }
        }
        System.out.println("Maximum value in the matrix: " + max);
    }

    // Display the principal diagonal elements
    public synchronized void displayPrincipalDiagonal() {
        System.out.println("Principal Diagonal:");
        for (int i = 0; i < Math.min(rows, cols); i++) {
            System.out.print(matrix[i][i] + "\t");
        }
        System.out.println();
    }

    // Display the non-diagonal elements
    public synchronized void displayNonDiagonalElements() {
        System.out.println("Non-Diagonal Elements:");
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (i != j) {
                    System.out.print(matrix[i][j] + "\t");
                }
            }
        }
        System.out.println();
    }
}

// Thread class to execute different operations on the matrix
class MatrixThread extends Thread {
    private Matrix matrix;
    private String operation;

    public MatrixThread(Matrix matrix, String operation) {
        this.matrix = matrix;
        this.operation = operation;
    }

    @Override
    public void run() {
        switch (operation) {
            case "display":
                matrix.displayMatrix();
                break;
            case "transpose":
                matrix.displayTranspose();
                break;
            case "max":
                matrix.displayMaxValue();
                break;
            case "diagonal":
                matrix.displayPrincipalDiagonal();
                break;
            case "nonDiagonal":
                matrix.displayNonDiagonalElements();
                break;
        }
    }
}

class MatrixOperations {
    public static void main(String[] args) {
        Matrix matrix = new Matrix(3, 3); // Create a 5x5 matrix

        // Create threads for each operation
        MatrixThread t1 = new MatrixThread(matrix, "display");
        MatrixThread t2 = new MatrixThread(matrix, "transpose");
        MatrixThread t3 = new MatrixThread(matrix, "max");
        MatrixThread t4 = new MatrixThread(matrix, "diagonal");
        MatrixThread t5 = new MatrixThread(matrix, "nonDiagonal");

        // Start the threads
        t1.start();
        t2.start();
        t3.start();
        t4.start();
        t5.start();
    }
}
