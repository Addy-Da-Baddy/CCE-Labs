import java.util.*;
class palindromeCheck{
	public static void main(String[] args) {
        int num;
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number: ");
		num = sc.nextInt();
		int rev = 0;
		int d ;
		int copy = num;
		while (copy!=0){
			d = copy%10;
			rev = rev*10 + d;
			copy = copy/10;

		}
		if (rev==num){
			System.out.println("Palindrome Number");
		}
		else {
			System.out.println("Not a Palindrome Number");			
		}		
    }
}