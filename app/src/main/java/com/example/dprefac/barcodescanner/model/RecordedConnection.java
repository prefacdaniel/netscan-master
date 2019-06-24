package com.example.dprefac.barcodescanner.model;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class RecordedConnection {
    private String id;
    private Country country;
    private ConnectionStatus connectionStatusFromUser;
    private ConnectionStatus connectionStatusFromAlgorithm;
    private String time;


    public Country getCountry() {
        return country;
    }

    public void setCountry(Country country) {
        this.country = country;
    }

    public ConnectionStatus getConnectionStatusFromUser() {
        return connectionStatusFromUser;
    }

    public void setConnectionStatusFromUser(ConnectionStatus connectionStatusFromUser) {
        this.connectionStatusFromUser = connectionStatusFromUser;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public ConnectionStatus getConnectionStatusFromAlgorithm() {
        return connectionStatusFromAlgorithm;
    }

    public void setConnectionStatusFromAlgorithm(ConnectionStatus connectionStatusFromAlgorithm) {
        this.connectionStatusFromAlgorithm = connectionStatusFromAlgorithm;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}