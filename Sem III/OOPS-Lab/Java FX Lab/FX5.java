import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class FX5 extends Application {

    @Override
    public void start(Stage stage) {
        TextField num1Field = new TextField();
        TextField num2Field = new TextField();
        Button computeButton = new Button("Compute");
        Canvas canvas = new Canvas(400, 300);
        Image calculatorImage = new Image("file:calculator.png"); // Replace with your image path

        computeButton.setOnAction(e -> {
            try {
                double num1 = Double.parseDouble(num1Field.getText());
                double num2 = Double.parseDouble(num2Field.getText());

                // Perform calculations
                double sum = num1 + num2;
                double difference = num1 - num2;
                double product = num1 * num2;
                double quotient = (num2 != 0) ? (num1 / num2) : Double.NaN; // Handle division by zero

                // Draw on the canvas
                GraphicsContext gc = canvas.getGraphicsContext2D();
                gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight()); // Clear previous drawings
                gc.drawImage(calculatorImage, 10, 10); // Draw calculator image

                // Display results
                gc.fillText("Sum: " + sum, 20, 150);
                gc.fillText("Difference: " + difference, 20, 180);
                gc.fillText("Product: " + product, 20, 210);
                gc.fillText("Quotient: " + (quotient == Double.NaN ? "undefined" : quotient), 20, 240);
            } catch (NumberFormatException ex) {
                // Handle invalid input
                GraphicsContext gc = canvas.getGraphicsContext2D();
                gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
                gc.drawImage(calculatorImage, 10, 10);
                gc.fillText("Invalid input. Please enter valid numbers.", 20, 150);
            }
        });

        GridPane gridPane = new GridPane();
        gridPane.setHgap(10);
        gridPane.setVgap(10);
        gridPane.add(new Label("Number 1:"), 0, 0);
        gridPane.add(num1Field, 1, 0);
        gridPane.add(new Label("Number 2:"), 0, 1);
        gridPane.add(num2Field, 1, 1);
        gridPane.add(computeButton, 1, 2);
        gridPane.add(canvas, 0, 3, 2, 1);

        Scene scene = new Scene(gridPane, 400, 350);
        stage.setTitle("Calculator Application");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
