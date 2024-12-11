import java.util.Scanner;

class Student {
    String regNo;
    String firstName;
    String lastName;
    String degree;

    Student(String regNo, String firstName, String lastName, String degree) {
        this.regNo = regNo;
        this.firstName = firstName;
        this.lastName = lastName;
        this.degree = degree;
    }
}

public class SearchStudent {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the number of students: ");
        int n = scanner.nextInt();
        scanner.nextLine();  // Consume newline

        Student[] students = new Student[n];

        for (int i = 0; i < n; i++) {
            System.out.print("Enter Registration Number: ");
            String regNo = scanner.nextLine();
            System.out.print("Enter First Name: ");
            String firstName = scanner.nextLine();
            System.out.print("Enter Last Name: ");
            String lastName = scanner.nextLine();
            System.out.print("Enter Degree: ");
            String degree = scanner.nextLine();
            students[i] = new Student(regNo, firstName, lastName, degree);
        }

        System.out.print("Enter First Name or Last Name to search: ");
        String searchTerm = scanner.nextLine().toLowerCase();

        boolean found = false;
        for (Student student : students) {
            if (student.firstName.toLowerCase().equals(searchTerm) || student.lastName.toLowerCase().equals(searchTerm)) {
                System.out.println("Found: " + student.firstName + " " + student.lastName + ", Registration No: " + student.regNo + ", Degree: " + student.degree);
                found = true;
            }
        }

        if (!found) {
            System.out.println("No student found.");
        }
    }
}
