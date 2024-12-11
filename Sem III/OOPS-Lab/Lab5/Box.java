import java.util.Scanner;

public class Box {
    public double width, height, depth;

    public Box(double width, double height, double depth) {
        this.width = width;
        this.height = height;
        this.depth = depth;
    }

    public double getVolume() {
        return width * height * depth;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter width, height, and depth of the box: ");
        
        double w = sc.nextDouble();
        double h = sc.nextDouble();
        double d = sc.nextDouble();
        
        Box b1 = new Box(w, h, d);
        
        System.out.println("Volume of the box is: " + b1.getVolume() + " cubic units");
        
        sc.close();
    }
}
