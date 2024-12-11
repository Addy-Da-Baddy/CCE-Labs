import java.util.Scanner;

public class Number {
    private double num;

    Number(double num) {
        this.num = num;
    }

    boolean isZero() {
        return (num == 0);
    }

    boolean isPositive() {
        return (num > 0);
    }

    boolean isNegative() {
        return (num < 0);
    }

    boolean isEven() {
        return (num % 2 == 0);
    }

    boolean isOdd() {
        return (!isEven());
    }

    boolean isPrime() {
        if (num <= 1 || num % 1 != 0) {
            return false;
        }
        int n = (int) num;
        if (n == 2) {
            return true;
        }
        if (n % 2 == 0) {
            return false;
        }
        for (int i = 3; i <= Math.sqrt(n); i += 2) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }

    boolean isArmstrong() {
        if (num % 1 != 0) {
            return false;
        }
        int originalNum = (int) num;
        int sum = 0;
        int temp = originalNum;

        while (temp > 0) {
            int d = temp % 10;
            sum += d*d*d;
            temp /= 10;
        }

        return (originalNum == sum);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a number: ");
        double inputNum = sc.nextDouble();
        Number number = new Number(inputNum);

        System.out.println("Is Zero: " + number.isZero());
        System.out.println("Is Positive: " + number.isPositive());
        System.out.println("Is Negative: " + number.isNegative());
        System.out.println("Is Even: " + number.isEven());
        System.out.println("Is Odd: " + number.isOdd());
        System.out.println("Is Prime: " + number.isPrime());
        System.out.println("Is Armstrong: " + number.isArmstrong());

        sc.close();
    }
}
