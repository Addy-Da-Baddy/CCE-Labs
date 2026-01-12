package com.example.calculator;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;   // <-- import Log
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private TextView tvNum1, tvNum2;
    private String num1 = "";
    private String num2 = "";
    private String operator = "";
    private boolean isSecondNum = false;

    private static final String TAG = "CalculatorApp"; // tag for Logcat

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvNum1 = findViewById(R.id.tvNum1);
        tvNum2 = findViewById(R.id.tvNum2);

        // Number buttons
        int[] numberButtons = {
                R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3,
                R.id.btn4, R.id.btn5, R.id.btn6,
                R.id.btn7, R.id.btn8, R.id.btn9
        };

        for (int id : numberButtons) {
            Button btn = findViewById(id);
            btn.setOnClickListener(v -> {
                String digit = btn.getText().toString();
                if (!isSecondNum) {
                    num1 += digit;
                    tvNum1.setText(num1);
                    Log.d(TAG, "Num1 updated: " + num1);
                } else {
                    num2 += digit;
                    tvNum2.setText(num2);
                    Log.d(TAG, "Num2 updated: " + num2);
                }
            });
        }

        // Operator buttons
        findViewById(R.id.btnPlus).setOnClickListener(v -> setOperator("+"));
        findViewById(R.id.btnMinus).setOnClickListener(v -> setOperator("-"));
        findViewById(R.id.btnMul).setOnClickListener(v -> setOperator("*"));
        findViewById(R.id.btnDiv).setOnClickListener(v -> setOperator("/"));

        // CLR button
        findViewById(R.id.btnCLR).setOnClickListener(v -> {
            num1 = "";
            num2 = "";
            operator = "";
            isSecondNum = false;
            tvNum1.setText("Num 1");
            tvNum2.setText("Num 2");
            Log.d(TAG, "Calculator cleared");
        });

        // Result button
        findViewById(R.id.btnResult).setOnClickListener(v -> {
            if (!num1.isEmpty() && !num2.isEmpty() && !operator.isEmpty()) {
                try {
                    double result = calculate(Double.parseDouble(num1), Double.parseDouble(num2), operator);
                    String expression = num1 + " " + operator + " " + num2 + " = " + result;

                    Log.d(TAG, "Calculated expression: " + expression);

                    Intent intent = new Intent(MainActivity.this, ResultActivity.class);
                    intent.putExtra("EXPRESSION", expression);
                    startActivity(intent);
                } catch (NumberFormatException e) {
                    Log.e(TAG, "Error parsing numbers: " + e.getMessage());
                }
            } else {
                Log.e(TAG, "Missing input: num1=" + num1 + ", num2=" + num2 + ", operator=" + operator);
            }
        });
    }

    private void setOperator(String op) {
        if (!num1.isEmpty()) {
            operator = op;
            isSecondNum = true;
            Log.d(TAG, "Operator set: " + operator);
        } else {
            Log.e(TAG, "Operator pressed before entering num1");
        }
    }

    private double calculate(double n1, double n2, String op) {
        switch (op) {
            case "+": return n1 + n2;
            case "-": return n1 - n2;
            case "*": return n1 * n2;
            case "/":
                if (n2 == 0) {
                    Log.e(TAG, "Division by zero attempted");
                    return Double.NaN;
                }
                return n1 / n2;
            default: return 0;
        }
    }
}
