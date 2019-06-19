package com.example.dprefac.barcodescanner.component;

import com.example.dprefac.barcodescanner.dto.Feature;

import java.util.List;

/**
 * Created by dprefac on 22-May-19.
 */

public class ListViewItemDTO {

    private boolean checked = false;
    private List<Feature> featureList;
    private String ip;

    public ListViewItemDTO(boolean checked, List<Feature> featureList, String ip) {
        this.checked = checked;
        this.featureList = featureList;
        this.ip = ip;
    }

    public boolean isChecked() {
        return checked;
    }

    public void setChecked(boolean checked) {
        this.checked = checked;
    }

    public List<Feature> getFeatureList() {
        return featureList;
    }

    public void setFeatureList(List<Feature> featureList) {
        this.featureList = featureList;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }
}