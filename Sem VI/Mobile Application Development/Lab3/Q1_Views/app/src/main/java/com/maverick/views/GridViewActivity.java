package com.maverick.views;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.GridView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

import com.google.android.material.tabs.TabLayout;

public class GridViewActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gridview);

        String[] teams = {"Real Madrid", "Man City", "PSG", "Barcelona", "Bayern", "Arsenal"};

        GridView gridView = findViewById(R.id.gridViewTeams);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_list_item_1, teams);
        gridView.setAdapter(adapter);
    }

    public static class TabLayoutActivity extends AppCompatActivity {
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_tablayout);

            TabLayout tabLayout = findViewById(R.id.tabLayout);
            ViewPager viewPager = findViewById(R.id.viewPager);

            TabPagerAdapter adapter = new TabPagerAdapter(getSupportFragmentManager());
            adapter.addFragment(new PlayersFragment(), "Players");
            adapter.addFragment(new TeamsFragment(), "Teams");
            adapter.addFragment(new MatchesFragment(), "Matches");

            viewPager.setAdapter(adapter);
            tabLayout.setupWithViewPager(viewPager);
        }
    }
}
