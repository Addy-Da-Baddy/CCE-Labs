import java.util.Scanner;

class NonSquareMatrixException extends Exception {
    public NonSquareMatrixException(String message) {
        super(message);
    }
}

public class MatrixValidator {

    public static void validateSquareMatrix(int n, int m) throws NonSquareMatrixException {
        if (n != m) {
            throw new NonSquareMatrixException("Matrix is not square. Rows: " + n + ", Columns: " + m);
        }
        System.out.println("Matrix is a valid square matrix.");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the number of rows (n): ");
        int n = scanner.nextInt();
        
        System.out.print("Enter the number of columns (m): ");
        int m = scanner.nextInt();

        try {
            validateSquareMatrix(n, m);
            int[][] matrix = new int[n][m];

            System.out.println("Enter the elements of the matrix:");
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    matrix[i][j] = scanner.nextInt();
                }
            }
        } catch (NonSquareMatrixException e) {
            System.err.println(e);
        }

        scanner.close();
    }
}
