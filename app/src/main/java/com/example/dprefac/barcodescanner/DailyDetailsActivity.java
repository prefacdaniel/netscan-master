package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.adapter.HourListAdapter;
import com.example.dprefac.barcodescanner.model.RecordedConnection;

import java.util.List;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;
import static com.example.dprefac.barcodescanner.ProductListActivity.COULD_NOT_RETRIEVE_LIST;
import static com.example.dprefac.barcodescanner.config.Configuration.deviceService;

public class DailyDetailsActivity extends AppCompatActivity {

    private final String TAG = this.getClass().getName();

    private int deviceId;
    private String deviceName;
    private String deviceImage;
    private String connectionsDate;

    private TextView deviceNameDaily;
    private ImageView deviceIconDaily;
    private TextView deviceDateDaily;
    private ListView hourListView;
    private Button updateConnectionStatusButton;

    private boolean isListLoaded = false;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_daily_details);

        deviceId = getIntent().getIntExtra("DEVICE_ID", -1);
        deviceName = getIntent().getStringExtra("DEVICE_NAME");
        deviceImage = getIntent().getStringExtra("DEVICE_IMAGE");
        connectionsDate = getIntent().getStringExtra("DATE_DATA");


        deviceNameDaily = findViewById(R.id.deviceNameDaily);
        deviceIconDaily = findViewById(R.id.deviceIconDaily);
        deviceDateDaily = findViewById(R.id.deviceDateDaily);
        hourListView = findViewById(R.id.hourList);
        updateConnectionStatusButton = findViewById(R.id.updateConnectionStatusButton);

        deviceNameDaily.setText(deviceName);
//        deviceIconDaily.setImageIcon();//todo
        deviceDateDaily.setText(connectionsDate);

    }


    private void downloadDeviceDailyList() {

        connectionsDate = connectionsDate.replace("/", "_");

        Call<List<RecordedConnection>> productCall = deviceService.getDailyAcitivyForADevice(deviceId, connectionsDate);
        ProgressDialog mDialog = new ProgressDialog(DailyDetailsActivity.this);
        mDialog.setMessage("Please wait...");
        mDialog.setCancelable(false);
        mDialog.show();

        productCall.enqueue(new Callback<List<RecordedConnection>>() {
            @Override
            public void onResponse(Call<List<RecordedConnection>> call, Response<List<RecordedConnection>> response) {
                if (response.code() == HttpsURLConnection.HTTP_OK) {

                    List<RecordedConnection> recordedConnectionList = response.body();
                    if (recordedConnectionList != null && !recordedConnectionList.isEmpty()) {
                        HourListAdapter hourListAdapter = new HourListAdapter(DailyDetailsActivity.this, R.layout.activity_list_hour_elements, recordedConnectionList);
                        hourListView.setAdapter(hourListAdapter);
                    } else {
                        Toast.makeText(DailyDetailsActivity.this, "List is empty!", Toast.LENGTH_LONG).show();
                    }
                } else {
                    Toast.makeText(DailyDetailsActivity.this, COULD_NOT_RETRIEVE_LIST, Toast.LENGTH_LONG).show();
                    Log.i(TAG, COULD_NOT_RETRIEVE_LIST + ": " + response.message());
                }
                mDialog.cancel();
            }

            @Override
            public void onFailure(@NonNull Call<List<RecordedConnection>> call, @NonNull Throwable t) {
                mDialog.cancel();
                Log.e(TAG, t.getMessage(), t);
                Toast.makeText(DailyDetailsActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
            }
        });
    }


    @Override
    protected void onResume() {
        super.onResume();
        if (!isListLoaded) {
            downloadDeviceDailyList();
            isListLoaded = true;
        }
    }
}
