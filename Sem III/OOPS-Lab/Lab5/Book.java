import java.util.Scanner;

public class Book {
    private String title;
    private String author;
    private int edition;

    public Book(String title, String author, int edition) {
        this.title = title;
        this.author = author;
        this.edition = edition;
    }

    public void displayDetails() {
        System.out.printf("Title: %s, Author: %s, Edition: %d%n", title, author, edition);
    }

    public static void bubbleSortByTitle(Book[] books) {
        int n = books.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                String title1 = books[j].title.toLowerCase();
                String title2 = books[j + 1].title.toLowerCase();
                if (title1.compareTo(title2) > 0) {
                    Book temp = books[j];
                    books[j] = books[j + 1];
                    books[j + 1] = temp;
                }
            }
        }
    }

    public static void main(String[] args) {
        Book[] books = new Book[] {
            new Book("The Da Vinci Code", "Dan Brown", 1),
            new Book("The Invisible Man", "HG Wells", 1),
            new Book("1984", "George Orwell", 2),
            new Book("Farhenheit 451", "Ray William Bradbury", 3),
            new Book("The Lord of the Rings", "JRR Tolkien", 2),
            new Book("Animal Farm", "George Orwell", 1)
        };

        bubbleSortByTitle(books);

        Scanner sc = new Scanner(System.in);
        System.out.println("Enter Author name: ");
        String authorName = sc.nextLine();
        sc.close();

        for (Book book : books) {
            if (book.author.equalsIgnoreCase(authorName)) {
                book.displayDetails();
            }
        }
    }
}
