package com.example.dprefac.barcodescanner.model;

import com.google.gson.annotations.SerializedName;

/**
 * Created by dprefac on 21-Jun-19.
 */

public enum ConnectionStatus {
    @SerializedName("NORMAL")NORMAL("NORMAL"),
    @SerializedName("INCERT")INCERT("INCERT"),
    @SerializedName("ATTACK")ATTACK("ATTACK");
    private String field;

    ConnectionStatus(String field) {
        this.field = field;
    }

    public String getField() {
        return field;
    }
}
