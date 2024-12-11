import java.util.Scanner;
class GenericStack<T> {
    private T[] elements;
    private int top;
    private int size;

    @SuppressWarnings("unchecked")
    public GenericStack(int size) {
        this.size = size;
        elements = (T[]) new Object[size];
        top = -1;
    }

    public void push(T element) {
        if (top == size - 1) {
            System.out.println("Stack is full!");
        } else {
            elements[++top] = element;
        }
    }

    public T pop() {
        if (top == -1) {
            System.out.println("Stack is empty!");
            return null;
        } else {
            return elements[top--];
        }
    }

    public T peek() {
        if (top == -1) {
            System.out.println("Stack is empty!");
            return null;
        } else {
            return elements[top];
        }
    }
}

class Student {
    String name;
    int studentId;

    public Student(String name, int studentId) {
        this.name = name;
        this.studentId = studentId;
    }

    @Override
    public String toString() {
        return "Student [Name=" + name + ", Student ID=" + studentId + "]";
    }
}

class Employee {
    String name;
    int employeeId;

    public Employee(String name, int employeeId) {
        this.name = name;
        this.employeeId = employeeId;
    }

    @Override
    public String toString() {
        return "Employee [Name=" + name + ", Employee ID=" + employeeId + "]";
    }
}

public class genericStackDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter stack size for students: ");
        int studentStackSize = scanner.nextInt();
        GenericStack<Student> studentStack = new GenericStack<>(studentStackSize);

        for (int i = 0; i < studentStackSize; i++) {
            System.out.print("Enter Student name and ID: ");
            String name = scanner.next();
            int id = scanner.nextInt();
            studentStack.push(new Student(name, id));
        }

        System.out.println("Popped Student: " + studentStack.pop());

        System.out.print("Enter stack size for employees: ");
        int employeeStackSize = scanner.nextInt();
        GenericStack<Employee> employeeStack = new GenericStack<>(employeeStackSize);

        for (int i = 0; i < employeeStackSize; i++) {
            System.out.print("Enter Employee name and ID: ");
            String name = scanner.next();
            int id = scanner.nextInt();
            employeeStack.push(new Employee(name, id));
        }

        System.out.println("Popped Employee: " + employeeStack.pop());
    }
}
