import java.util.Scanner;

class SumAndProd {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter number of rows and columns of matrix 1: ");
        int r1 = sc.nextInt();
        int c1 = sc.nextInt();
        int[][] matrix1 = new int[r1][c1];

        System.out.println("Enter the elements of matrix 1: ");
        for (int i = 0; i < r1; i++) {
            for (int j = 0; j < c1; j++) {
                matrix1[i][j] = sc.nextInt();
            }
        }

        System.out.println("Enter number of rows and columns of matrix 2: ");
        int r2 = sc.nextInt();
        int c2 = sc.nextInt();
        int[][] matrix2 = new int[r2][c2];

        System.out.println("Enter the elements of matrix 2: ");
        for (int i = 0; i < r2; i++) {
            for (int j = 0; j < c2; j++) {
                matrix2[i][j] = sc.nextInt();
            }
        }

        // Check if matrices can be added or multiplied
        boolean canAdd = (r1 == r2 && c1 == c2);
        boolean canMultiply = (c1 == r2);

        if (canAdd) {
            int[][] sum = new int[r1][c1];
            for (int i = 0; i < r1; i++) {
                for (int j = 0; j < c1; j++) {
                    sum[i][j] = matrix1[i][j] + matrix2[i][j];
                }
            }

            System.out.println("Sum of matrices:");
            printMatrix(sum);
        } 

        else {
            System.out.println("Cannot be added");
        }
        if (canMultiply) {
            int[][] product = new int[r1][c2];
            for (int i = 0; i < r1; i++) {
                for (int j = 0; j < c2; j++) {
                    product[i][j] = 0;
                    for (int k = 0; k < c1; k++) {
                        product[i][j] += matrix1[i][k] * matrix2[k][j];
                    }
                }
            }

            System.out.println("Product of matrices:");
            printMatrix(product);

        } 
        
        else {
            System.out.println("Matrices cannot be multiplied");
        }

    }

    public static void printMatrix(int[][] matrix) {
        for (int[] row : matrix) {
            for (int element : row) {
                System.out.print(element + " ");
            }
            System.out.println();
        }
    }
}
