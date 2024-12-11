import java.util.Scanner;
class MagicSquareCheck {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Enter the size of the matrix (n x n): ");
        int size = scanner.nextInt();
        
        int[][] matrix = new int[size][size];
        
        System.out.println("Enter the elements of the matrix:");
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                matrix[i][j] = scanner.nextInt();
            }
        }
        
        int sum = 0;
        
        for (int j = 0; j < size; j++) {
            sum += matrix[0][j];
        }
        
        boolean isMagicSquare = true;
        
        for (int i = 0; i < size; i++) {
            int rowSum = 0;
            for (int j = 0; j < size; j++) {
                rowSum += matrix[i][j];
            }
            if (rowSum != sum) {
                isMagicSquare = false;
                break;
            }
        }
        
        if (isMagicSquare) {
            for (int j = 0; j < size; j++) {
                int colSum = 0;
                for (int i = 0; i < size; i++) {
                    colSum += matrix[i][j];
                }
                if (colSum != sum) {
                    isMagicSquare = false;
                    break;
                }
            }
        }
        
        if (isMagicSquare) {
            int principalDiagonalSum = 0;
            for (int i = 0; i < size; i++) {
                principalDiagonalSum += matrix[i][i];
            }
            if (principalDiagonalSum != sum) {
                isMagicSquare = false;
            }
        }
        
        if (isMagicSquare) {
            int secondaryDiagonalSum = 0;
            for (int i = 0; i < size; i++) {
                secondaryDiagonalSum += matrix[i][size - 1 - i];
            }
            if (secondaryDiagonalSum != sum) {
                isMagicSquare = false;
            }
        }
        
        if (isMagicSquare) {
            System.out.println("The matrix is a magic square.");
        } else {
            System.out.println("The matrix is not a magic square.");
        }
        
        scanner.close();
    }
}
