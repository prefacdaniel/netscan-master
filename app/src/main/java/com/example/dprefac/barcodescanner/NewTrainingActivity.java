package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.model.TrainingRequest;
import com.example.dprefac.barcodescanner.util.Utils;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;
import static com.example.dprefac.barcodescanner.config.Configuration.deviceService;

public class NewTrainingActivity extends AppCompatActivity {

    private static final String TAG = NewTrainingActivity.class.getName();
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
        try {
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

            startNewTraining.setOnClickListener(view -> {
                try {

                    TrainingRequest trainingRequest = new TrainingRequest();
                    trainingRequest.setDeviceId(deviceId);
                    if (normalRadioButton.isChecked()) {
                        trainingRequest.setUse_unknown_status_data(true);
                    }

                    Call<Void> productCall = deviceService.startNewTraining(trainingRequest);
                    ProgressDialog mDialog = new ProgressDialog(NewTrainingActivity.this);
                    mDialog.setMessage("Please wait...");
                    mDialog.setCancelable(false);
                    mDialog.show();

                    productCall.enqueue(new Callback<Void>() {
                        @Override
                        public void onResponse(Call<Void> call, Response<Void> response) {
                            try {
                                if (response.code() == HttpsURLConnection.HTTP_OK) {
                                    Toast.makeText(NewTrainingActivity.this, "Training started successfully!", Toast.LENGTH_LONG).show();
                                } else {
                                    Toast.makeText(NewTrainingActivity.this, "No training started!", Toast.LENGTH_LONG).show();
                                }
                                mDialog.cancel();
                            } catch (Exception e) {
                                Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG).show();
                                Log.e(TAG, e.getMessage(), e);
                            }
                            finish();
                        }

                        @Override
                        public void onFailure(@NonNull Call<Void> call, @NonNull Throwable t) {
                            mDialog.cancel();
                            Log.e(TAG, t.getMessage(), t);
                            Toast.makeText(NewTrainingActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
                            finish();
                        }
                    });
                } catch (Exception e) {
                    Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
                    Log.e(TAG, e.getMessage(), e);
                }
            });
        } catch (Exception e) {
            Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }
    }
}
