package com.example.dprefac.barcodescanner.adapter;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.DailyDetailsActivity;
import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.model.DateElement;

import java.util.List;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class DateListAdapter extends ArrayAdapter<DateElement> {
    private final String TAG = this.getClass().getName();
    private int resourceLayout;
    private Context mContext;
    private int deviceId;
    private String deviceName;
    private String deviceImage;

    public DateListAdapter(Context context, int resource, List<DateElement> items, int deviceId, String deviceName, String deviceImage) {
        super(context, resource, items);
        this.resourceLayout = resource;
        this.mContext = context;
        this.deviceId = deviceId;
        this.deviceName = deviceName;
        this.deviceImage = deviceImage;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        DateElement dateElement = getItem(position);

        View v = convertView;

        try {
            if (v == null) {
                LayoutInflater vi;
                vi = LayoutInflater.from(mContext);
                v = vi.inflate(resourceLayout, null);
                v.setOnClickListener(v1 -> {
                    if (dateElement != null) {
                        Intent intent = new Intent(mContext, DailyDetailsActivity.class);
                        intent.putExtra("DEVICE_ID", deviceId);
                        intent.putExtra("DEVICE_NAME", deviceName);
                        intent.putExtra("DEVICE_IMAGE", deviceImage);
                        intent.putExtra("DATE_DATA", dateElement.getDateString());
                        mContext.startActivity(intent);
                    }
                });
            }else{
                Toast.makeText(getContext(),"View cannot be null!", Toast.LENGTH_LONG).show();
            }

            if (dateElement != null) {
                TextView dateStringView = v.findViewById(R.id.dateString);
                TextView attacksNumberView = v.findViewById(R.id.attacksNumber);

                if (dateStringView != null) {
                    dateStringView.setText(dateElement.getDateString());
                }

                ImageView attackImageView = v.findViewById(R.id.attackImageView);

                if (attacksNumberView != null) {
                    int attacksNumber = dateElement.getAttacksNumber();
                    if (attacksNumber > 0) {
                        attacksNumberView.setText(attacksNumber + " attacks!");
                        attacksNumberView.setTextColor(Color.RED);
                        attackImageView.setVisibility(View.VISIBLE);
                    } else {
                        attackImageView.setVisibility(View.INVISIBLE);
                        attacksNumberView.setText("Nothing suspicious");
                        attacksNumberView.setTextColor(Color.BLUE);
                    }
                }
            }else{
                Toast.makeText(getContext(),"dateElement cannot be null!", Toast.LENGTH_LONG).show();
            }
        } catch (Exception e) {
            Toast.makeText(getContext(),e.getMessage(), Toast.LENGTH_LONG).show();
            Log.e(TAG, e.getMessage(), e);
        }

        return v;
    }

}
