import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class Additional1 extends Application {

    public class Employee {
        String name;
        String empID;
        String designation;
        double basicPay;
        double DA;
        double HRA;
        double PF;
        double LIC;
        double netSalary;

        public Employee(String name, String empID, String designation, double basicPay, double LIC) {
            this.name = name;
            this.empID = empID;
            this.designation = designation;
            this.basicPay = basicPay;
            this.LIC = LIC;
            this.DA = 0.40 * basicPay;
            this.HRA = 0.15 * basicPay;
            this.PF = 0.12 * basicPay;
            this.netSalary = calculateNetSalary();
        }

        public double calculateNetSalary() {
            return basicPay + DA + HRA - PF - LIC;
        }
    }

    @Override
    public void start(Stage stage) {
        Label nameLabel = new Label("Name:");
        TextField nameField = new TextField();
        
        Label empIDLabel = new Label("Employee ID:");
        TextField empIDField = new TextField();
        
        Label designationLabel = new Label("Designation:");
        TextField designationField = new TextField();
        
        Label basicPayLabel = new Label("Basic Pay:");
        TextField basicPayField = new TextField();
        
        Label licLabel = new Label("LIC:");
        TextField licField = new TextField();
        
        Button displayButton = new Button("Display Employee Info");
        Label resultLabel = new Label();

        GridPane gridPane = new GridPane();
        gridPane.setHgap(10);
        gridPane.setVgap(10);
        gridPane.add(nameLabel, 0, 0);
        gridPane.add(nameField, 1, 0);
        gridPane.add(empIDLabel, 0, 1);
        gridPane.add(empIDField, 1, 1);
        gridPane.add(designationLabel, 0, 2);
        gridPane.add(designationField, 1, 2);
        gridPane.add(basicPayLabel, 0, 3);
        gridPane.add(basicPayField, 1, 3);
        gridPane.add(licLabel, 0, 4);
        gridPane.add(licField, 1, 4);
        gridPane.add(displayButton, 1, 5);
        gridPane.add(resultLabel, 1, 6);

        displayButton.setOnAction(e -> {
            String name = nameField.getText();
            String empID = empIDField.getText();
            String designation = designationField.getText();
            double basicPay = Double.parseDouble(basicPayField.getText());
            double LIC = Double.parseDouble(licField.getText());

            Employee employee = new Employee(name, empID, designation, basicPay, LIC);
            resultLabel.setText(
                "Name: " + employee.name + "\n" +
                "Employee ID: " + employee.empID + "\n" +
                "Designation: " + employee.designation + "\n" +
                "Basic Pay: " + employee.basicPay + "\n" +
                "DA: " + employee.DA + "\n" +
                "HRA: " + employee.HRA + "\n" +
                "PF: " + employee.PF + "\n" +
                "LIC: " + employee.LIC + "\n" +
                "Net Salary: " + employee.netSalary
            );
        });

        Scene scene = new Scene(gridPane, 400, 300);
        stage.setTitle("Employee Information");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
