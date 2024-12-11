class MarkOutOfBoundsException extends Exception {
    public MarkOutOfBoundsException(String message) {
        super(message);
    }
}

class Student {
    private int marks;

    public void setMarks(int marks) throws MarkOutOfBoundsException {
        if (marks > 100) {
            throw new MarkOutOfBoundsException("Marks cannot be greater than 100.");
        }
        this.marks = marks;
    }

    public int getMarks() {
        return marks;
    }
}

public class StudentMarks {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Student student = new Student();

        System.out.print("Enter the student's marks: ");
        int marks = scanner.nextInt();

        try {
            student.setMarks(marks);
            System.out.println("Student's marks: " + student.getMarks());
        } catch (MarkOutOfBoundsException e) {
            System.err.println(e.getMessage());
        }

        scanner.close();
    }
}
