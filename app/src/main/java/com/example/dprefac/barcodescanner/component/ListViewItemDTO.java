package com.example.dprefac.barcodescanner.component;

import com.example.dprefac.barcodescanner.dto.Feature;

/**
 * Created by dprefac on 22-May-19.
 */

public class ListViewItemDTO {

    private boolean checked = false;

    private Feature itemText;

    public boolean isChecked() {
        return checked;
    }

    public void setChecked(boolean checked) {
        this.checked = checked;
    }

    public Feature getItemText() {
        return itemText;
    }

    public void setItemText(Feature itemText) {
        this.itemText = itemText;
    }
}