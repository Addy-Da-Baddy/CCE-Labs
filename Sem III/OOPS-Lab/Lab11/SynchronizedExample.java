class SharedResource {
    private int count = 0;

    // Synchronized method
    public synchronized void incrementUsingMethod(String threadName) {
        count++;
        System.out.println(threadName + " (method) count: " + count);
    }

    // Synchronized block
    public void incrementUsingBlock(String threadName) {
        synchronized (this) {
            count++;
            System.out.println(threadName + " (block) count: " + count);
        }
    }
}

class MethodThread extends Thread {
    private SharedResource resource;
    public MethodThread(SharedResource resource) { this.resource = resource; }
    public void run() {
        for (int i = 0; i < 3; i++) resource.incrementUsingMethod("Thread 1");
    }
}

class BlockThread extends Thread {
    private SharedResource resource;
    public BlockThread(SharedResource resource) { this.resource = resource; }
    public void run() {
        for (int i = 0; i < 3; i++) resource.incrementUsingBlock("Thread 2");
    }
}

public class SynchronizedExample {
    public static void main(String[] args) {
        SharedResource resource = new SharedResource();
        new MethodThread(resource).start();
        new BlockThread(resource).start();
    }
}
