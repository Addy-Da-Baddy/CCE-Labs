import java.util.Scanner;

public class StudentGradeCalculator {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        try {
            System.out.print("Enter Student's Name: ");
            String name = scanner.nextLine();

            System.out.print("Enter Roll Number: ");
            String rollNumber = scanner.nextLine();

            System.out.print("Enter Marks in Subject 1: ");
            int marks1 = Integer.parseInt(scanner.nextLine());

            System.out.print("Enter Marks in Subject 2: ");
            int marks2 = Integer.parseInt(scanner.nextLine());

            System.out.print("Enter Marks in Subject 3: ");
            int marks3 = Integer.parseInt(scanner.nextLine());

            int totalMarks = marks1 + marks2 + marks3;
            double percentage = (totalMarks / 3.0);
            String grade = calculateGrade(percentage);

            System.out.println("Student Name: " + name);
            System.out.println("Roll Number: " + rollNumber);
            System.out.println("Total Marks: " + totalMarks);
            System.out.println("Percentage: " + percentage + "%");
            System.out.println("Grade: " + grade);

        } catch (NumberFormatException e) {
            System.err.println("Invalid input.Please enter numeric values for marks.");
        } catch (Exception e) {
            System.err.println(e);
        } finally {
            scanner.close();
        }
    }

    private static String calculateGrade(double percentage) {
        if (percentage >= 90) {
            return "A+";
        } else if (percentage >= 80) {
            return "A";
        } else if (percentage >= 70) {
            return "B";
        } else if (percentage >= 60) {
            return "C";
        } else if (percentage >= 50) {
            return "D";
        } else {
            return "F";
        }
    }
}
