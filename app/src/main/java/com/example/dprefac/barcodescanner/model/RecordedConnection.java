package com.example.dprefac.barcodescanner.model;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class RecordedConnection {
    private Country country;
    private ConnectionStatus connectionStatus;
    private ConnectionStatus initialConnectionStatus;
    private int hour;
    private int minute;


    public Country getCountry() {
        return country;
    }

    public void setCountry(Country country) {
        this.country = country;
    }

    public ConnectionStatus getConnectionStatus() {
        return connectionStatus;
    }

    public void setConnectionStatus(ConnectionStatus connectionStatus) {
        this.connectionStatus = connectionStatus;
    }

    public int getHour() {
        return hour;
    }

    public void setHour(int hour) {
        this.hour = hour;
    }

    public int getMinute() {
        return minute;
    }

    public void setMinute(int minute) {
        this.minute = minute;
    }

    public ConnectionStatus getInitialConnectionStatus() {
        return initialConnectionStatus;
    }

    public void setInitialConnectionStatus(ConnectionStatus initialConnectionStatus) {
        this.initialConnectionStatus = initialConnectionStatus;
    }
}
