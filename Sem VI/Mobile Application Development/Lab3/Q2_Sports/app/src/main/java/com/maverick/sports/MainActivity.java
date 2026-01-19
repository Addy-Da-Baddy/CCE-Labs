package com.maverick.sports;

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
        TabLayout tab = findViewById(R.id.tab);
        TextView text = findViewById(R.id.textView);

        tab.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                String sport = tab.getText().toString();
                Toast.makeText(MainActivity.this, "You selected: " + sport, Toast.LENGTH_SHORT).show();
                Log.d("[SELECTED SPORT]", sport);
                text.setText(getTopPlayers(sport));
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {

            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {

            }
        });


    }
    private String getTopPlayers(String sport) { switch (sport) { case "Basketball": return "Top 10 Basketball Players:\n" + "1. Michael Jordan\n2. LeBron James\n3. Kareem Abdul-Jabbar\n4. Magic Johnson\n5. Kobe Bryant\n6. Larry Bird\n7. Shaquille O'Neal\n8. Tim Duncan\n9. Wilt Chamberlain\n10. Hakeem Olajuwon"; case "Football": return "Top 10 Football Players:\n" + "1. Pelé\n2. Diego Maradona\n3. Lionel Messi\n4. Cristiano Ronaldo\n5. Johan Cruyff\n6. Zinedine Zidane\n7. Ronaldo Nazário\n8. Ronaldinho\n9. Franz Beckenbauer\n10. Michel Platini"; case "Cricket": return "Top 10 Cricket Players:\n" + "1. Sachin Tendulkar\n2. Don Bradman\n3. Virat Kohli\n4. Brian Lara\n5. Ricky Ponting\n6. Jacques Kallis\n7. Muttiah Muralitharan\n8. Shane Warne\n9. Kumar Sangakkara\n10. MS Dhoni"; default: return "No players available."; } }

}