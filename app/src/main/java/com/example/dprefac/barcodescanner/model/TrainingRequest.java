package com.example.dprefac.barcodescanner.model;

/**
 * Created by dprefac on 29-Jun-19.
 */

public class TrainingRequest {
    private int deviceId;
    private boolean use_unknown_status_data = false;

    public boolean isUse_unknown_status_data() {
        return use_unknown_status_data;
    }

    public void setUse_unknown_status_data(boolean use_unknown_status_data) {
        this.use_unknown_status_data = use_unknown_status_data;
    }

    public int getDeviceId() {
        return deviceId;
    }

    public void setDeviceId(int deviceId) {
        this.deviceId = deviceId;
    }

    @Override
    public String toString() {
        return "TrainingRequest{" +
                "deviceId=" + deviceId +
                ", use_unknown_status_data=" + use_unknown_status_data +
                '}';
    }
}

