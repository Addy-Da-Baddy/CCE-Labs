import java.util.Scanner;

public class SortStrings {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] strings = new String[5];

        System.out.println("Enter 5 strings:");
        for (int i = 0; i < 5; i++) {
            strings[i] = scanner.nextLine();
        }

        // Sorting the strings using bubble sort
        for (int i = 0; i < strings.length - 1; i++) {
            for (int j = 0; j < strings.length - 1 - i; j++) {
                if (strings[j].compareTo(strings[j + 1]) > 0) {
                    // Swap
                    String temp = strings[j];
                    strings[j] = strings[j + 1];
                    strings[j + 1] = temp;
                }
            }
        }

        System.out.println("Strings in alphabetical order:");
        for (String str : strings) {
            System.out.println(str);
        }
    }
}
