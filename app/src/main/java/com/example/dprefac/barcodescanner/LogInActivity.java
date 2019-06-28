package com.example.dprefac.barcodescanner;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.Toast;

public class LogInActivity extends AppCompatActivity {
    private static final String TAG = LogInActivity.class.getName();
    private Button logInButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_in);

        try {
            logInButton = findViewById(R.id.logInButton);


            logInButton.setOnClickListener(v -> {
                Intent intent = new Intent(getApplicationContext(), DeviceListActivity.class);
                getApplicationContext().startActivity(intent);
            });
        } catch (Exception e) {
            Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == R.id.your_item_id) {
            Intent intent = new Intent(getApplicationContext(), SettingsActivity.class);
            getApplicationContext().startActivity(intent);
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
