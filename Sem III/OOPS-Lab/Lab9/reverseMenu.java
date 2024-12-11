

import java.util.*;

class ReverseMenu {
    static String reverseString(String str) {
        StringBuffer strbuff = new StringBuffer(str);
        return strbuff.reverse().toString();
    }

    static String bubbleSortString(String str) {
        char[] strArray = str.toCharArray();
        int n = strArray.length;

        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (Character.toUpperCase(strArray[j])> Character.toUpperCase(strArray[j+1])) {
                    char temp = strArray[j];
                    strArray[j] = strArray[j + 1];
                    strArray[j + 1] = temp;
                }
            }
        }
        return new String(strArray);
    }

    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a string: ");
        String s = sc.nextLine();

        while (true) {
            System.out.println("\nMenu:");
            System.out.println("1. Check if the string is a palindrome");
            System.out.println("2. Write the string in alphabetical order (Bubble Sort)");
            System.out.println("3. Reverse the string");
            System.out.println("4. Concatenate original and reversed string");
            System.out.println("5. Exit");
            System.out.print("Enter your choice (1-5): ");

            int choice = sc.nextInt();
            sc.nextLine(); 
            String reversed = reverseString(s);

            switch (choice) {
                case 1:
                    if (s.equalsIgnoreCase(reversed)) {
                        System.out.println("The string is a palindrome.");
                    } else {
                        System.out.println("The string is not a palindrome.");
                    }
                    break;
                case 2:
                    System.out.println("The string in alphabetical order is: " + bubbleSortString(s));
                    break;
                case 3:
                    System.out.println("Reversed String is: " + reversed);
                    break;
                case 4:
                    StringBuffer concatenated = new StringBuffer(s);
                    concatenated.append(reversed);
                    System.out.println("Concatenated String: " + concatenated.toString());
                    break;
                case 5:
                    System.out.println("Exiting the program.");
                    sc.close();
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }
}
