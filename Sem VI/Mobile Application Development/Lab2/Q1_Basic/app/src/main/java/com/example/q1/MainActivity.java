package com.example.q1;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    Button button1, button2, button3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        Toast.makeText(this, "onCreate(): Activity Created", Toast.LENGTH_SHORT).show();

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Button references
        button1 = findViewById(R.id.button);
        button2 = findViewById(R.id.button2);
        button3 = findViewById(R.id.button3);

        // Button click actions
        button1.setOnClickListener(v ->
                Toast.makeText(this, "onCreate(): Activity initialized", Toast.LENGTH_SHORT).show()
        );

        button2.setOnClickListener(v ->
                Toast.makeText(this, "onStart(): Activity visible", Toast.LENGTH_SHORT).show()
        );

        button3.setOnClickListener(v ->
                Toast.makeText(this, "onResume(): Ready for interaction", Toast.LENGTH_SHORT).show()
        );
    }

    @Override
    protected void onStart() {
        super.onStart();
        Toast.makeText(this, "onStart() called", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onResume() {
        super.onResume();
        Toast.makeText(this, "onResume() called", Toast.LENGTH_SHORT).show();
    }
}
