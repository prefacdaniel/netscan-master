package com.example.dprefac.barcodescanner.model;

import android.support.annotation.NonNull;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class RecordedConnection implements Comparable<RecordedConnection> {
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

    @Override
    public int compareTo(@NonNull RecordedConnection that) {
        if (this == that) {
            return 0;
        }

        if (this.time == null) {
            return -1;
        }

        if (that.time == null) {
            return 1;
        }

        String[] thisSplicedTime = this.time.split(":");
        String[] thatSplicedTime = that.time.split(":");

        if (Integer.parseInt(thisSplicedTime[0]) < Integer.parseInt(thatSplicedTime[0])) {
            return -1;
        } else if (Integer.parseInt(thisSplicedTime[0]) > Integer.parseInt(thatSplicedTime[0])) {
            return 1;
        }

        if (Integer.parseInt(thisSplicedTime[1]) < Integer.parseInt(thatSplicedTime[1])) {
            return -1;
        } else if (Integer.parseInt(thisSplicedTime[1]) > Integer.parseInt(thatSplicedTime[1])) {
            return 1;
        }

        return 0;
    }
}