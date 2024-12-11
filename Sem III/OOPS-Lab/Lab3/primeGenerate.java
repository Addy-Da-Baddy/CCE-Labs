import java.util.*;
class primeGenerate{
    public static void main(String args[]){
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the lower and upper limits: (both inclusive) ");
        boolean isPrime;
        int LL = sc.nextInt();
        int UL = sc.nextInt();
        if (LL>UL){
            System.out.println("Lower Limit should not be more than Upper Limit");
        }
        else {
            while (LL<=UL){
                if (LL<2){
                    LL = 2;
                }
                isPrime = true;
                for (int i = 2; i<=Math.sqrt(LL);i++){
                    if (LL%i==0){
                        isPrime = false;
                        break;
                    }
                }
                if (isPrime)
                    System.out.print(LL + " ");
                LL++;
            }
        }

    }
}