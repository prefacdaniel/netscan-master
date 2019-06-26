package com.example.dprefac.barcodescanner;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.TextView;

import com.example.dprefac.barcodescanner.util.Utils;

public class NewTrainingActivity extends AppCompatActivity {

    private int deviceId;
    private String deviceImage;
    private String deviceName;


    private ImageView deviceIconTraining;
    private TextView deviceNameTraining;

    private RadioButton maliciousradioButton;
    private RadioButton ignoredRadioButton;
    private RadioButton normalRadioButton;

    private Button startNewTraining;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_training);

        deviceIconTraining = findViewById(R.id.deviceIconTraining);
        deviceNameTraining = findViewById(R.id.deviceNameTraining);

        maliciousradioButton = findViewById(R.id.maliciousradioButton);
        ignoredRadioButton = findViewById(R.id.ignoredRadioButton);
        normalRadioButton = findViewById(R.id.normalRadioButton);

        startNewTraining = findViewById(R.id.startNewTraining);

        deviceId = getIntent().getIntExtra("DEVICE_ID", -1);
        deviceName = getIntent().getStringExtra("DEVICE_NAME");
        deviceImage = getIntent().getStringExtra("DEVICE_IMAGE");

        deviceNameTraining.setText(deviceName);
        deviceIconTraining.setImageBitmap(Utils.base64StringToBitmap(deviceImage));

        startNewTraining.setOnClickListener(view ->{
            //todo
        });
    }
}
