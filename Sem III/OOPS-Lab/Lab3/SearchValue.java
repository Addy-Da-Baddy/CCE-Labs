import java.util.Scanner;


public class SearchValue {
    public static void main(String[] args) {
		
		int[] a = {1,2,3,1,2,1,5,6,7};
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Enter the value to search: ");
        int searchValue = scanner.nextInt();
        int indx = 0;
        System.out.println("The value has been found in locations: ");
        for (int i:a){
            if (i==searchValue){
                System.out.print("a["+indx+"] ");
            }
            indx++;
        }

        
    }
}
