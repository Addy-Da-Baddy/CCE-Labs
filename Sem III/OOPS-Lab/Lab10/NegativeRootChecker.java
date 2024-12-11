import java.util.Scanner;

class NegativeIntegerException extends Exception {
    public NegativeIntegerException(String message) {
        super(message);
    }
}

public class NegativeRootChecker {

    public static void checkNegativeInteger(int number) throws NegativeIntegerException {
        if (number >= 0) {
            throw new NegativeIntegerException("The number must be a negative integer. Provided: " + number);
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter an integer: ");
        int number = scanner.nextInt();

        try {
            checkNegativeInteger(number);
            double root = Math.sqrt(-number); 
            System.out.println("The square root of " + number + " is: " + root + "i"); 
        } catch (NegativeIntegerException e) {
            System.err.println(e);
        }

        scanner.close();
    }
}
