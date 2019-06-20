package com.example.dprefac.barcodescanner.model;

/**
 * Created by dprefac on 20-Jun-19.
 */

public enum Country {

    ROMANIA("RO"),
    RUSSIA("RU"),
    CHINA("CN");


    Country(String field) {
        this.field = field;
    }

    private String field;

    public String getField() {
        return field;
    }
}
