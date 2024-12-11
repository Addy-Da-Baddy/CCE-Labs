import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class SimpleCalculator extends Application {

    @Override
    public void start(Stage stage) {
        TextField num1Field = new TextField();
        TextField num2Field = new TextField();
        Label resultLabel = new Label("Result: ");
        
        Button addButton = new Button("+");
        Button subtractButton = new Button("-");
        Button multiplyButton = new Button("*");
        Button divideButton = new Button("/");

        GridPane gridPane = new GridPane();
        gridPane.setHgap(10);
        gridPane.setVgap(10);
        gridPane.add(new Label("Number 1:"), 0, 0);
        gridPane.add(num1Field, 1, 0);
        gridPane.add(new Label("Number 2:"), 0, 1);
        gridPane.add(num2Field, 1, 1);
        gridPane.add(addButton, 0, 2);
        gridPane.add(subtractButton, 1, 2);
        gridPane.add(multiplyButton, 0, 3);
        gridPane.add(divideButton, 1, 3);
        gridPane.add(resultLabel, 0, 4, 2, 1);

        addButton.setOnAction(e -> {
            double num1 = Double.parseDouble(num1Field.getText());
            double num2 = Double.parseDouble(num2Field.getText());
            double result = num1 + num2;
            resultLabel.setText("Result: " + result);
        });

        subtractButton.setOnAction(e -> {
            double num1 = Double.parseDouble(num1Field.getText());
            double num2 = Double.parseDouble(num2Field.getText());
            double result = num1 - num2;
            resultLabel.setText("Result: " + result);
        });

        multiplyButton.setOnAction(e -> {
            double num1 = Double.parseDouble(num1Field.getText());
            double num2 = Double.parseDouble(num2Field.getText());
            double result = num1 * num2;
            resultLabel.setText("Result: " + result);
        });

        divideButton.setOnAction(e -> {
            double num1 = Double.parseDouble(num1Field.getText());
            double num2 = Double.parseDouble(num2Field.getText());
            if (num2 != 0) {
                double result = num1 / num2;
                resultLabel.setText("Result: " + result);
            } else {
                resultLabel.setText("Error: Division by zero");
            }
        });

        Scene scene = new Scene(gridPane, 300, 200);
        stage.setTitle("Simple Calculator");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
