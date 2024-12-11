public class SavingsAccount extends Account {
    final double INTEREST_RATE = 0.04; 
    final double MIN_BALANCE = 100.0;

    SavingsAccount(String name, String accNo, double initialBalance) {
        super(name, accNo, "Savings", initialBalance);
    }

    @Override
    void withdraw(double amount) {
        if (amount > 0) {
            if (balance - amount >= MIN_BALANCE) {
                balance -= amount;
                System.out.println("Withdrew $" + amount + ". New balance: $" + balance);
            } else {
                System.out.println("Insufficient balance to withdraw. Minimum balance required is $" + MIN_BALANCE);
            }
        } else {
            System.out.println("Withdrawal amount must be positive.");
        }
    }

    void computeAndDepositInterest() {
        double interest = balance * INTEREST_RATE;
        deposit(interest);
        System.out.println("Interest of $" + interest + " added to account.");
    }
}