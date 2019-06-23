package com.example.dprefac.barcodescanner.model;

import com.google.gson.annotations.SerializedName;

/**
 * Created by dprefac on 20-Jun-19.
 */

public enum Country {

    @SerializedName("lc")LOCAL("lc"),
    @SerializedName("ro")ROMANIA("RO"),
    @SerializedName("ru")RUSSIA("RU"),
    @SerializedName("cn")CHINA("CN");


    Country(String field) {
        this.field = field;
    }

    private String field;

    public String getField() {
        return field;
    }
}
