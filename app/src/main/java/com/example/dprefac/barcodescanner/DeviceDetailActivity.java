package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.adapter.DateListAdapter;
import com.example.dprefac.barcodescanner.adapter.DeviceListAdapter;
import com.example.dprefac.barcodescanner.model.DateElement;
import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.model.RecordedConnection;

import java.util.ArrayList;
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

    private  int deviceId;
    private  String deviceName;
    private  String deviceImage;

    private boolean isListLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_detail);

        deviceId = getIntent().getIntExtra("DEVICE_ID", -1);
        deviceName = getIntent().getStringExtra("DEVICE_NAME");
        deviceImage = getIntent().getStringExtra("DEVICE_IMAGE");


        dateListView = findViewById(R.id.dateList);
        deviceNameTextView = findViewById(R.id.deviceNameAddDevice);

        //todo: set device image
        deviceNameTextView.setText(deviceName);
    }

    private void downloadDeviceActivities() {

        Call<List<DateElement>> productCall = deviceService.getDatesForDevice(deviceId);
        ProgressDialog mDialog = new ProgressDialog(DeviceDetailActivity.this);
        mDialog.setMessage("Please wait...");
        mDialog.setCancelable(false);
        mDialog.show();

        productCall.enqueue(new Callback<List<DateElement>>() {
            @Override
            public void onResponse(Call<List<DateElement>> call, Response<List<DateElement>> response) {
                if (response.code() == HttpsURLConnection.HTTP_OK) {

                    List<DateElement> products = response.body();
                    if (products != null && !products.isEmpty()) {
                        DateListAdapter dateListAdapter = new DateListAdapter(getApplicationContext(), R.layout.activity_list_date_view, products);
                        dateListView.setAdapter(dateListAdapter);
                    } else {
                        Toast.makeText(DeviceDetailActivity.this, "List is empty!", Toast.LENGTH_LONG).show();
                    }
                } else {
                    Toast.makeText(DeviceDetailActivity.this, COULD_NOT_RETRIEVE_LIST, Toast.LENGTH_LONG).show();
                    Log.i(TAG, COULD_NOT_RETRIEVE_LIST + ": " + response.message());
                }
                mDialog.cancel();
            }


            @Override
            public void onFailure(@NonNull Call<List<DateElement>> call, @NonNull Throwable t) {
                mDialog.cancel();
                Log.e(TAG, t.getMessage(), t);
                Toast.makeText(DeviceDetailActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
            }
        });
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
