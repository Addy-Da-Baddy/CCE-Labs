import java.util.Scanner;

public class numberFormatException {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Please enter a number (integer or decimal): ");
        String input = sc.nextLine();
        
        try {
            int intValue = Integer.parseInt(input);
            System.out.println("You entered a valid integer: " + intValue);
        } catch (NumberFormatException e1) {
            try {
                double doubleValue = Double.parseDouble(input);
                System.out.println("You entered a valid decimal number: " + doubleValue);
            } catch (NumberFormatException e2) {
                System.out.println("Invalid input! Please enter a valid number.");
            }
    }
    sc.close();
}
}
