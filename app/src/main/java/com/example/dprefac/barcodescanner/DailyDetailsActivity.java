package com.example.dprefac.barcodescanner;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ListView;

import com.example.dprefac.barcodescanner.adapter.HourListAdapter;
import com.example.dprefac.barcodescanner.model.ConnectionStatus;
import com.example.dprefac.barcodescanner.model.Country;
import com.example.dprefac.barcodescanner.model.RecordedConnection;

import java.util.ArrayList;
import java.util.List;

public class DailyDetailsActivity extends AppCompatActivity {

    private ListView hourListView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_daily_details);


        RecordedConnection recordedConnection1 = new RecordedConnection();
        recordedConnection1.setCountry(Country.ROMANIA);
        recordedConnection1.setConnectionStatus(ConnectionStatus.NORMAL);
        recordedConnection1.setInitialConnectionStatus(ConnectionStatus.NORMAL);
        recordedConnection1.setHour(12);
        recordedConnection1.setMinute(34);

        RecordedConnection recordedConnection2 = new RecordedConnection();
        recordedConnection2.setConnectionStatus(ConnectionStatus.INCERT);
        recordedConnection2.setCountry(Country.RUSSIA);
        recordedConnection2.setInitialConnectionStatus(ConnectionStatus.INCERT);
        recordedConnection2.setHour(12);
        recordedConnection2.setMinute(43);

        RecordedConnection recordedConnection3 = new RecordedConnection();
        recordedConnection3.setConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection3.setCountry(Country.CHINA);
        recordedConnection3.setInitialConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection3.setHour(12);
        recordedConnection3.setMinute(57);


        RecordedConnection recordedConnection4 = new RecordedConnection();
        recordedConnection4.setConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection4.setCountry(Country.CHINA);
        recordedConnection4.setInitialConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection4.setHour(13);
        recordedConnection4.setMinute(10);


        RecordedConnection recordedConnection5 = new RecordedConnection();
        recordedConnection5.setConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection5.setCountry(Country.CHINA);
        recordedConnection5.setInitialConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection5.setHour(13);
        recordedConnection5.setMinute(13);

        RecordedConnection recordedConnection6 = new RecordedConnection();
        recordedConnection6.setConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection6.setCountry(Country.CHINA);
        recordedConnection6.setInitialConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection6.setHour(13);
        recordedConnection6.setMinute(20);

        RecordedConnection recordedConnection7 = new RecordedConnection();
        recordedConnection7.setConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection7.setCountry(Country.CHINA);
        recordedConnection7.setInitialConnectionStatus(ConnectionStatus.ATTACK);
        recordedConnection7.setHour(13);
        recordedConnection7.setMinute(25);

        List<RecordedConnection> recordedConnectionArrayList = new ArrayList<>();
        recordedConnectionArrayList.add(recordedConnection1);
        recordedConnectionArrayList.add(recordedConnection2);
        recordedConnectionArrayList.add(recordedConnection3);
        recordedConnectionArrayList.add(recordedConnection4);
        recordedConnectionArrayList.add(recordedConnection5);
        recordedConnectionArrayList.add(recordedConnection6);
        recordedConnectionArrayList.add(recordedConnection7);


        HourListAdapter hourListAdapter = new HourListAdapter(this, R.layout.activity_list_hour_elements, recordedConnectionArrayList);
        hourListView = findViewById(R.id.hourList);
        hourListView.setAdapter(hourListAdapter);
    }
}
