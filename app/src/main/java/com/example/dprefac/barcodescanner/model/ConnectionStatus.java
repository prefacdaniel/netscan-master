package com.example.dprefac.barcodescanner.model;

/**
 * Created by dprefac on 21-Jun-19.
 */

public enum ConnectionStatus {
    NORMAL("NORMAL"),
    INCERT("INCERT"),
    ATTACK("ATTACK");
    private String field;

    ConnectionStatus(String field) {
        this.field = field;
    }

    public String getField() {
        return field;
    }
}
