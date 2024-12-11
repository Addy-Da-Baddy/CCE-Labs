import java.util.*;
class principalDiagonal{
    public static void main(String args[]){
        Scanner sc = new Scanner(System.in);
        int r,c;
        System.out.println("Enter number of rows and columns: ");
        r = sc.nextInt();
        c = sc.nextInt();
        int matrix[][] = new int[r][c];
        System.out.println("Enter the elements of the matrix: ");
        for (int i = 0; i<r;i++){
            for (int j = 0; j<c;j++){
                matrix[i][j] = sc.nextInt();
            }
        }
        int sum = 0;
        for (int i = 0; i<r;i++){
            for (int j = 0; j<c;j++){
                if (i==j){
                    sum = sum + matrix[i][j];
                }
            }
        }

        System.out.println("Sum: " + sum);

    }
}