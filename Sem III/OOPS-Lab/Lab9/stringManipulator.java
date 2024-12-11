import java.util.Scanner;

class StringManipulator {

    public static String compareStrings(String str1, String str2) {
        return str1.equals(str2) ? "Strings are equal." : "Strings are not equal.";
    }

    public static char toggleCase(char ch) {
        if (ch >= 'a' && ch <= 'z') {
            return (char) (ch - 32); 
        } else if (ch >= 'A' && ch <= 'Z') {
            return (char) (ch + 32); 
        } else {
            return ch; 
        }
    }

    public static String convertCase(String str) {
        StringBuilder converted = new StringBuilder();
        for (char ch : str.toCharArray()) {
            converted.append(toggleCase(ch));
        }
        return converted.toString();
    }

    public static boolean contains(String str1, String str2) {
        return str1.contains(str2);
    }

    public static String replaceSubstring(String str1, String str2) {
        return str1.replace(str2, "Hello");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        while (true) {
            System.out.println("\nMenu:");
            System.out.println("1. Compare two strings");
            System.out.println("2. Convert uppercase to lowercase and vice-versa");
            System.out.println("3. Check if one string is a substring of the other");
            System.out.println("4. Replace substring with 'Hello' if it exists");
            System.out.println("5. Exit");
            
            System.out.print("Enter your choice (1-5): ");
            int choice = scanner.nextInt();
            scanner.nextLine(); 
            
            switch (choice) {
                case 1:
                    System.out.print("Enter first string: ");
                    String str1 = scanner.nextLine();
                    System.out.print("Enter second string: ");
                    String str2 = scanner.nextLine();
                    System.out.println(compareStrings(str1, str2));
                    break;
                
                case 2:
                    System.out.print("Enter a string: ");
                    String string = scanner.nextLine();
                    System.out.println("Converted string: " + convertCase(string));
                    break;
                
                case 3:
                    System.out.print("Enter first string: ");
                    String mainStr = scanner.nextLine();
                    System.out.print("Enter second string: ");
                    String subStr = scanner.nextLine();
                    if (contains(mainStr, subStr)) {
                        System.out.println("\"" + subStr + "\" is a substring of \"" + mainStr + "\".");
                    } else {
                        System.out.println("\"" + subStr + "\" is not a substring of \"" + mainStr + "\".");
                    }
                    break;
                
                case 4:
                    System.out.print("Enter the main string: ");
                    String replaceMainStr = scanner.nextLine();
                    System.out.print("Enter the substring to replace: ");
                    String replaceSubStr = scanner.nextLine();
                    if (contains(replaceMainStr, replaceSubStr)) {
                        String result = replaceSubstring(replaceMainStr, replaceSubStr);
                        System.out.println("Updated string: " + result);
                    } else {
                        System.out.println("\"" + replaceSubStr + "\" is not a substring of \"" + replaceMainStr + "\", no replacement done.");
                    }
                    break;
                
                case 5:
                    System.out.println("Exiting the program.");
                    scanner.close();
                    return;
                
                default:
                    System.out.println("Invalid choice! Please select a valid option.");
            }
        }
    }
}
