package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.adapter.DateListAdapter;
import com.example.dprefac.barcodescanner.model.DateElement;
import com.example.dprefac.barcodescanner.util.Utils;

import java.util.Collections;
import java.util.List;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;
import static com.example.dprefac.barcodescanner.ProductListActivity.COULD_NOT_RETRIEVE_LIST;
import static com.example.dprefac.barcodescanner.config.Configuration.deviceService;

public class DeviceDetailActivity extends AppCompatActivity {


    private final String TAG = this.getClass().getName();

    private ListView dateListView;
    private TextView deviceNameTextView;
    private ImageView deviceIconDaily;
    private Button startTraining;

    private int deviceId;
    private String deviceName;
    private String deviceImage;

    private boolean isListLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_detail);
        try {
            deviceId = getIntent().getIntExtra("DEVICE_ID", -1);
            deviceName = getIntent().getStringExtra("DEVICE_NAME");
            deviceImage = getIntent().getStringExtra("DEVICE_IMAGE");


            dateListView = findViewById(R.id.dateList);
            deviceNameTextView = findViewById(R.id.deviceNameDetails);
            deviceIconDaily = findViewById(R.id.deviceIconDetails);
            startTraining = findViewById(R.id.startTraining);

            startTraining.setOnClickListener(view -> {
                try {
                    Intent intent = new Intent(getApplicationContext(), NewTrainingActivity.class);
                    intent.putExtra("DEVICE_ID", deviceId);
                    intent.putExtra("DEVICE_NAME", deviceName);
                    intent.putExtra("DEVICE_IMAGE", deviceImage);
                    getApplicationContext().startActivity(intent);
                } catch (Exception e) {
                    Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
                    Log.e(TAG, e.getMessage(), e);
                }
            });

            deviceIconDaily.setImageBitmap(Utils.base64StringToBitmap(deviceImage));
            deviceNameTextView.setText(deviceName);
        } catch (Exception e) {
            Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }
    }

    private void downloadDeviceActivities() {
        try {
            Call<List<DateElement>> productCall = deviceService.getDatesForDevice(deviceId);
            ProgressDialog mDialog = new ProgressDialog(DeviceDetailActivity.this);
            mDialog.setMessage("Please wait...");
            mDialog.setCancelable(false);
            mDialog.show();

            productCall.enqueue(new Callback<List<DateElement>>() {
                @Override
                public void onResponse(Call<List<DateElement>> call, Response<List<DateElement>> response) {
                    try {
                        if (response.code() == HttpsURLConnection.HTTP_OK) {

                            List<DateElement> products = response.body();
                            if (products != null && !products.isEmpty()) {
                                Collections.sort(products);
                                DateListAdapter dateListAdapter = new DateListAdapter(getApplicationContext(), R.layout.activity_list_date_view, products, deviceId, deviceName, deviceImage);
                                dateListView.setAdapter(dateListAdapter);
                            } else {
                                Toast.makeText(DeviceDetailActivity.this, "List is empty!", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            Toast.makeText(DeviceDetailActivity.this, COULD_NOT_RETRIEVE_LIST, Toast.LENGTH_LONG).show();
                            Log.i(TAG, COULD_NOT_RETRIEVE_LIST + ": " + response.message());
                        }
                        mDialog.cancel();
                    } catch (Exception e) {
                    Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG).show();
                    Log.e(TAG, e.getMessage(), e);
                }
                }


                @Override
                public void onFailure(@NonNull Call<List<DateElement>> call, @NonNull Throwable t) {
                    mDialog.cancel();
                    Log.e(TAG, t.getMessage(), t);
                    Toast.makeText(DeviceDetailActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
                }
            });
        } catch (Exception e) {
            Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (!isListLoaded) {
            downloadDeviceActivities();
            isListLoaded = true;
        }
    }
}
