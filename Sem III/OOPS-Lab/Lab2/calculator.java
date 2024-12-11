import java.util.*;

class calculator {

    static float add(float x, float y) {
        return x + y;
    }

    static float sub(float x, float y) {
        return x - y;
    }

    static float mul(float x, float y) {
        return x * y;
    }

    static float div(float x, float y) {
        if (y != 0) {
            return x / y;
        } else {
            System.out.println("Cannot divide by zero");
            return 0;
        }
    }

    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        float x, y;
        int ops;
        char c;
        do {
            System.out.println("Enter first number:");
            x = sc.nextFloat();
            System.out.println("Enter second number:");
            y = sc.nextFloat();
            System.out.println("1. Add 2. Subtract 3. Multiply 4. Divide");
            System.out.println("Enter your choice:");
            ops = sc.nextInt();
            switch (ops) {
                case 1:
                    System.out.println("Result: " + add(x, y));
                    break;
                case 2:
                    System.out.println("Result: " + sub(x, y));
                    break;
                case 3:
                    System.out.println("Result: " + mul(x, y));
                    break;
                case 4:
                    System.out.println("Result: " + div(x, y));
                    break;
                default:
                    System.out.println("Invalid Choice!");
                    break;
            }
            System.out.println("Enter 'y' to continue");
            c = sc.next().charAt(0);
        } while (c == 'y');
    }
}
