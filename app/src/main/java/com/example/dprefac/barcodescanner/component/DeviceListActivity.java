package com.example.dprefac.barcodescanner.component;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ListView;

import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.model.Device;

import java.util.ArrayList;
import java.util.List;

import static com.example.dprefac.barcodescanner.model.DeviceStatus.*;

public class DeviceListActivity extends AppCompatActivity {


    private ListView devicesListView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_list);
        devicesListView = findViewById(R.id.deviceListView);

        Device device1 = new Device();
        device1.setId(1);
        device1.setName("Webcam Interior");
        device1.setStatus(CONNECTED);

        Device device2 = new Device();
        device2.setId(2);
        device2.setName("Webcam Exterior");
        device2.setStatus(DISCONNECTED);

        Device device3 = new Device();
        device3.setId(3);
        device3.setName("Smart bulb");
        device3.setStatus(DISCONNECTED);

        List<Device> deviceList = new ArrayList<>();
        deviceList.add(device1);
        deviceList.add(device2);
        deviceList.add(device3);

        DeviceListAdapter deviceListAdapter = new DeviceListAdapter(this,R.layout.activity_list_view_devices,deviceList);
        devicesListView.setAdapter(deviceListAdapter);
    }
}
