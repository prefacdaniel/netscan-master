package com.example.dprefac.barcodescanner.exception;

/**
 * Created by dprefac on 04-Feb-19.
 */

public class IncompleteRequestException extends Exception {

    public IncompleteRequestException() {
    }

    public IncompleteRequestException(String message) {
        super(message);
    }

    public IncompleteRequestException(String message, Throwable cause) {
        super(message, cause);
    }

    public IncompleteRequestException(Throwable cause) {
        super(cause);
    }

    public IncompleteRequestException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }
}
