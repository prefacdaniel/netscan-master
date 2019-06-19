package com.example.dprefac.barcodescanner.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.model.DateElement;

import java.util.List;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class DateListAdapter extends ArrayAdapter<DateElement> {

    private int resourceLayout;
    private Context mContext;

    public DateListAdapter(Context context, int resource, List<DateElement> items) {
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

        DateElement dateElement = getItem(position);

        if (dateElement != null) {
            TextView dateStringView = v.findViewById(R.id.dateString);
            TextView attacksNumberView = v.findViewById(R.id.attacksNumber);

            if (dateStringView != null) {
                dateStringView.setText(dateElement.getDateString());
            }
            if (attacksNumberView != null) {
                attacksNumberView.setText(dateElement.getAttacksNumber() + " attacks!");
            }
        }
        return v;
    }

}
