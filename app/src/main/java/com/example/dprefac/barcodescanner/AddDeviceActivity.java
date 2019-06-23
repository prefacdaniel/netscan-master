package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.exception.IncompleteRequestException;
import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.model.DeviceStatus;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;
import static com.example.dprefac.barcodescanner.config.Configuration.deviceService;

public class AddDeviceActivity extends AppCompatActivity {

    private static final String TAG = AddDeviceActivity.class.getName();

    private final String DEVICE_ADDED = "Device added!";
    private final String DEVICE_COULD_NOT_BE_ADDED = "Device could not be added!";

    private ImageButton imageButton;
    private EditText deviceName;
    private EditText ipField;
    private EditText port;
    private Button saveDevice;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_device);

        imageButton = findViewById(R.id.addImageButton);
        deviceName = findViewById(R.id.deviceNameAddDevice);
        ipField = findViewById(R.id.ipFieldAddDevice);
        port = findViewById(R.id.portFieldAddDevice);
        saveDevice = findViewById(R.id.saveDevice);

        saveDevice.setOnClickListener(v -> {
            String deviceNameString = deviceName.getText().toString();
            String ipFiedString = ipField.getText().toString();
            String portNumberString = port.getText().toString();

            if (deviceNameString.isEmpty() || ipFiedString.isEmpty() || portNumberString.isEmpty()) {
                Toast.makeText(getApplicationContext(), "All fields are mandatory!", Toast.LENGTH_LONG).show();
            } else {
                try {
                    int portNumber = Integer.parseInt(portNumberString);

                    Device device = new Device();
                    device.setIp(ipFiedString);
                    device.setPort(portNumber);
                    device.setName(deviceNameString);
                    device.setStatus(DeviceStatus.DISCONNECTED);
                    device.setImage("base64img");//TODO - add real image

                    sendDeviceToDatabase(device);
                } catch (Exception e) {
                    Log.e(TAG, e.getMessage(), e);
                    Toast.makeText(getApplicationContext(), "Wrong input data!", Toast.LENGTH_LONG).show();
                }
            }
        });
    }


    public void sendDeviceToDatabase(Device device) {

        try {

            ProgressDialog mDialog = new ProgressDialog(AddDeviceActivity.this);
            mDialog.setMessage("Please wait...");
            mDialog.setCancelable(false);
            mDialog.show();

            Call<Void> newProductCall = deviceService.addNewDevice(device);
            newProductCall.enqueue(new Callback<Void>() {
                @Override
                public void onResponse(Call<Void> call, Response<Void> response) {
                    if (response.code() == HttpsURLConnection.HTTP_OK) {
                        Toast.makeText(AddDeviceActivity.this, DEVICE_ADDED, Toast.LENGTH_LONG).show();
                        Log.i(TAG, DEVICE_ADDED);
                    } else {
                        Toast.makeText(AddDeviceActivity.this, DEVICE_COULD_NOT_BE_ADDED, Toast.LENGTH_LONG).show();
                        Log.i(TAG, DEVICE_COULD_NOT_BE_ADDED + ": " + response.message());
                    }
                    mDialog.cancel();
                    AddDeviceActivity.this.finish();
                }

                @Override
                public void onFailure(Call<Void> call, Throwable t) {
                    mDialog.cancel();
                    Log.e(TAG, t.getMessage(), t);
                    Toast.makeText(AddDeviceActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
                }
            });
        } catch (Exception e) {
            Toast.makeText(AddDeviceActivity.this, "Error occurred!", Toast.LENGTH_SHORT).show();
            Log.e(TAG, e.getMessage(), e);
        }


    }
}
