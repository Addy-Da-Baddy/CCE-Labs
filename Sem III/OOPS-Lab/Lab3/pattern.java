import java.util.*;
class pattern{
    public static void main(String args[]){
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter your choice. Press 1 for nested loop and Press 2 for for-each: ");
        int ch = sc.nextInt();
        System.out.println("Enter number of lines: ");
        int n = sc.nextInt();
        switch(ch){
            case 1:
                System.out.println("Using nested for loop: ");
                for (int i = 1; i<=n; i++){
                    for (int j = 1; j<=i; j++){
                        System.out.print(i + " ");
                    }
                    System.out.println();
                }
                break;
            case 2:
                System.out.println("Using for-each loop: ");
                int[][] elements=new int[n][n];
                for (int i = 0; i<n;i++){
                    for (int j = 0; j<=i;j++){
                        elements[i][j] = i + 1;
                    }
                }
                for (int[] i:elements){
                    for(int j:i){
                        if (j!=0)
                        System.out.print(j + " ");
                    }
                System.out.println();
                }
                break;

            default:
            System.out.println("Invalid Choice");
        }

    }
}