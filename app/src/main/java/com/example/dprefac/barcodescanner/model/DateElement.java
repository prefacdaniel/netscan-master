package com.example.dprefac.barcodescanner.model;

import android.support.annotation.NonNull;

/**
 * Created by dprefac on 20-Jun-19.
 */

public class DateElement implements Comparable<DateElement> {
    private String dateString;
    private int attacksNumber;

    public String getDateString() {
        return dateString;
    }

    public void setDateString(String dateString) {
        this.dateString = dateString;
    }

    public int getAttacksNumber() {
        return attacksNumber;
    }

    public void setAttacksNumber(int attacksNumber) {
        this.attacksNumber = attacksNumber;
    }

    @Override
    public int compareTo(@NonNull DateElement that) {
        if (this == that) return 0;

        if (this.dateString == null) {
            return -1;
        }

        if (that.dateString == null) {
            return 1;
        }

        String[] thisSplicedDate = this.dateString.split("/");
        String[] thatSplicedDate = that.dateString.split("/");

        if (Integer.parseInt(thisSplicedDate[2]) < Integer.parseInt(thatSplicedDate[2])) {
            return -1;
        } else if (Integer.parseInt(thisSplicedDate[2]) > Integer.parseInt(thatSplicedDate[2])) {
            return 1;
        }

        if (Integer.parseInt(thisSplicedDate[1]) < Integer.parseInt(thatSplicedDate[1])) {
            return -1;
        } else if (Integer.parseInt(thisSplicedDate[1]) > Integer.parseInt(thatSplicedDate[1])) {
            return 1;
        }

        if (Integer.parseInt(thisSplicedDate[0]) < Integer.parseInt(thatSplicedDate[0])) {
            return -1;
        } else if (Integer.parseInt(thisSplicedDate[0]) > Integer.parseInt(thatSplicedDate[0])) {
            return 1;
        }

        return 0;
    }
}
