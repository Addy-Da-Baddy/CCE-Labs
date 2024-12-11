import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.FlowPane;
import javafx.stage.Stage;

public class FX2 extends Application {

    @Override
    public void start(Stage stage) {
        TextField numberInput = new TextField();
        Button generateButton = new Button("Generate Table");
        Label resultLabel = new Label();

        FlowPane pane = new FlowPane();
        pane.setHgap(10);
        pane.setVgap(10);
        pane.getChildren().addAll(new Label("Enter a number:"), numberInput, generateButton, resultLabel);

        generateButton.setOnAction(e -> {
            int number = Integer.parseInt(numberInput.getText());
            StringBuilder result = new StringBuilder();
            for (int i = 1; i <= 10; i++) {
                result.append(number).append(" * ").append(i).append(" = ").append(number * i).append("\n");
            }
            resultLabel.setText(result.toString());	
        });

        Scene scene = new Scene(pane, 400, 250);
        stage.setTitle("Multiplication Table");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
