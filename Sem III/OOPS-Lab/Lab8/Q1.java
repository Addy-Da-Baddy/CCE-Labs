import java.util.Scanner;

interface Sales {
    int calcSales();
    String getDescription();
}

class Hardware implements Sales {
    private String category;
    private String manufacturer;
    private int totalSales;

    Hardware(String category, String manufacturer) {
        this.category = category;
        this.manufacturer = manufacturer;
    }

    public int calcSales() {
        Scanner sc = new Scanner(System.in);
        totalSales = 0;
        System.out.println("Enter sales for the last 3 months for Hardware Product:");
        for (int i = 1; i <= 3; i++) {
            System.out.print("Month " + i + ": ");
            int sales = sc.nextInt();
            totalSales += sales;
        }
        return totalSales;
    }

    public String getDescription() {
        return "Hardware Product of Category: " + category + ", Manufacturer: " + manufacturer;
    }

    public int getTotalSales() {
        return totalSales;
    }
}

class Software implements Sales {
    private String type;
    private String operatingSystem;
    private int totalSales;

    Software(String type, String operatingSystem) {
        this.type = type;
        this.operatingSystem = operatingSystem;
    }

    public int calcSales() {
        Scanner sc = new Scanner(System.in);
        totalSales = 0;
        System.out.println("Enter sales for the last 3 months for Software Product:");
        for (int i = 1; i <= 3; i++) {
            System.out.print("Month " + i + ": ");
            int sales = sc.nextInt();
            totalSales += sales;
        }
        return totalSales;
    }

    public String getDescription() {
        return "Software Product of Type: " + type + ", OS: " + operatingSystem;
    }

    public int getTotalSales() {
        return totalSales;
    }
}

public class Q1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        Hardware h1 = new Hardware("CPU", "AMD Ryzen 7000");
        Software s1 = new Software("Antivirus", "Debian");
        
        int hardwareSales = h1.calcSales();
        int softwareSales = s1.calcSales();
        
        System.out.println("\n--- Bill Summary ---");
        System.out.println(h1.getDescription());
        System.out.println("Total Sales for Last 3 Months: INR " + hardwareSales);
        System.out.println(s1.getDescription());
        System.out.println("Total Sales for Last 3 Months: INR " + softwareSales);
        System.out.println("---------------------");
        System.out.println("Total Sales for All Products: INR " + (hardwareSales + softwareSales));
    }
}
