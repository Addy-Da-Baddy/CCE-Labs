package com.maverick.views;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btnListView = findViewById(R.id.btnListView);
        Button btnGridView = findViewById(R.id.btnGridView);
        Button btnTabLayout = findViewById(R.id.btnTabLayout);
        Button btnTableLayout = findViewById(R.id.btnTableLayout);

        btnListView.setOnClickListener(v ->
                startActivity(new Intent(MainActivity.this, ListViewActivity.class)));

        btnGridView.setOnClickListener(v ->
                startActivity(new Intent(MainActivity.this, GridViewActivity.class)));

        btnTabLayout.setOnClickListener(v ->
                startActivity(new Intent(MainActivity.this, GridViewActivity.TabLayoutActivity.class)));

        btnTableLayout.setOnClickListener(v ->
                startActivity(new Intent(MainActivity.this, TableLayoutActivity.class)));
    }
}
