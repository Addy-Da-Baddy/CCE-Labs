import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.FlowPane;
import javafx.stage.Stage;
import javafx.scene.paint.Color;

public class FX extends Application {
    
    @Override
    public void start(Stage primaryStage) {
        // Create a Label with the message
        Label messageLabel = new Label("Welcome to JavaFX programming");

        // Set the text color to Magenta
        messageLabel.setTextFill(Color.MAGENTA);
        
        // Create a FlowPane layout
        FlowPane flowPane = new FlowPane();
        flowPane.setHgap(10);  // Set horizontal gap between elements
        flowPane.setVgap(10);  // Set vertical gap between elements
        
        // Add the Label to the FlowPane
        flowPane.getChildren().add(messageLabel);
        
        // Create a Scene with the FlowPane layout, width 500 and height 200
        Scene scene = new Scene(flowPane, 500, 200);
        
        // Set the title of the Stage
        primaryStage.setTitle("This is the first JavaFX Application");
        
        // Set the Scene on the Stage and display it
        primaryStage.setScene(scene);
        primaryStage.show();
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}
