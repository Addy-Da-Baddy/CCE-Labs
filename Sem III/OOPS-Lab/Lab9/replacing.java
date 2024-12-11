import java.util.Scanner;

class Replacing {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.println("Enter the Lines...");
        String str = in.nextLine().trim(); 
        System.out.println("Enter the word to be removed");
        String word = in.nextLine();

        String rep = "*".repeat(word.length());
        String replacedStr = str.replace(word, rep);

        System.out.println("Replaced String=\n" + replacedStr);
        in.close(); 
    }
}
