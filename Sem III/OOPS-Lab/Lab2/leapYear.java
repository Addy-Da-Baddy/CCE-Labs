import java.util.*;

class leapYear {
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        int y;
        boolean isLeap;
        System.out.println("Enter a year");
        y = sc.nextInt();
        
        if (y % 4 == 0) {
            if (y % 100 == 0) {
                if (y % 400 == 0) {
                    isLeap = true;
                } else {
                    isLeap = false;
                }
            } else {
                isLeap = true;
            }
        } else {
            isLeap = false;
        }
        
        if (isLeap) {
            System.out.println(y + " is a leap year");
        } else {
            System.out.println(y + " is not a leap year");
        }
    }
}
