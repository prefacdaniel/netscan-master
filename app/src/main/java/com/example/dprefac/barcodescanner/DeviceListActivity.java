package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.adapter.DeviceListAdapter;
import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.model.Product;
import com.example.dprefac.barcodescanner.service.DeviceService;

import java.util.ArrayList;
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
import static com.example.dprefac.barcodescanner.model.DeviceStatus.CONNECTED;
import static com.example.dprefac.barcodescanner.model.DeviceStatus.DISCONNECTED;

public class DeviceListActivity extends AppCompatActivity {

    private ListView devicesListView;
    private Button addDeviceButton;
    private DeviceService deviceService;

    private static final String TAG = DeviceListActivity.class.getName();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_list);
        devicesListView = findViewById(R.id.deviceListView);

//        Device device1 = new Device();
//        device1.setId(1);
//        device1.setName("Webcam Interior");
//        device1.setStatus(CONNECTED);
//
//        Device device2 = new Device();
//        device2.setId(2);
//        device2.setName("Webcam Exterior");
//        device2.setStatus(DISCONNECTED);
//
//        Device device3 = new Device();
//        device3.setId(3);
//        device3.setName("Smart bulb");
//        device3.setStatus(DISCONNECTED);
//
//        List<Device> deviceList = new ArrayList<>();
//        deviceList.add(device1);
//        deviceList.add(device2);
//        deviceList.add(device3);

//        DeviceListAdapter deviceListAdapter = new DeviceListAdapter(this, R.layout.activity_list_view_devices, deviceList);
//        devicesListView.setAdapter(deviceListAdapter);

        addDeviceButton = findViewById(R.id.addDeviceButtonList);
        addDeviceButton.setOnClickListener(v -> {
            Intent intent = new Intent(getApplicationContext(), AddDeviceActivity.class);
            getApplicationContext().startActivity(intent);
        });

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(SERVER_ADDRESS)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        deviceService = retrofit.create(DeviceService.class);
        downloadDeviceList();
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
            public void onFailure(Call<List<Device>> call, Throwable t) {
                mDialog.cancel();
                Log.e(TAG, t.getMessage(), t);
                Toast.makeText(DeviceListActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
            }
        });
    }
}
