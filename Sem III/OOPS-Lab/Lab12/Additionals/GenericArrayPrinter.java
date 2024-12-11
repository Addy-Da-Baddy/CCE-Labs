import java.util.Scanner;

public class GenericArrayPrinter {

    public static <T> void printArray(T[] array) {
        for (T element : array) {
            System.out.print(element + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the type of array (Integer/String/Double): ");
        String type = scanner.next();

        if (type.equalsIgnoreCase("Integer")) {
            System.out.print("Enter the number of elements in the array: ");
            int n = scanner.nextInt();
            Integer[] intArray = new Integer[n];

            System.out.println("Enter the elements of the array:");
            for (int i = 0; i < n; i++) {
                intArray[i] = scanner.nextInt();
            }

            System.out.println("Printing Integer array:");
            printArray(intArray);

        } else if (type.equalsIgnoreCase("String")) {
            System.out.print("Enter the number of elements in the array: ");
            int n = scanner.nextInt();
            String[] strArray = new String[n];

            System.out.println("Enter the elements of the array:");
            for (int i = 0; i < n; i++) {
                strArray[i] = scanner.next();
            }

            System.out.println("Printing String array:");
            printArray(strArray);

        } else if (type.equalsIgnoreCase("Double")) {
            System.out.print("Enter the number of elements in the array: ");
            int n = scanner.nextInt();
            Double[] doubleArray = new Double[n];

            System.out.println("Enter the elements of the array:");
            for (int i = 0; i < n; i++) {
                doubleArray[i] = scanner.nextDouble();
            }

            System.out.println("Printing Double array:");
            printArray(doubleArray);

        } else {
            System.out.println("Invalid type entered. Please enter either 'Integer', 'String', or 'Double'.");
        }
    }
}
