package com.example.dprefac.barcodescanner;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ListView;

import com.example.dprefac.barcodescanner.adapter.DateListAdapter;
import com.example.dprefac.barcodescanner.model.DateElement;

import java.util.ArrayList;
import java.util.List;

public class DeviceDetailActivity extends AppCompatActivity {

    private ListView dateListView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_detail);

        DateElement dateElement1 = new DateElement();
        dateElement1.setDateString("5/5/2019");
        dateElement1.setAttacksNumber(32);
        DateElement dateElement2 = new DateElement();
        dateElement2.setDateString("6/5/2019");
        dateElement2.setAttacksNumber(32);
        DateElement dateElement3 = new DateElement();
        dateElement3.setDateString("17/6/2019");
        dateElement3.setAttacksNumber(32);
        DateElement dateElement4 = new DateElement();
        dateElement4.setDateString("18/6/2019");
        dateElement4.setAttacksNumber(32);


        List<DateElement> dateElementList = new ArrayList<>();
        dateElementList.add(dateElement1);
        dateElementList.add(dateElement2);
        dateElementList.add(dateElement3);
        dateElementList.add(dateElement3);
        dateElementList.add(dateElement3);
        dateElementList.add(dateElement3);
        dateElementList.add(dateElement3);
        dateElementList.add(dateElement3);
        dateElementList.add(dateElement3);
        dateElementList.add(dateElement4);

        DateListAdapter dateListAdapter = new DateListAdapter(this, R.layout.activity_list_date_view, dateElementList);
        dateListView = findViewById(R.id.dateList);
        dateListView.setAdapter(dateListAdapter);
    }
}
