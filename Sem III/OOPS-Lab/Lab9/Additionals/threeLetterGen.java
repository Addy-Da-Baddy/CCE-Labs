import java.util.Scanner;

public class ThreeLetterWords {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a five-letter word: ");
        String word = scanner.nextLine();
        
        System.out.print("Enter the number of common three-letter words: ");
        int n = scanner.nextInt();
        scanner.nextLine();  // Consume newline
        
        String[] commonWords = new String[n];
        System.out.println("Enter " + n + " common three-letter words:");
        for (int i = 0; i < n; i++) {
            commonWords[i] = scanner.nextLine();
        }

        System.out.println("Possible three-letter words:");
        for (String commonWord : commonWords) {
            if (canFormWord(word, commonWord)) {
                System.out.println(commonWord);
            }
        }
    }

    static boolean canFormWord(String fiveLetterWord, String threeLetterWord) {
        for (char c : threeLetterWord.toCharArray()) {
            if (fiveLetterWord.indexOf(c) == -1) {
                return false;
            }
        }
        return true;
    }
}
