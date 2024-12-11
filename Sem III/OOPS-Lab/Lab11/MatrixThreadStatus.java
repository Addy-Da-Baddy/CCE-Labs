public class MatrixThreadStatus {
    public static void main(String[] args) {
        Matrix matrix = new Matrix(2, 2); // Reuse the Matrix class from Program 2

        // Create threads for each operation
        MatrixThread t1 = new MatrixThread(matrix, "display");
        MatrixThread t2 = new MatrixThread(matrix, "transpose");
        MatrixThread t3 = new MatrixThread(matrix, "max");
        MatrixThread t4 = new MatrixThread(matrix, "diagonal");
        MatrixThread t5 = new MatrixThread(matrix, "nonDiagonal");

        // Start the threads
        t1.start();
        t2.start();
        t3.start();

        // Demonstrate join() and isAlive()
        try {
            // Wait for t1 to finish
            t1.join();
            System.out.println("t1 has finished execution.");

            // Check if t2 is still alive
            if (t2.isAlive()) {
                System.out.println("t2 is still running.");
            } else {
                System.out.println("t2 has finished execution.");
            }

            // Wait for t2, t3, t4, and t5 to finish
            t2.join();
            t3.join();
            t4.join();
            t5.join();

            System.out.println("All threads have finished execution.");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
