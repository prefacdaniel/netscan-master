package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.adapter.DeviceListAdapter;
import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.service.DeviceService;

import java.util.List;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;
import static com.example.dprefac.barcodescanner.ProductListActivity.COULD_NOT_RETRIEVE_LIST;
import static com.example.dprefac.barcodescanner.config.Configuration.SERVER_ADDRESS;

public class DeviceListActivity extends AppCompatActivity {

    private ListView devicesListView;
    private Button addDeviceButton;

    private static final String TAG = DeviceListActivity.class.getName();
    private boolean isListLoaded = false;

    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(SERVER_ADDRESS)
            .addConverterFactory(GsonConverterFactory.create())
            .build();
    private DeviceService deviceService = retrofit.create(DeviceService.class);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_list);
        devicesListView = findViewById(R.id.deviceListView);

        addDeviceButton = findViewById(R.id.addDeviceButtonList);
        addDeviceButton.setOnClickListener(v -> {
            Intent intent = new Intent(getApplicationContext(), AddDeviceActivity.class);
            getApplicationContext().startActivity(intent);
        });
    }


    private void downloadDeviceList() {
        Call<List<Device>> productCall = deviceService.getAllDevices();
        ProgressDialog mDialog = new ProgressDialog(DeviceListActivity.this);
        mDialog.setMessage("Please wait...");
        mDialog.setCancelable(false);
        mDialog.show();

        productCall.enqueue(new Callback<List<Device>>() {
            @Override
            public void onResponse(Call<List<Device>> call, Response<List<Device>> response) {
                if (response.code() == HttpsURLConnection.HTTP_OK) {

                    List<Device> products = response.body();
                    if (products != null && !products.isEmpty()) {
                        DeviceListAdapter deviceListAdapter = new DeviceListAdapter(getApplicationContext(), R.layout.activity_list_view_devices, products);
                        devicesListView.setAdapter(deviceListAdapter);
                    } else {
                        Toast.makeText(DeviceListActivity.this, "List is empty!", Toast.LENGTH_LONG).show();
                    }
                } else {
                    Toast.makeText(DeviceListActivity.this, COULD_NOT_RETRIEVE_LIST, Toast.LENGTH_LONG).show();
                    Log.i(TAG, COULD_NOT_RETRIEVE_LIST + ": " + response.message());
                }
                mDialog.cancel();
            }

            @Override
            public void onFailure(@NonNull Call<List<Device>> call, @NonNull Throwable t) {
                mDialog.cancel();
                Log.e(TAG, t.getMessage(), t);
                Toast.makeText(DeviceListActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (!isListLoaded) {
            downloadDeviceList();
            isListLoaded = true;
        }
    }
}
