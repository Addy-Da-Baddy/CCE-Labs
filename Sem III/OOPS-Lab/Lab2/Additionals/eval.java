import java.util.*;

class eval {
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
		System.out.println ("Enter a and b");
		int a = sc.nextInt();
		int b = sc.nextInt();
		System.out.println("a. " + (a << 2) + (b >> 2));
		System.out.println("b. " + (b > 0));
		System.out.println("c. " + (a + b * 100) / 10);
		System.out.println("d. " + (a & b));
	}

}
