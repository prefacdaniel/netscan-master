package com.example.dprefac.barcodescanner;

import android.app.ProgressDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.model.Product;
import com.example.dprefac.barcodescanner.service.ProductService;

import java.util.List;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.dprefac.barcodescanner.MainActivity.HOST_URL;
import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;

public class ProductListActivity extends AppCompatActivity {


    private static final String TAG = ProductListActivity.class.getName();

    public static final String COULD_NOT_RETRIEVE_LIST = "Could not retrieve list!";

    private ListView productList;

    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(HOST_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();
    ProductService productService = retrofit.create(ProductService.class);
    private boolean isListLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_list);

        productList = findViewById(R.id.productList);


    }

    @Override
    protected void onResume() {
        super.onResume();
        if (!isListLoaded) {
            downloadProductList();
            isListLoaded = true;
        }
    }

    private void downloadProductList() {
        Call<List<Product>> productCall = productService.getAllProducts();
        ProgressDialog mDialog = new ProgressDialog(ProductListActivity.this);
        mDialog.setMessage("Please wait...");
        mDialog.setCancelable(false);
        mDialog.show();

        productCall.enqueue(new Callback<List<Product>>() {
            @Override
            public void onResponse(Call<List<Product>> call, Response<List<Product>> response) {
                if (response.code() == HttpsURLConnection.HTTP_OK) {

                    List<Product> products = response.body();
                    if (!products.isEmpty()) {

                        ArrayAdapter adapter = new ArrayAdapter(ProductListActivity.this, android.R.layout.simple_list_item_2, android.R.id.text1, response.body()) {
                            @Override
                            public View getView(int position, View convertView, ViewGroup parent) {
                                View view = super.getView(position, convertView, parent);
                                TextView text1 = (TextView) view.findViewById(android.R.id.text1);
                                TextView text2 = (TextView) view.findViewById(android.R.id.text2);

                                text1.setText(products.get(position).getName());
                                text2.setText("Q: " + products.get(position).getQuantity());
                                return view;
                            }
                        };

                        productList.setAdapter(adapter);
                    } else {
                        Toast.makeText(ProductListActivity.this, "List is empty!", Toast.LENGTH_LONG).show();
                    }

                } else {
                    Toast.makeText(ProductListActivity.this, COULD_NOT_RETRIEVE_LIST, Toast.LENGTH_LONG).show();
                    Log.i(TAG, COULD_NOT_RETRIEVE_LIST + ": " + response.message());
                }
                mDialog.cancel();
            }

            @Override
            public void onFailure(Call<List<Product>> call, Throwable t) {
                mDialog.cancel();
                Log.e(TAG, t.getMessage(), t);
                Toast.makeText(ProductListActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
            }
        });
    }
}
