package com.example.dprefac.barcodescanner.model;

/**
 * Created by dprefac on 20-Jun-19.
 */

public enum DeviceStatus {

    CONNECTED("Connected"),
    DISCONNECTED("Disconnected");


    private String field;

    DeviceStatus(String field) {
        this.field = field;
    }

    public String getField() {
        return field;
    }
}
