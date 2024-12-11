import java.util.Scanner;

public class LargestSmallest {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        System.out.println("Enter the first number:");
        int a = sc.nextInt();
        
        System.out.println("Enter the second number:");
        int b = sc.nextInt();
        
        System.out.println("Enter the third number:");
        int c = sc.nextInt();
        
        // Finding the largest number using ternary operator
        int largest = (a > b) ? (a > c ? a : c) : (b > c ? b : c);
        
        // Finding the smallest number using ternary operator
        int smallest = (a < b) ? (a < c ? a : c) : (b < c ? b : c);
        
        System.out.println("The largest number is: " + largest);
        System.out.println("The smallest number is: " + smallest);
    }
}
