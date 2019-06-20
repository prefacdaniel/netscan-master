package com.example.dprefac.barcodescanner.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;
import android.widget.ToggleButton;

import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.model.ConnectionStatus;
import com.example.dprefac.barcodescanner.model.RecordedConnection;

import java.util.List;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class HourListAdapter extends ArrayAdapter<RecordedConnection> {
    private int resourceLayout;
    private Context mContext;

    public HourListAdapter(Context context, int resource, List<RecordedConnection> items) {
        super(context, resource, items);
        this.resourceLayout = resource;
        this.mContext = context;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {

        View view = convertView;

        if (view == null) {
            LayoutInflater vi;
            vi = LayoutInflater.from(mContext);
            view = vi.inflate(resourceLayout, null);
        }


        RecordedConnection recordedConnection = getItem(position);

        if (recordedConnection != null) {
            TextView hourField = view.findViewById(R.id.hourString);

            if (hourField != null) {
                hourField.setText(recordedConnection.getHour() + ":" + recordedConnection.getMinute());
            }
            ToggleButton attackButton = view.findViewById(R.id.attackButton);
            ToggleButton incertButton = view.findViewById(R.id.incertButton);
            ToggleButton normalButton = view.findViewById(R.id.normalButton);
            Button resetButton = view.findViewById(R.id.resetButton);

            attackButton.setOnClickListener(viewButton -> {
                attackButton.setChecked(true);
                incertButton.setChecked(false);
                normalButton.setChecked(false);
                recordedConnection.setConnectionStatus(ConnectionStatus.ATTACK);
                resetButton.setEnabled(true);
            });

            incertButton.setOnClickListener(viewButton -> {
                attackButton.setChecked(false);
                incertButton.setChecked(true);
                normalButton.setChecked(false);
                recordedConnection.setConnectionStatus(ConnectionStatus.INCERT);
                resetButton.setEnabled(true);
            });

            normalButton.setOnClickListener(viewButton -> {
                attackButton.setChecked(false);
                incertButton.setChecked(false);
                normalButton.setChecked(true);
                recordedConnection.setConnectionStatus(ConnectionStatus.NORMAL);
                resetButton.setEnabled(true);
            });

            resetButton.setOnClickListener(v -> {
                recordedConnection.setConnectionStatus( recordedConnection.getInitialConnectionStatus());
                resetButton.setEnabled(false);
                updateButtons(recordedConnection, attackButton, incertButton, normalButton);
            });

            updateButtons(recordedConnection, attackButton, incertButton, normalButton);
        }
        return view;
    }

    private void updateButtons(RecordedConnection recordedConnection, ToggleButton attackButton, ToggleButton incertButton, ToggleButton normalButton) {
        switch (recordedConnection.getConnectionStatus()) {
            case NORMAL:
                attackButton.setChecked(false);
                incertButton.setChecked(false);
                normalButton.setChecked(true);
                break;
            case INCERT:
                attackButton.setChecked(false);
                incertButton.setChecked(true);
                normalButton.setChecked(false);
                break;
            case ATTACK:
                attackButton.setChecked(true);
                incertButton.setChecked(false);
                normalButton.setChecked(false);
                break;
        }
    }
}
