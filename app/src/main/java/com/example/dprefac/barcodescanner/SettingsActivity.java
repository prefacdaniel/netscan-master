package com.example.dprefac.barcodescanner;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.config.Configuration;
import com.example.dprefac.barcodescanner.exception.IncompleteRequestException;
import com.example.dprefac.barcodescanner.service.DeviceService;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.dprefac.barcodescanner.config.Configuration.SERVER_ADDRESS;

public class SettingsActivity extends AppCompatActivity {


    private static final String TAG = SettingsActivity.class.getName();

    EditText hostAddress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        hostAddress = findViewById(R.id.hostField);

    }

    public void updateHost(View view) {
        try {
            String address = hostAddress.getText().toString();
            if (address.isEmpty()) {
                throw new IncompleteRequestException("Host field can't be empty!");
            }

            Configuration.SERVER_ADDRESS = "http://" + address; //info: add also :5000 port

            Configuration.retrofit = new Retrofit.Builder()
                    .baseUrl(SERVER_ADDRESS)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();

            Configuration.deviceService = Configuration.retrofit.create(DeviceService.class);
            Toast.makeText(SettingsActivity.this, "New address: " + Configuration.SERVER_ADDRESS, Toast.LENGTH_LONG).show();

            finish();
        } catch (IncompleteRequestException e) {
            Toast.makeText(SettingsActivity.this, e.getMessage(), Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            Log.e(TAG,e.getMessage(),e);
        }
    }
}
