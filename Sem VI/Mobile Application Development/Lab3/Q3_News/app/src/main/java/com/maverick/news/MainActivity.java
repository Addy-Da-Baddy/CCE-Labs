package com.maverick.news;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.material.tabs.TabLayout;

public class MainActivity extends AppCompatActivity {

    private TextView textView3, textView4, textView5;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        TabLayout tabLayout = findViewById(R.id.tab);
        textView3 = findViewById(R.id.textView3);
        textView4 = findViewById(R.id.textView4);
        textView5 = findViewById(R.id.textView5);

        // Listen for tab selections
        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                String section = tab.getText().toString();

                Toast.makeText(MainActivity.this,
                        "Selected: " + section,
                        Toast.LENGTH_SHORT).show();

                Log.d("NEWS_APP", "User selected section: " + section);

                updateHeadlines(section);
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) { }

            @Override
            public void onTabReselected(TabLayout.Tab tab) { }
        });
    }

    // Hardcoded headlines for each section
    private void updateHeadlines(String section) {
        switch (section) {
            case "Top Stories":
                textView3.setText("Global markets rally after tech surge");
                textView4.setText("New climate deal signed by leaders");
                textView5.setText("Breakthrough in AI reshaping industries");
                break;

            case "Sports":
                textView3.setText("Football: City clinches dramatic win");
                textView4.setText("Cricket: India defeats Australia in thriller");
                textView5.setText("Tennis: Nadal announces retirement plans");
                break;

            case "Entertainment":
                textView3.setText("Oscars 2026: Surprise Best Picture winner");
                textView4.setText("Music: New album from global superstar");
                textView5.setText("Streaming: Hit series renewed for Season 3");
                break;

            default:
                textView3.setText("No headlines available");
                textView4.setText("");
                textView5.setText("");
        }
    }
}
