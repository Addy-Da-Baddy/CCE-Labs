import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class wildcardDemo {

    public static void printList(List<?> list) {
        for (Object element : list) {
            System.out.println(element);
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        List<Integer> intList = new ArrayList<>();
        System.out.print("Enter number of integers: ");
        int n = scanner.nextInt();
        for (int i = 0; i < n; i++) {
            System.out.print("Enter integer: ");
            intList.add(scanner.nextInt());
        }

        List<String> strList = new ArrayList<>();
        System.out.print("Enter number of strings: ");
        int m = scanner.nextInt();
        scanner.nextLine();
        for (int i = 0; i < m; i++) {
            System.out.print("Enter string: ");
            strList.add(scanner.nextLine());
        }

        System.out.println("Integer List:");
        printList(intList);

        System.out.println("\nString List:");
        printList(strList);
    }
}
