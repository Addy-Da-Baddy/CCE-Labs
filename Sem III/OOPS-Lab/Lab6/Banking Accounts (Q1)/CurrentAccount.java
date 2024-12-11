public class CurrentAccount extends Account {
    final double MIN_BALANCE = 500.0;
    final double SERVICE_TAX = 20.0;

    CurrentAccount(String name, String accNo, double initialBalance) {
        super(name, accNo, "Current", initialBalance);
    }

    @Override
    void withdraw(double amount) {
        if (amount > 0) {
            if (balance - amount >= MIN_BALANCE) {
                balance -= amount;
                System.out.println("Withdrew $" + amount + ". New balance: $" + balance);
                imposePenalty();
            } else {
                System.out.println("Insufficient balance to withdraw. Minimum balance required is $" + MIN_BALANCE);
            }
        } else {
            System.out.println("Withdrawal amount must be positive.");
        }
    }

    @Override
    void imposePenalty() {
        if (balance < MIN_BALANCE) {
            balance -= SERVICE_TAX;
            System.out.println("Imposed service tax of $" + SERVICE_TAX + ". New balance: $" + balance);
        }
    }
}
