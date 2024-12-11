import java.util.*;

class bitwiseOps {
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        
        System.out.println("Enter an int number");
        int i = sc.nextInt();
		int mult = i << 1;
		int div = i >> 1;
		
		System.out.println("After multiplying by 2 using bitwise: " + mult);
        
		System.out.println("After dividing by 2 using bitwise: " + div);

		
    }
}
