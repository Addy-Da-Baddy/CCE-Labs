import java.util.*;

public class StudentDemo {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter number of students from MIT whose details you want to enter: ");
        int numStudents = sc.nextInt();
        sc.nextLine(); 
        Student_Detail[] details = new Student_Detail[numStudents];
        String name, id;

        for (int i = 0; i < numStudents; i++) {
            System.out.println("Enter the name and ID of student " + (i + 1) + ":");
            name = sc.nextLine();
            id = sc.nextLine();
            details[i] = new Student_Detail(name, id);
        }
        Student_Detail.display_details(details);
    }
}
