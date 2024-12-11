import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.FlowPane;
import javafx.stage.Stage;

public class FX4 extends Application {

    @Override
    public void start(Stage stage) {
        TextField number1Field = new TextField();
        TextField number2Field = new TextField();
        Button calculateButton = new Button("Calculate GCD");
        Label resultLabel = new Label();

        FlowPane pane = new FlowPane();
        pane.setHgap(10);
        pane.setVgap(10);
        pane.getChildren().addAll(new Label("Number 1:"), number1Field, new Label("Number 2:"), number2Field, calculateButton, resultLabel);

        calculateButton.setOnAction(e -> {
            int num1 = Integer.parseInt(number1Field.getText());
            int num2 = Integer.parseInt(number2Field.getText());
            int gcd = findGCD(num1, num2);
            resultLabel.setText("Numbers: " + num1 + " and " + num2 + ", GCD: " + gcd);
        });

        Scene scene = new Scene(pane, 400, 200);
        stage.setTitle("GCD Calculator");
        stage.setScene(scene);
        stage.show();
    }

    public static int findGCD(int a, int b) {
        if (b == 0) {
            return a;
        }
        return findGCD(b, a % b);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
