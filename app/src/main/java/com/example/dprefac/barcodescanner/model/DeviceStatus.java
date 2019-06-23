package com.example.dprefac.barcodescanner.model;

import com.google.gson.annotations.SerializedName;

/**
 * Created by dprefac on 20-Jun-19.
 */

public enum DeviceStatus {

    @SerializedName("Connected")CONNECTED("Connected"),
    @SerializedName("Disconnected")DISCONNECTED("Disconnected");


    private String field;

    DeviceStatus(String field) {
        this.field = field;
    }

    public String getField() {
        return field;
    }
}
