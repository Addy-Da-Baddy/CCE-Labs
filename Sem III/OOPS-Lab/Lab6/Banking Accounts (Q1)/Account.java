public abstract class Account {
    String name;
    String accNo;
    String accType;
    double balance;

    Account(String name, String accNo, String accType, double initialBalance) {
        this.name = name;
        this.accNo = accNo;
        this.accType = accType;
        this.balance = initialBalance;
    }

    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited $" + amount + ". New balance: $" + balance);
        } else {
            System.out.println("Deposit amount must be positive.");
        }
    }

    void displayBalance() {
        System.out.println("Account holder: " + name);
        System.out.println("Account number: " + accNo);
        System.out.println("Account type: " + accType);
        System.out.println("Balance: $" + balance);
    }

    void withdraw(double amount) {
        if (amount > 0) {
            if (amount <= balance) {
                balance -= amount;
                System.out.println("Withdrew $" + amount + ". New balance: $" + balance);
                imposePenalty();
            } else {
                System.out.println("Insufficient balance.");
            }
        } else {
            System.out.println("Withdrawal amount must be positive.");
        }
    }

    void imposePenalty() {
    }
}
