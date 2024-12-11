import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class FX8 extends Application {

    @Override
    public void start(Stage stage) {
        TextField diameterField = new TextField();
        Button calculateButton = new Button("Calculate");
        Canvas canvas = new Canvas(400, 300);
        ListView<String> optionsListView = new ListView<>();
        optionsListView.getItems().addAll("Area", "Radius", "Diameter", "Circumference");

        calculateButton.setOnAction(e -> {
            try {
                double diameter = Double.parseDouble(diameterField.getText());
                double radius = diameter / 2;
                double area = Math.PI * radius * radius;
                double circumference = Math.PI * diameter;

                String selectedOption = optionsListView.getSelectionModel().getSelectedItem();
                String result = "";

                switch (selectedOption) {
                    case "Area":
                        result = "Area: " + area;
                        break;
                    case "Radius":
                        result = "Radius: " + radius;
                        break;
                    case "Diameter":
                        result = "Diameter: " + diameter;
                        break;
                    case "Circumference":
                        result = "Circumference: " + circumference;
                        break;
                }

                GraphicsContext gc = canvas.getGraphicsContext2D();
                gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight()); // Clear previous drawings
                gc.fillText(result, 20, 30);
                gc.fillText("Diameter: " + diameter, 20, 60);
                gc.fillText("Radius: " + radius, 20, 90);
                gc.fillText("Circumference: " + circumference, 20, 120);

                // Draw the circle
                gc.strokeOval(150, 100, diameter, diameter);

            } catch (NumberFormatException ex) {
                GraphicsContext gc = canvas.getGraphicsContext2D();
                gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
                gc.fillText("Invalid input. Please enter a valid number.", 20, 30);
            }
        });

        GridPane gridPane = new GridPane();
        gridPane.setHgap(10);
        gridPane.setVgap(10);
        gridPane.add(new Label("Enter Diameter:"), 0, 0);
        gridPane.add(diameterField, 1, 0);
        gridPane.add(optionsListView, 0, 1, 2, 1);
        gridPane.add(calculateButton, 0, 2);
        gridPane.add(canvas, 0, 3, 2, 1);

        Scene scene = new Scene(gridPane, 400, 350);
        stage.setTitle("Circle Calculator");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
