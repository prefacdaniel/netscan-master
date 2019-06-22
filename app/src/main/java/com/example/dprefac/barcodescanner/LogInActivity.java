package com.example.dprefac.barcodescanner;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;

public class LogInActivity extends AppCompatActivity {

    private Button logInButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_in);

        logInButton = findViewById(R.id.logInButton);


        logInButton.setOnClickListener(v -> {
            Intent intent = new Intent(getApplicationContext(), DeviceListActivity.class);
            getApplicationContext().startActivity(intent);
        });
    }
}
