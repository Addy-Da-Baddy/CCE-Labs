import java.util.Scanner;

class InputException extends Exception {
    public InputException(String message) {
        super(message);
    }
}

public class InputValidator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int sum = 0;

        while (true) {
            System.out.print("Enter a number (-1 to exit): ");
            String input = scanner.nextLine();

            try {
                int number = Integer.parseInt(input);
                if (number == -1) {
                    break;
                }
                sum += number;
            } catch (NumberFormatException e) {
                try {
                    throw new InputException("Invalid input: Please enter an integer.");
                } catch (InputException ex) {
                    System.err.println(ex.getMessage());
                }
            }
        }

        System.out.println("Sum of entered numbers: " + sum);
        scanner.close();
    }
}
