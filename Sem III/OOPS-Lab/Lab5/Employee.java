import java.util.*;
public class Employee {
    String name;
    String city;
    double BS;
    double DA;
    double HRA;

    void getData(){
        Scanner sc = new Scanner (System.in);
        System.out.println("Enter in order the following: Name, City, Basic Salary, Dearness Allowance (DA%) and House Rent(HRA%)");
        name = sc.nextLine();
        city = sc.next();
        BS = sc.nextDouble();
        DA = sc.nextDouble();
        HRA = sc.nextDouble();
    }

    double calculate(){
        double total = BS + ((BS*DA)/(100.0)) + ((BS*HRA)/(100.0));
        return total;
    }

    void display(double total){
        System.out.println("The total salary of " + name + " is INR " + total);
    }
    
    public static void main(String[] args){
        Employee e1 = new Employee();
        e1.getData();
        e1.display(e1.calculate());
    }
}
