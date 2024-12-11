import java.util.Scanner;

class ArrayOverflowException extends Exception {
    public ArrayOverflowException(String message) {
        super(message);
    }
}

public class arrayOverflow {
    int[] array;
    int size;
    int count;

    public arrayOverflow(int size) {
        this.size = size;
        this.array = new int[size];
        this.count = 0;
    }

    public void addElement(int element) throws ArrayOverflowException {
        if (count >= size) {
            throw new ArrayOverflowException("Array Full");
        }
        array[count] = element;
        count++;
    }

    public void displayElements() {
        for (int i = 0; i < count; i++) {
            System.out.print(array[i] + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the size of the array: ");
        int size = scanner.nextInt();

        arrayOverflow arrOverflow = new arrayOverflow(size);

        while (true) {
            System.out.print("Enter a number to add to the array (or -1 to stop): ");
            int input = scanner.nextInt();
            if (input == -1) {
                break;
            }
            try {
                arrOverflow.addElement(input);
                System.out.println("Element added successfully.");
            } catch (ArrayOverflowException e) {
                System.out.println(e);
            }
        }

        System.out.println("Current elements in the array:");
        arrOverflow.displayElements();
        scanner.close();
    }
}

