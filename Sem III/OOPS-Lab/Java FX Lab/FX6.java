import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class FX6 extends Application {

    @Override
    public void start(Stage stage) {
        TextField nameField = new TextField();
        TextField emailField = new TextField();
        TextField phoneField = new TextField();
        TextField skillsField = new TextField();
        
        CheckBox englishCheckBox = new CheckBox("English");
        CheckBox spanishCheckBox = new CheckBox("Spanish");
        CheckBox frenchCheckBox = new CheckBox("French");
        CheckBox germanCheckBox = new CheckBox("German");
        
        Button submitButton = new Button("Submit");
        Canvas canvas = new Canvas(400, 300);

        submitButton.setOnAction(e -> {
            String name = nameField.getText();
            String email = emailField.getText();
            String phone = phoneField.getText();
            String skills = skillsField.getText();
            StringBuilder languages = new StringBuilder();

            if (englishCheckBox.isSelected()) languages.append("English, ");
            if (spanishCheckBox.isSelected()) languages.append("Spanish, ");
            if (frenchCheckBox.isSelected()) languages.append("French, ");
            if (germanCheckBox.isSelected()) languages.append("German, ");

            if (languages.length() > 0) {
                languages.setLength(languages.length() - 2); // Remove the last comma and space
            } else {
                languages.append("None");
            }

            GraphicsContext gc = canvas.getGraphicsContext2D();
            gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight()); // Clear previous drawings

            gc.fillText("Resume", 150, 20);
            gc.fillText("Name: " + name, 20, 50);
            gc.fillText("Email: " + email, 20, 80);
            gc.fillText("Phone: " + phone, 20, 110);
            gc.fillText("Skills: " + skills, 20, 140);
            gc.fillText("Languages: " + languages.toString(), 20, 170);
        });

        GridPane gridPane = new GridPane();
        gridPane.setHgap(10);
        gridPane.setVgap(10);
        gridPane.add(new Label("Name:"), 0, 0);
        gridPane.add(nameField, 1, 0);
        gridPane.add(new Label("Email:"), 0, 1);
        gridPane.add(emailField, 1, 1);
        gridPane.add(new Label("Phone:"), 0, 2);
        gridPane.add(phoneField, 1, 2);
        gridPane.add(new Label("Skills:"), 0, 3);
        gridPane.add(skillsField, 1, 3);
        gridPane.add(new Label("Languages:"), 0, 4);
        gridPane.add(englishCheckBox, 1, 4);
        gridPane.add(spanishCheckBox, 1, 5);
        gridPane.add(frenchCheckBox, 1, 6);
        gridPane.add(germanCheckBox, 1, 7);
        gridPane.add(submitButton, 1, 8);
        gridPane.add(canvas, 0, 9, 2, 1);

        Scene scene = new Scene(gridPane, 400, 400);
        stage.setTitle("Resume Builder");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
