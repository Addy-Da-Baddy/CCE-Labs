package com.maverick.views;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import androidx.appcompat.app.AppCompatActivity;

public class ListViewActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_listview);

        String[] scorers = {
                "Raphinha - 34G/26A",
                "Mohamed Salah - 34G/23A",
                "Harry Kane - 38G/13A",
                "Ousmane Dembélé - 33G/15A",
                "Kylian Mbappé - 42G/4A",
                "Robert Lewandowski - 42G/3A",
                "Omar Marmoush - 28G/17A",
                "Serhou Guirassy - 34G/9A",
                "Lamine Yamal - 18G/25A",
                "Bradley Barcola - 21G/19A"
        };


        ListView listView = findViewById(R.id.listViewScorers);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_list_item_1, scorers);
        listView.setAdapter(adapter);
    }
}
