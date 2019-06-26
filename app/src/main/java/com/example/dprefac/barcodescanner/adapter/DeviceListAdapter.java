package com.example.dprefac.barcodescanner.adapter;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.DeviceDetailActivity;
import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.model.DeviceStatus;
import com.example.dprefac.barcodescanner.util.Utils;

import java.util.List;

import static com.example.dprefac.barcodescanner.model.DeviceStatus.CONNECTED;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class DeviceListAdapter extends ArrayAdapter<Device> {
    private final String TAG = this.getClass().getName();

    private int resourceLayout;
    private Context mContext;

    public DeviceListAdapter(Context context, int resource, List<Device> items) {
        super(context, resource, items);
        this.resourceLayout = resource;
        this.mContext = context;
    }


    @Override
    public View getView(int position, View convertView, ViewGroup parent) {

        View v = convertView;

        try {
            Device device = getItem(position);

            if (v == null) {
                LayoutInflater vi;
                vi = LayoutInflater.from(mContext);
                v = vi.inflate(resourceLayout, null);
                v.setOnClickListener(v1 -> {
                    if (device != null) {
                        Intent intent = new Intent(mContext, DeviceDetailActivity.class);
                        intent.putExtra("DEVICE_ID", device.getId());
                        intent.putExtra("DEVICE_NAME", device.getName());
                        intent.putExtra("DEVICE_IMAGE", device.getImage());
                        mContext.startActivity(intent);
                    } else {
                        Toast.makeText(getContext(), "Device not found !!", Toast.LENGTH_LONG).show();
                    }
                });
            }

            if (device != null) {
                TextView deviceNameTextView = v.findViewById(R.id.list_view_device_name);
                TextView deviceStatus = v.findViewById(R.id.list_view_device_status);

                if (deviceNameTextView != null) {
                    deviceNameTextView.setText(device.getName());
                }

                if (deviceStatus != null) {
                    DeviceStatus deviceStatusString = device.getStatus();
                    deviceStatus.setText(deviceStatusString.getField());

                    if (CONNECTED.equals(deviceStatusString)) {
                        deviceStatus.setTextColor(Color.GREEN);
                    } else {
                        deviceStatus.setTextColor(Color.RED);
                    }
                }
                ImageView imageView = v.findViewById(R.id.deviceSmallImage);

                imageView.setImageBitmap(Utils.base64StringToBitmap(device.getImage()));
            }
        } catch (Exception e) {
            Toast.makeText(getContext(), e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }
        return v;
    }
}
