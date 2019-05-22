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

public class ProductDetailsActivity extends AppCompatActivity {

    private static final String TAG = ProductDetailsActivity.class.getName();
    public static final String PRODUCT_DELETED = "Product deleted!";
    public static final String PRODUCT_NOT_DELETED = "Product couldn't be deleted!";
    public static final String OPERATION_FAILED_CHECK_CONNECTION = "Operation failed! Check connection!";
    public static final String FAILED_TO_UPDATED_QUANTITY = "Failed to updated quantity!";
    public static final String QUANTITY_UPDATED = "Quantity updated!";


    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(HOST_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();
    ProductService productService = retrofit.create(ProductService.class);

    private Product product = new Product();

    private TextView barcodeLabel;
    private TextView nameLabel;
    private EditText quantityLabel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_details);

        initElements();
        updateLocalProduct();
        setDataOnElements();


    }

    private void setDataOnElements() {
        barcodeLabel.setText(product.getBarcode());
        nameLabel.setText(product.getName());
        quantityLabel.setText(Integer.toString(product.getQuantity()));
    }

    private void updateLocalProduct() {
        Intent intent = getIntent();
        product.setId(intent.getIntExtra("id", -1));
        product.setBarcode(intent.getStringExtra("barcode"));
        product.setName(intent.getStringExtra("name"));
        product.setQuantity(intent.getIntExtra("quantity", -1));
    }

    private void initElements() {
        barcodeLabel = findViewById(R.id.barcodeLabel);
        nameLabel = findViewById(R.id.nameLabel);
        quantityLabel = findViewById(R.id.quantityInput);
    }

    public void deleteProduct(View view) {
        ProgressDialog mDialog = new ProgressDialog(ProductDetailsActivity.this);
        mDialog.setMessage("Please wait...");
        mDialog.setCancelable(false);
        mDialog.show();

        Call<Void> deleteCall = productService.deleteProduct(product.getBarcode());
        deleteCall.enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                if (response.code() == HttpsURLConnection.HTTP_OK) {
                    Toast.makeText(ProductDetailsActivity.this, PRODUCT_DELETED, Toast.LENGTH_LONG).show();
                    Log.i(TAG, PRODUCT_DELETED);
                } else {
                    Toast.makeText(ProductDetailsActivity.this, PRODUCT_NOT_DELETED, Toast.LENGTH_LONG).show();
                    Log.i(TAG, PRODUCT_NOT_DELETED + ": " + response.message());
                }
                mDialog.cancel();
                finish();
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                mDialog.cancel();
                Log.e(TAG, t.getMessage(), t);
                Toast.makeText(ProductDetailsActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
            }
        });
    }

    public void updateProductQuantity(View view) {
        try {
            String quantityString = quantityLabel.getText().toString();
            if (quantityString.isEmpty()) {
                throw new IncompleteRequestException("Quantity field can't be empty!");
            }
            int quantity = Integer.parseInt(quantityString);
            if(quantity < 0){
                throw new IncompleteRequestException("Quantity can't be a negative value!");
            }
            product.setQuantity(quantity);

            ProgressDialog mDialog = new ProgressDialog(ProductDetailsActivity.this);
            mDialog.setMessage("Please wait...");
            mDialog.setCancelable(false);
            mDialog.show();

            Call<Void> updateCall = productService.updateProductQuantity(product);
            updateCall.enqueue(new Callback<Void>() {
                @Override
                public void onResponse(Call<Void> call, Response<Void> response) {
                    if (response.code() == HttpsURLConnection.HTTP_OK) {
                        Toast.makeText(ProductDetailsActivity.this, QUANTITY_UPDATED, Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(ProductDetailsActivity.this, FAILED_TO_UPDATED_QUANTITY, Toast.LENGTH_LONG).show();
                        Log.i(TAG, FAILED_TO_UPDATED_QUANTITY + ": " + response.message());
                    }
                    mDialog.cancel();
                    ProductDetailsActivity.this.finish();
                }

                @Override
                public void onFailure(Call<Void> call, Throwable t) {
                    mDialog.cancel();
                    Log.e(TAG, t.getMessage(), t);
                    Toast.makeText(ProductDetailsActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
                }
            });

        } catch (IncompleteRequestException e) {
            Toast.makeText(ProductDetailsActivity.this, e.getMessage(), Toast.LENGTH_LONG).show();
        } catch (NumberFormatException e) {
            Toast.makeText(ProductDetailsActivity.this, "Quantity must be a number!", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            Toast.makeText(ProductDetailsActivity.this, "Error occurred!", Toast.LENGTH_SHORT).show();
            Log.e(TAG, e.getMessage(), e);
        }
    }
}
