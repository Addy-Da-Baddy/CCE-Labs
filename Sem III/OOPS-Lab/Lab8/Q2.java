import java.util.Scanner;

abstract class Shape {
    abstract double calculateArea();
}

class Rectangle extends Shape {
    double width;
    double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    double calculateArea() {
        return width * height;
    }
}

class Circle extends Shape {
    double radius;

    Circle(double radius) {
        this.radius = radius;
    }

    double calculateArea() {
        return Math.PI * radius * radius;
    }
}

class Square extends Shape {
    double side;

    Square(double side) {
        this.side = side;
    }

    double calculateArea() {
        return side * side;
    }
}

class Triangle extends Shape {
    double base;
    double height;

    Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    double calculateArea() {
        return 0.5 * base * height;
    }
}

public class Q2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the width of the rectangle: ");
        double rectWidth = scanner.nextDouble();
        System.out.print("Enter the height of the rectangle: ");
        double rectHeight = scanner.nextDouble();
        Shape rectangle = new Rectangle(rectWidth, rectHeight);
        System.out.println("Area of the rectangle: " + rectangle.calculateArea());

        System.out.print("Enter the radius of the circle: ");
        double circleRadius = scanner.nextDouble();
        Shape circle = new Circle(circleRadius);
        System.out.println("Area of the circle: " + circle.calculateArea());

        System.out.print("Enter the side length of the square: ");
        double squareSide = scanner.nextDouble();
        Shape square = new Square(squareSide);
        System.out.println("Area of the square: " + square.calculateArea());

        System.out.print("Enter the base of the triangle: ");
        double triBase = scanner.nextDouble();
        System.out.print("Enter the height of the triangle: ");
        double triHeight = scanner.nextDouble();
        Shape triangle = new Triangle(triBase, triHeight);
        System.out.println("Area of the triangle: " + triangle.calculateArea());

        scanner.close();
    }
}
