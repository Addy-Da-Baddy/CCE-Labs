class Passenger extends Thread {
    private String name;
    private boolean isVip;

    public Passenger(String name, boolean isVip) {
        this.name = name;
        this.isVip = isVip;
        if (isVip) {
            setPriority(Thread.MAX_PRIORITY); // VIP passengers get maximum priority
        } else {
            setPriority(Thread.MIN_PRIORITY); // Regular passengers get minimum priority
        }
    }

    @Override
    public void run() {
        try {
            System.out.println(name + " is going through the security check. Priority: " + getPriority());
            for (int i = 1; i <= 5; i++) {
                System.out.println(name + " is being checked: step " + i);
                Thread.sleep(500); // Simulate time taken for each security step
            }
            System.out.println(name + " has cleared security.");
        } catch (InterruptedException e) {
            System.out.println(name + "'s security check was interrupted due to an emergency!");
        }
    }
}

public class priorityChecker {
    public static void main(String[] args) {
        // Create VIP and regular passengers
        Passenger vipPassenger = new Passenger("VIP Passenger", true);
        Passenger regularPassenger1 = new Passenger("Regular Passenger 1", false);
        Passenger regularPassenger2 = new Passenger("Regular Passenger 2", false);

        // Start the threads
        vipPassenger.start();
        regularPassenger1.start();
        regularPassenger2.start();

        // Interrupt a regular passenger's thread as if there's an emergency
        try {
            Thread.sleep(1000); // Allow threads to run for a bit
            System.out.println("Emergency detected! Interrupting regular passenger's security check.");
            regularPassenger1.interrupt(); // Simulate emergency interruption for a regular passenger
        } catch (InterruptedException e) {
            System.out.println(e);
        }
    }
}
