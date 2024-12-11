import java.util.*;
class symmetricCheck {
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
        boolean flag = true;
        for (int i = 0; i<r;i++){
            for (int j = i + 1; j<c;j++){
                if (matrix[j][i]!=matrix[i][j]){
                    flag = false;
                    break ;
                }
            }
        }
        if (flag){
            System.out.println("Symmetric Matrix");
        }
        else {
            System.out.println(" Non-Symmetric Matrix");

        }

    }
}
