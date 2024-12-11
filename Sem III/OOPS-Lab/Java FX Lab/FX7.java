import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.RadioButton;
import javafx.scene.control.ToggleGroup;
import javafx.scene.layout.BorderPane;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class FX7 extends Application {

    private static final String MESSAGE = "Welcome to JavaFX scrolling message application! ";

    @Override
    public void start(Stage stage) {
        Text messageText = new Text(MESSAGE);
        messageText.setStyle("-fx-font-size: 24;");

        RadioButton leftToRightButton = new RadioButton("Scroll Left to Right");
        RadioButton rightToLeftButton = new RadioButton("Scroll Right to Left");
        ToggleGroup toggleGroup = new ToggleGroup();
        leftToRightButton.setToggleGroup(toggleGroup);
        rightToLeftButton.setToggleGroup(toggleGroup);
        leftToRightButton.setSelected(true); // Default selection

        BorderPane root = new BorderPane();
        root.setTop(leftToRightButton);
        root.setCenter(messageText);
        root.setBottom(rightToLeftButton);
        
        Scene scene = new Scene(root, 600, 100);
        stage.setTitle("Scrolling Message");
        stage.setScene(scene);
        stage.show();

        new Thread(() -> {
            double x = 600; // Start position for scrolling
            while (true) {
                // Determine the direction based on selected radio button
                if (leftToRightButton.isSelected()) {
                    x += 2; // Move right
                    if (x > scene.getWidth()) {
                        x = -messageText.getLayoutBounds().getWidth(); // Reset position
                    }
                } else {
                    x -= 2; // Move left
                    if (x < -messageText.getLayoutBounds().getWidth()) {
                        x = scene.getWidth(); // Reset position
                    }
                }
                final double finalX = x;
                // Update message position in the JavaFX application thread
                javafx.application.Platform.runLater(() -> messageText.setLayoutX(finalX));
                try {
                    Thread.sleep(30); // Control the speed of the scrolling
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
