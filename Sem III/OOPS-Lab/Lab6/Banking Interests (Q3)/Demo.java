import java.util.*;
class Demo{
    public static void main(String args[]){
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter initial bank balance: ");
        double balance = sc.nextDouble();
        SBI sbi = new SBI(balance);
        ICICI icici = new ICICI(balance);
        AXIS axis = new AXIS(balance);

        System.out.println("SBI Interest: " + (sbi.getRateOfInterest()/100.0)*balance + " INR ");
        System.out.println("ICICI Interest: " + (icici.getRateOfInterest()/100.0)*balance + " INR ");
        System.out.println("Axis Interest: " + (axis.getRateOfInterest()/100.0)*balance + " INR ");


        
    }
}