import java.util.*;

class StringCount {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter lines. Type QUIT to quit");

        int numWords = 0, numChars = 0, numLines = 0, numVowels = 0;
        String vowels = "aeiouAEIOU";

        while (true) {
            String line = sc.nextLine();

            if (line.equalsIgnoreCase("QUIT")) {
                break; 
            }

            numLines++;
            numChars += line.length();

            String words[] = line.split(" "); 
            numWords += words.length;

            for (char c : line.toCharArray()) {
                if (vowels.indexOf(c) != -1) {
                    numVowels++;
                }
            }
        }

        System.out.println("Number of lines: " + numLines);
        System.out.println("Number of words: " + numWords);
        System.out.println("Number of characters: " + numChars);
        System.out.println("Number of vowels: " + numVowels);

    }
}
