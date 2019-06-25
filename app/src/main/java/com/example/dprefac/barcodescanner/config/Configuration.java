package com.example.dprefac.barcodescanner.config;

import com.example.dprefac.barcodescanner.service.DeviceService;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by dprefac on 23-Jun-19.
 */

public class Configuration {
    public static String SERVER_ADDRESS = "http://192.168.43.28:5000";

   private static Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(SERVER_ADDRESS)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    public static DeviceService deviceService = retrofit.create(DeviceService.class);
}
