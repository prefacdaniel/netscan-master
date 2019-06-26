package com.example.dprefac.barcodescanner;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.model.DeviceStatus;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;
import static com.example.dprefac.barcodescanner.config.Configuration.deviceService;

public class AddDeviceActivity extends AppCompatActivity {

    private final String TAG = this.getClass().getName();

    private final String DEVICE_ADDED = "Device added!";
    private final String DEVICE_COULD_NOT_BE_ADDED = "Device could not be added!";

    private ImageButton imageButton;
    private EditText deviceName;
    private EditText ipField;
    private EditText port;
    private Button saveDevice;

    public final static int PICK_PHOTO_FOR_AVATAR = 37;

    private String base64Image;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_device);
        try {
            imageButton = findViewById(R.id.addImageButton);
            deviceName = findViewById(R.id.deviceNameDaily);
            ipField = findViewById(R.id.ipFieldAddDevice);
            port = findViewById(R.id.portFieldAddDevice);
            saveDevice = findViewById(R.id.saveDevice);


            imageButton.setOnClickListener(view -> {
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.setType("image/*");
                startActivityForResult(intent, PICK_PHOTO_FOR_AVATAR);
            });

            saveDevice.setOnClickListener(v -> {
                try {
                    String deviceNameString = deviceName.getText().toString();
                    String ipFieldString = ipField.getText().toString();
                    String portNumberString = port.getText().toString();

                    if (deviceNameString.isEmpty() || ipFieldString.isEmpty() || portNumberString.isEmpty() || base64Image == null || base64Image.isEmpty()) {
                        Toast.makeText(getApplicationContext(), "All fields are mandatory!", Toast.LENGTH_LONG).show();
                    } else {
                        try {
                            int portNumber = Integer.parseInt(portNumberString);

                            Device device = new Device();
                            device.setIp(ipFieldString);
                            device.setPort(portNumber);
                            device.setName(deviceNameString);
                            device.setStatus(DeviceStatus.DISCONNECTED);
                            device.setImage(base64Image);

                            sendDeviceToDatabase(device);
                        } catch (Exception e) {
                            Log.e(TAG, e.getMessage(), e);
                            Toast.makeText(getApplicationContext(), "Wrong input data!", Toast.LENGTH_LONG).show();
                        }
                    }
                } catch (Exception e) {
                    Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
                    Log.e(TAG, e.getMessage(), e);
                }
            });
        } catch (Exception e) {
            Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        try {
            if (requestCode == PICK_PHOTO_FOR_AVATAR && resultCode == Activity.RESULT_OK) {
                if (data == null) {
                    Log.e(TAG, "Data for image is null!");
                } else {
                    try {
                        InputStream inputStream = getApplicationContext().getContentResolver().openInputStream(data.getData());
                        ByteArrayOutputStream result = new ByteArrayOutputStream();
                        byte[] buffer = new byte[1024];
                        int length;
                        while ((length = inputStream.read(buffer)) != -1) {
                            result.write(buffer, 0, length);
                        }
                        final byte[] imageData = result.toByteArray();
                        base64Image = Base64.encodeToString(imageData, Base64.URL_SAFE);
                        Bitmap bitmap = BitmapFactory.decodeByteArray(imageData, 0, imageData.length);
                        imageButton.setImageBitmap(bitmap);
                    } catch (Exception e) {
                        Log.e(TAG, "Error while reading data!");
                    }
                }
            }
        } catch (Exception e) {
            Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }
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
