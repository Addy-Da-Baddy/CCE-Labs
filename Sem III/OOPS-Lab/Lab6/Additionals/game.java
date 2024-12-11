// Base class
class Game {
    // Method to be overridden
    void type() {
        System.out.println("Indoor & outdoor games");
    }
}

// Subclass Cricket
class Cricket extends Game {
    // Overriding the type method
    @Override
    void type() {
        System.out.println("Cricket is an outdoor game");
    }
}

// Subclass Chess
class Chess extends Game {
    // Overriding the type method
    @Override
    void type() {
        System.out.println("Chess is an indoor game");
    }
}

// Main class to test dynamic method dispatch
public class GameTest {
    public static void main(String[] args) {
        Game game1 = new Cricket(); // Game reference but Cricket object
        Game game2 = new Chess();   // Game reference but Chess object

        game1.type(); // Calls Cricket's type method
        game2.type(); // Calls Chess's type method
    }
}
