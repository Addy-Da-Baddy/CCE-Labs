import java.util.Scanner;

public class Complex {
    private double real;
    private double imaginary;

    public Complex() {
        this.real = 0;
        this.imaginary = 0;
    }

    public Complex(double real, double imaginary) {
        this.real = real;
        this.imaginary = imaginary;
    }

    public Complex add(Complex other) {
        return new Complex(this.real + other.real, this.imaginary + other.imaginary);
    }

    public Complex add(int realPart) {
        return new Complex(this.real + realPart, this.imaginary);
    }

    public void display() {
        if (imaginary >= 0) {
            System.out.printf("%.2f + %.2fi\n", real, imaginary);
        } else {
            System.out.printf("%.2f - %.2fi\n", real, -imaginary);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter real and imaginary parts for Complex number 1: ");
        double real1 = sc.nextDouble();
        double imaginary1 = sc.nextDouble();
        Complex c1 = new Complex(real1, imaginary1);

        System.out.println("Enter real and imaginary parts for Complex number 2: ");
        double real2 = sc.nextDouble();
        double imaginary2 = sc.nextDouble();
        Complex c2 = new Complex(real2, imaginary2);

        System.out.println("Enter an integer to add to Complex number 1: ");
        int integer = sc.nextInt();

        System.out.print("Complex number 1: ");
        c1.display();
        System.out.print("Complex number 2: ");
        c2.display();

        Complex sum1 = c1.add(c2);
        System.out.print("Sum of Complex number 1 and Complex number 2: ");
        sum1.display();

        Complex sum2 = c1.add(integer);
        System.out.print("Sum of integer and Complex number 1: ");
        sum2.display();

        sc.close();
    }
}
