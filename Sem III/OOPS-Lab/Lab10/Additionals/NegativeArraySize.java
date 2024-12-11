import java.util.Scanner;

public class NegativeArraySize {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the size of the array: ");
        int size = scanner.nextInt();

        try {
            if (size < 0) {
                throw new NegativeArraySizeException("Array size cannot be negative.");
            }
            int[] array = new int[size]; // Create the array
            System.out.println("Array of size " + size + " created successfully.");
        } catch (NegativeArraySizeException e) {
            System.err.println(e.getMessage());
        }

        scanner.close();
    }
}
