package com.example.dprefac.barcodescanner.service;

import com.example.dprefac.barcodescanner.model.Device;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;

/**
 * Created by dprefac on 23-Jun-19.
 */

public interface DeviceService {

    @GET("/servers")
    Call<List<Device>> getAllDevices();
}
