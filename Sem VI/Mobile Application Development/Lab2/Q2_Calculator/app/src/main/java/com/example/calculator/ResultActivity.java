package com.example.calculator;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;

public class ResultActivity extends AppCompatActivity {

    private static final String TAG = "CalculatorApp";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        TextView tvResult = findViewById(R.id.tvResult);
        String expression = getIntent().getStringExtra("EXPRESSION");

        if (expression != null) {
            tvResult.setText(expression);
            Log.d(TAG, "ResultActivity received expression: " + expression);
        } else {
            Log.e(TAG, "No expression received in ResultActivity");
        }

        // Use OnBackPressedDispatcher for back handling
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                Log.d(TAG, "Back pressed in ResultActivity via dispatcher");
                finish(); // closes this activity and returns to MainActivity
            }
        });
    }
}
