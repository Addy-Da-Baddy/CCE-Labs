import java.util.Scanner;

public class ConcatenateStrings {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the number of strings to concatenate: ");
        int n = scanner.nextInt();
        scanner.nextLine();  // Consume newline

        String[] strings = new String[n];

        System.out.println("Enter " + n + " strings:");
        for (int i = 0; i < n; i++) {
            strings[i] = scanner.nextLine();
        }

        String concatenatedString = "";
        for (String str : strings) {
            concatenatedString += str;
        }

        System.out.println("Concatenated string: " + concatenatedString);
    }
}
