public class DemoClass {
    public static void main(String[] args) {
        CurrentAccount currentAcc = new CurrentAccount("John Doe", "CA123456", 1000.0);
        
        currentAcc.displayBalance();
        
        currentAcc.deposit(200.0);
        currentAcc.withdraw(100.0);
        currentAcc.withdraw(700.0); 
        
        SavingsAccount savingsAcc = new SavingsAccount("Jane Smith", "SA654321", 500.0);
        
        savingsAcc.displayBalance();
        
        savingsAcc.deposit(100.0);
        savingsAcc.withdraw(450.0); 
        savingsAcc.computeAndDepositInterest();
        
        System.out.println("\nFinal balances:");
        currentAcc.displayBalance();
        savingsAcc.displayBalance();
    }
}
