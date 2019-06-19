package com.example.dprefac.barcodescanner.component;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.model.DeviceStatus;

import java.util.List;

import static com.example.dprefac.barcodescanner.model.DeviceStatus.CONNECTED;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class DeviceListAdapter extends ArrayAdapter<Device> {

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

        if (v == null) {
            LayoutInflater vi;
            vi = LayoutInflater.from(mContext);
            v = vi.inflate(resourceLayout, null);
        }

        Device device = getItem(position);

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

        }

        return v;
    }
}
