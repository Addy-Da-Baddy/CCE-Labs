import java.util.Scanner;

// Node class
class Node<T> {
    T data;
    Node<T> next;

    public Node(T data) {
        this.data = data;
        this.next = null;
    }
}

class GenericSinglyLinkedList<T> {
    private Node<T> head;

    public GenericSinglyLinkedList() {
        this.head = null;
    }

    public void add(T data) {
        Node<T> newNode = new Node<>(data);
        if (head == null) {
            head = newNode;
        } else {
            Node<T> current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
    }

    public void display() {
        if (head == null) {
            System.out.println("List is empty.");
            return;
        }
        Node<T> current = head;
        while (current != null) {
            System.out.print(current.data + " -> ");
            current = current.next;
        }
        System.out.println("null");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        GenericSinglyLinkedList<Integer> intList = new GenericSinglyLinkedList<>();
        System.out.print("Enter number of integers: ");
        int n = scanner.nextInt();
        for (int i = 0; i < n; i++) {
            System.out.print("Enter integer: ");
            intList.add(scanner.nextInt());
        }
        System.out.println("Integer Linked List:");
        intList.display();

        GenericSinglyLinkedList<Double> doubleList = new GenericSinglyLinkedList<>();
        System.out.print("Enter number of doubles: ");
        int m = scanner.nextInt();
        for (int i = 0; i < m; i++) {
            System.out.print("Enter double: ");
            doubleList.add(scanner.nextDouble());
        }
        System.out.println("Double Linked List:");
        doubleList.display();
    }
}
