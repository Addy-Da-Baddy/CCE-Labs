import java.util.Scanner;

public class genericSwap {

    public static <T> void swap(T[] array, int index1, int index2) {
        T temp = array[index1];
        array[index1] = array[index2];
        array[index2] = temp;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the type of array (Integer/String): ");
        String type = scanner.next();

        if (type.equalsIgnoreCase("Integer")) {
            System.out.print("Enter the number of elements in the array: ");
            int n = scanner.nextInt();
            Integer[] intArray = new Integer[n];

            System.out.println("Enter the elements of the array:");
            for (int i = 0; i < n; i++) {
                intArray[i] = scanner.nextInt();
            }

            System.out.print("Enter the first index to swap: ");
            int index1 = scanner.nextInt();
            System.out.print("Enter the second index to swap: ");
            int index2 = scanner.nextInt();

            swap(intArray, index1, index2);

            System.out.println("Array after swapping:");
            for (Integer element : intArray) {
                System.out.print(element + " ");
            }

        } else if (type.equalsIgnoreCase("String")) {
            System.out.print("Enter the number of elements in the array: ");
            int n = scanner.nextInt();
            String[] strArray = new String[n];

            System.out.println("Enter the elements of the array:");
            for (int i = 0; i < n; i++) {
                strArray[i] = scanner.next();
            }

            System.out.print("Enter the first index to swap: ");
            int index1 = scanner.nextInt();
            System.out.print("Enter the second index to swap: ");
            int index2 = scanner.nextInt();

            swap(strArray, index1, index2);

            System.out.println("Array after swapping:");
            for (String element : strArray) {
                System.out.print(element + " ");
            }

        } else {
            System.out.println("Invalid type entered. Please enter either 'Integer' or 'String'.");
        }
    }
}
