import java.util.*;
public class Counter {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Object obs[] = new Object[100];
        while(true){
           System.out.println("Do wish to create an object? Press Y for Yes and N for no: ");
           char ch = sc.next().charAt(0); 
           if (ch=='N'){
            break;
           }
           if (object.count==100){
            System.out.println("Maximum Limit of 100 reached!");
            break;
           }
           obs[object.count++] = new Object();
        }

        System.out.println("Number of objects created: " + object.count);

    }
}
