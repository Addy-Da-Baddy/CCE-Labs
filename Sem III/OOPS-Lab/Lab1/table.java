import java.util.*;
class table{
	public static void main(String args[]){
		Scanner sc = new Scanner (System.in);
		System.out.println("Enter a numnber: ");
		int num = sc.nextInt();
		int p;
		for (int i = 1; i<=12;i++){
			p = num*i;
			System.out.println(num + " x " + i + " = " + p);
		}
	}
}7


