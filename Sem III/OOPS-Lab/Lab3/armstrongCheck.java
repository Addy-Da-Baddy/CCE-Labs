import java.util.*;
class armstrongCheck{
    public static void main(String args[]){
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a number: ");
        int num = sc.nextInt();
        int copy = num;
        int sum = 0;
        while (copy!=0){
            int d = copy%10;
            sum = sum + (int)Math.pow(d,3);
;            copy = copy/10;
        }
        if (sum==num){
            System.out.println(num + " is an armstrong number");
        }
        else {
            System.out.println(num + " is not an armstrong number");
        }
    }
}

