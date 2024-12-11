import java.util.*;
//To accept lenght and breadth of a rectangle and display its area and circumfurence 
class areaRectangle{
	public static void main(String args[]){
		Scanner sc = new Scanner(System.in);
		int l,b,a,c;
		System.out.println("Enter the Length: ");
		l = sc.nextInt();
		System.out.println("Enter the Breadth: ");
		b = sc.nextInt();
		a = l*b;
		c = 2*(l+b);
		System.out.println("Area of the rectangle: "+ a );
		System.out.println("Circumfurence of the rectangle: "+ c);
		
		
	}
}
