import java.util.*;
// enter 10 numbers and display the number of positive,negative and zeros number.
class numberList{
	public static void main(String args[]){
		Scanner sc = new Scanner(System.in);
		int z= 0;
		int p = 0;
		int ne=0;
		System.out.println("Enter the numbers: ");
		int temp;
		for (int i = 0 ; i<10;i++){
			temp = sc.nextInt();
			if (temp>0)
				 p = p + 1;
			else if(temp<0){
				 ne = ne + 1;
			}
			else if (temp==0) {
				 z = z + 1;
			}
		}
		System.out.println("Number of Positive Integers: "+p);
		System.out.println("Number of Negative Integers: "+ne);
		System.out.println("Number of Zeroes:  "+z);

		
	}
}