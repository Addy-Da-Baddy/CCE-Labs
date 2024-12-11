import java.util.*;

class conversion {
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        
        System.out.println("Enter an int number");
        int i = sc.nextInt();
        
        System.out.println("Enter a double number");
        double d = sc.nextDouble();
        
        System.out.println("Enter a character");
        char ch = sc.next().charAt(0);
        
        System.out.print("int to byte: ");
        byte b1 = (byte) i;
        System.out.println(b1);
        
        System.out.print("char to int: ");
        int ci = (int) ch;
        System.out.println(ci);
        
        System.out.print("double to byte: ");
        byte b2 = (byte) d;
        System.out.println(b2);
        
        System.out.print("double to int: ");
        int di = (int) d;
        System.out.println(di);
    }
}

