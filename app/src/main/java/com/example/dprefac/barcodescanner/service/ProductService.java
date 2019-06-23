package com.example.dprefac.barcodescanner.service;

import com.example.dprefac.barcodescanner.model.Feature;
import com.example.dprefac.barcodescanner.model.Product;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

/**
 * Created by dprefac on 04-Feb-19.
 */

public interface ProductService {


    @GET("get/{barcode}")
    Call<Product> getProductByBarcode(@Path("barcode") String barcode);

    @POST("/add")
    Call<Void> addNewProduct(@Body Product product);

    @DELETE("/delete/{barcode}")
    Call<Void> deleteProduct(@Path("barcode") String barcode);

    @PUT("/update")
    Call<Void> updateProductQuantity(@Body Product product);

    @GET("/products")
    Call<List<Product>> getAllProducts();

    @GET("/feature")
    Call<List<Feature>> getAllFeature();
}
