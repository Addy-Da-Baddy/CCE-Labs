import java.util.Scanner;

// Class implementing Runnable interface
class RunnableExample implements Runnable {
    public void run() {
        System.out.println("Thread using Runnable interface is running.");
    }
}

// Class extending Thread class
class ThreadExample extends Thread {
    public void run() {
        System.out.println("Thread using Thread class is running.");
    }
}

public class interfaceThreadDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int choice;

        do {
            System.out.println("\n--- Thread Creation Menu ---");
            System.out.println("1. Create Thread using Runnable Interface");
            System.out.println("2. Create Thread by Extending Thread Class");
            System.out.println("3. Exit");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    // Creating thread using Runnable interface
                    RunnableExample runnableExample = new RunnableExample();
                    Thread thread1 = new Thread(runnableExample);
                    thread1.start();
                    break;

                case 2:
                    // Creating thread by extending Thread class
                    ThreadExample threadExample = new ThreadExample();
                    threadExample.start();
                    break;

                case 3:
                    System.out.println("Exiting...");
                    break;

                default:
                    System.out.println("Invalid choice! Please choose again.");
            }
        } while (choice != 3);

        scanner.close();
    }
}
