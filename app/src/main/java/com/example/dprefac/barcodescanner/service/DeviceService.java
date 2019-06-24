package com.example.dprefac.barcodescanner.service;

import com.example.dprefac.barcodescanner.model.DateElement;
import com.example.dprefac.barcodescanner.model.Device;
import com.example.dprefac.barcodescanner.model.RecordedConnection;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

/**
 * Created by dprefac on 23-Jun-19.
 */

public interface DeviceService {

    @GET("/servers")
    Call<List<Device>> getAllDevices();

    @POST("/server")
    Call<Void> addNewDevice(@Body Device device);

    @GET("/date/{deviceId}")
    Call<List<DateElement>> getDatesForDevice(@Path("deviceId") int device);

    @GET("/connections/{deviceId}/{date}")
    Call<List<RecordedConnection>> getDailyActivityForADevice(@Path("deviceId") int device, @Path("date") String date);

    @POST("/statusupdate")
    Call<Void> updateConnectionStatus(@Body List<RecordedConnection> recordedConnectionList);
}
