import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class FX3 extends Application {

    @Override
    public void start(Stage stage) {
        Label userNameLabel = new Label("UserName:");
        TextField userNameField = new TextField();
        Label passwordLabel = new Label("Password:");
        PasswordField passwordField = new PasswordField();
        Button signInButton = new Button("Sign in");
        Text welcomeText = new Text();

        GridPane gridPane = new GridPane();
        gridPane.setHgap(10);
        gridPane.setVgap(10);
        gridPane.add(userNameLabel, 0, 0);
        gridPane.add(userNameField, 1, 0);
        gridPane.add(passwordLabel, 0, 1);
        gridPane.add(passwordField, 1, 1);
        gridPane.add(signInButton, 1, 2);
        gridPane.add(welcomeText, 1, 3);

        signInButton.setOnAction(e -> {
            String userName = userNameField.getText();
            welcomeText.setText("Welcome " + userName);
        });

        Scene scene = new Scene(gridPane, 300, 200);
        stage.setTitle("Sign In");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
