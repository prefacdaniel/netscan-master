package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.exception.IncompleteRequestException;
import com.example.dprefac.barcodescanner.model.Product;
import com.example.dprefac.barcodescanner.service.ProductService;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.dprefac.barcodescanner.MainActivity.HOST_URL;
import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;

public class NewProductActivity extends AppCompatActivity {


    private static final String TAG = NewProductActivity.class.getName();
    public static final String PRODUCT_ADDED = "Product added!";
    public static final String PRODUCT_COULD_NOT_BE_ADDED = "Product couldn't be added!";

    private TextView newBarcodeLabel;
    private EditText newNameLabel;
    private EditText newQuantityLabel;

    private Product product = new Product();

    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(HOST_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();
    ProductService productService = retrofit.create(ProductService.class);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_product);

        initElements();

        Intent intent = getIntent();
        product.setBarcode(intent.getStringExtra("barcode"));
        newBarcodeLabel.setText(product.getBarcode());
    }

    private void initElements() {
        newBarcodeLabel = findViewById(R.id.newBarcodeLabel);
        newNameLabel = findViewById(R.id.newNameLabel);
        newQuantityLabel = findViewById(R.id.newQuantityInput);
    }

    public void addNewProduct(View view) {

        try {
            String productName = newNameLabel.getText().toString();
            String quantityString = newQuantityLabel.getText().toString();

            if (productName.isEmpty()) {
                throw new IncompleteRequestException("Name field can't be empty!");
            }
            if (quantityString.isEmpty()) {
                throw new IncompleteRequestException("Quantity field can't be empty!");
            }

            int quantity = Integer.parseInt(quantityString);
            if(quantity < 0){
                throw new IncompleteRequestException("Quantity can't be a negative value!");
            }

            product.setName(productName);
            product.setQuantity(quantity);

            ProgressDialog mDialog = new ProgressDialog(NewProductActivity.this);
            mDialog.setMessage("Please wait...");
            mDialog.setCancelable(false);
            mDialog.show();

            Call<Void> newProductCall = productService.addNewProduct(product);
            newProductCall.enqueue(new Callback<Void>() {
                @Override
                public void onResponse(Call<Void> call, Response<Void> response) {
                    if (response.code() == HttpsURLConnection.HTTP_OK) {
                        Toast.makeText(NewProductActivity.this, PRODUCT_ADDED, Toast.LENGTH_LONG).show();
                        Log.i(TAG, PRODUCT_ADDED);
                    } else {
                        Toast.makeText(NewProductActivity.this, PRODUCT_COULD_NOT_BE_ADDED, Toast.LENGTH_LONG).show();
                        Log.i(TAG, PRODUCT_COULD_NOT_BE_ADDED + ": " + response.message());
                    }
                    mDialog.cancel();
                    NewProductActivity.this.finish();
                }

                @Override
                public void onFailure(Call<Void> call, Throwable t) {
                    mDialog.cancel();
                    Log.e(TAG, t.getMessage(), t);
                    Toast.makeText(NewProductActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
                }
            });


        } catch (IncompleteRequestException e) {
            Toast.makeText(NewProductActivity.this, e.getMessage(), Toast.LENGTH_LONG).show();
        } catch (NumberFormatException e) {
            Toast.makeText(NewProductActivity.this, "Quantity must be a number!", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            Toast.makeText(NewProductActivity.this, "Error occurred!", Toast.LENGTH_SHORT).show();
            Log.e(TAG, e.getMessage(), e);
        }


    }
}
