import java.util.Scanner;

public class LargestofThree {

    public static <T extends Comparable<T>> T findLargest(T obj1, T obj2, T obj3) {
        T largest = obj1;

        if (obj2.compareTo(largest) > 0) {
            largest = obj2;
        }

        if (obj3.compareTo(largest) > 0) {
            largest = obj3;
        }

        return largest;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the type of objects (Integer/String/Double): ");
        String type = scanner.next();

        if (type.equalsIgnoreCase("Integer")) {
            System.out.println("Enter three integer values:");
            Integer num1 = scanner.nextInt();
            Integer num2 = scanner.nextInt();
            Integer num3 = scanner.nextInt();

            System.out.println("Largest Integer: " + findLargest(num1, num2, num3));

        } else if (type.equalsIgnoreCase("String")) {
            System.out.println("Enter three string values:");
            String str1 = scanner.next();
            String str2 = scanner.next();
            String str3 = scanner.next();

            System.out.println("Largest String: " + findLargest(str1, str2, str3));

        } else if (type.equalsIgnoreCase("Double")) {
            System.out.println("Enter three double values:");
            Double d1 = scanner.nextDouble();
            Double d2 = scanner.nextDouble();
            Double d3 = scanner.nextDouble();

            System.out.println("Largest Double: " + findLargest(d1, d2, d3));

        } else {
            System.out.println("Invalid type entered. Please enter either 'Integer', 'String', or 'Double'.");
        }
    }
}
