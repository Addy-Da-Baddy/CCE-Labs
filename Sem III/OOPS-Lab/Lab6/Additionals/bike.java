// Base class
class Bike {
    // Data member
    int speedLimit = 80;

    // Method to be overridden
    void run() {
        System.out.println("Bike speed limit: " + speedLimit + " km/h");
    }
}

// Subclass Splendar
class Splendar extends Bike {
    // Data member
    int speedLimit = 60;

    // Overriding the run method
    @Override
    void run() {
        System.out.println("Splendar speed limit: " + speedLimit + " km/h");
    }
}

// Main class to test runtime polymorphism
public class BikeTest {
    public static void main(String[] args) {
        Bike bike = new Splendar(); // Bike reference but Splendar object

        // This will call the run method of Splendar
        bike.run();

        // To show that data members are not polymorphic
        // Using cast to access the Splendar's speedLimit
        Splendar splendar = (Splendar) bike;
        System.out.println("Speed limit in Splendar: " + splendar.speedLimit + " km/h");
    }
}
