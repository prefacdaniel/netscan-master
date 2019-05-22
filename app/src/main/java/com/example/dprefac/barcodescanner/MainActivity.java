package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.model.Product;
import com.example.dprefac.barcodescanner.service.ProductService;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import java.util.List;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;

public class MainActivity extends AppCompatActivity {


    private static final String TAG = MainActivity.class.getName();
    public static final String INTERN_SERVER_ERROR = "Intern server error!";
    public static String HOST_URL = "http://192.168.43.96:5000";

    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(HOST_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();
    ProductService productService = retrofit.create(ProductService.class);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void scanBarecode(View view) {
        new IntentIntegrator(this).initiateScan();
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        if (result != null) {
            if (result.getContents() == null) {
                Toast.makeText(this, "Cancelled", Toast.LENGTH_LONG).show();
            } else {
                final String barcode = result.getContents();

                ProgressDialog mDialog = new ProgressDialog(MainActivity.this);
                mDialog.setMessage("Please wait...");
                mDialog.setCancelable(false);
                mDialog.show();

                Call<Product> productCall = productService.getProductByBarcode(barcode);
                productCall.enqueue(new Callback<Product>() {
                    @Override
                    public void onResponse(Call<Product> call, Response<Product> response) {

                        if (response.code() == HttpsURLConnection.HTTP_OK) {
                            Product product = response.body();
                            Log.i(TAG, "Call done!");
                            if (product != null && product.getId() != -1) {
                                Log.i(TAG, "Product NOT null!");
                                Intent intent = new Intent(MainActivity.this, ProductDetailsActivity.class);
                                intent.putExtra("id", product.getId());
                                intent.putExtra("name", product.getName());
                                intent.putExtra("quantity", product.getQuantity());
                                intent.putExtra("barcode", product.getBarcode());
                                startActivity(intent);
                            } else {
                                Log.i(TAG, "Product  null!");
                                Intent intent = new Intent(MainActivity.this, NewProductActivity.class);
                                intent.putExtra("barcode", barcode);
                                startActivity(intent);
                            }
                        } else {
                            Toast.makeText(MainActivity.this, INTERN_SERVER_ERROR, Toast.LENGTH_LONG).show();
                            Log.i(TAG, INTERN_SERVER_ERROR + ": " + response.message());
                        }

                        mDialog.cancel();
                    }

                    @Override
                    public void onFailure(Call<Product> call, Throwable t) {
                        mDialog.cancel();
                        Log.e(TAG, t.getMessage(), t);
                        Toast.makeText(MainActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
                    }
                });
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    public void listAllProducts(View view) {
        Intent intent = new Intent(MainActivity.this,ProductListActivity.class);
        startActivity(intent);
    }

    public void startSettings(View view) {
        Intent intent = new Intent(MainActivity.this,SettingsActivity.class);
        startActivity(intent);
    }
}
