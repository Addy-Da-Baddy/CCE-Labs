import java.util.Scanner;

class Sin {

    public static double fact(int x) {
        double fact = 1.0;
        for (int j = 1; j <= x; j++) {
            fact *= j;
        }
        return fact;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter x: ");
        double x = sc.nextDouble(); 
        int sign = 1; 
        double sin = 0.0; 

        for (int i = 1; i < 25; i++) {
            if (i % 2 != 0) {
                double numer = Math.pow(x, i); 
                double denum = fact(i); 
                double term = sign * (numer / denum);
                sign = sign * -1; 
                sin = sin + term; 
            }
        }
        System.out.println("The sine of " + x + " is: " + sin);
    }
}
