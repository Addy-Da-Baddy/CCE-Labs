class EvenNumberException extends Exception {
    public EvenNumberException(String message) {
        super(message);
    }
}

public class EvenNumberChecker {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number: ");
        int number = scanner.nextInt();

        try {
            if (number % 2 == 0) {
                throw new EvenNumberException("The number " + number + " is even.");
            }
            System.out.println("The number " + number + " is odd.");
        } catch (EvenNumberException e) {
            System.err.println(e.getMessage());
        }

        scanner.close();
    }
}
