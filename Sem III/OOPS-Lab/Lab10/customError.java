import java.util.*;
class InvalidTransactionException extends Exception{
    InvalidTransactionException(String msg){
        super(msg);
    }
}

public class customError {
        public static void transactionCheck(int amount)throws InvalidTransactionException{
                if (amount>=10000|amount < 0){
                    throw new InvalidTransactionException("Amount cannot be negative or more than 10000");
                }
                System.out.println("Transaction Validated of amount: " + amount);
            }
        public static void main(String[] args) {
            System.out.println("Enter transaction amount: ");
            Scanner sc = new Scanner(System.in);
            int amt = sc.nextInt();
            sc.close();
            try{
                transactionCheck(amt);
            }
            catch (InvalidTransactionException e){
                System.err.println(e);
            }
    }    
}

