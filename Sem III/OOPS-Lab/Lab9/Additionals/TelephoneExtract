import java.util.Scanner;

public class PhoneNumberExtractor {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a phone number in the form (555) 555-5555: ");
        String phoneNumber = scanner.nextLine();

        // Extracting the area code and the phone number parts
        String areaCode = phoneNumber.substring(1, 4);
        String firstPart = phoneNumber.substring(6, 9);
        String secondPart = phoneNumber.substring(10, 14);

        System.out.println("Area Code: " + areaCode);
        System.out.println("Phone Number: " + firstPart + "-" + secondPart);
    }
}
