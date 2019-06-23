package com.example.dprefac.barcodescanner.component;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.CheckBox;
import android.widget.ListView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.model.Feature;
import com.example.dprefac.barcodescanner.service.ProductService;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import javax.net.ssl.HttpsURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.example.dprefac.barcodescanner.MainActivity.INTERN_SERVER_ERROR;
import static com.example.dprefac.barcodescanner.ProductDetailsActivity.OPERATION_FAILED_CHECK_CONNECTION;

/**
 * Created by dprefac on 22-May-19.
 */

public class ListViewWithCheckboxActivity extends AppCompatActivity {


    private static final String TAG = ListViewWithCheckboxActivity.class.getName();
    public static String HOST_URL = "http://192.168.43.96:5000";

    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(HOST_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();
    ProductService productService = retrofit.create(ProductService.class);

    final ArrayList<ListViewItemDTO> initItemList = new ArrayList<>();
    ListViewItemCheckboxBaseAdapter listViewDataAdapter;
    private boolean isDataLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list_view_with_checkbox);

        listViewDataAdapter = new ListViewItemCheckboxBaseAdapter(getApplicationContext(), initItemList);

        // Get listview checkbox.
        final ListView listViewWithCheckbox = (ListView) findViewById(R.id.list_view_with_checkbox);

        listViewWithCheckbox.setAdapter(listViewDataAdapter);
        listViewWithCheckbox.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int itemIndex, long l) {
                // Get user selected item.
                Object itemObject = adapterView.getAdapter().getItem(itemIndex);

                // Translate the selected item to DTO object.
                ListViewItemDTO itemDto = (ListViewItemDTO) itemObject;

                // Get the checkbox.
                CheckBox itemCheckbox = (CheckBox) view.findViewById(R.id.list_view_item_checkbox);

                // Reverse the checkbox and clicked item check state.
                if (itemDto.isChecked()) {
                    itemCheckbox.setChecked(false);
                    itemDto.setChecked(false);
                } else {
                    itemCheckbox.setChecked(true);
                    itemDto.setChecked(true);
                }

                //Toast.makeText(getApplicationContext(), "select item text : " + itemDto.getFeatureList(), Toast.LENGTH_SHORT).show();
            }
        });

        getFeatureList();
        isDataLoaded = true;
    }


    private void getFeatureList() {

        if(!isDataLoaded) {
            Call<List<Feature>> productCall = productService.getAllFeature();

            productCall.enqueue(new Callback<List<Feature>>() {
                @Override
                public void onResponse(Call<List<Feature>> call, Response<List<Feature>> response) {

                    if (response.code() == HttpsURLConnection.HTTP_OK) {
                        List<Feature> product = response.body();
                        Log.i(TAG, "Call done!");

                        Map<String, List<Feature>> featureMap = new HashMap<>();
                        for (Feature feature : product) {
                            List<Feature> featureList = featureMap.get(feature.getSource()); //TODO change getSource with getIP when changed
                            if (null == featureList) {
                                featureList = new LinkedList<>();
                            }
                            featureList.add(feature);
                            featureMap.put(feature.getSource(), featureList);
                        }
                        for (List<Feature> featureList : featureMap.values()) {
                            ListViewItemDTO dto = new ListViewItemDTO(false, featureList, featureList.get(0).getSource());
                            initItemList.add(dto);
                        }

                        listViewDataAdapter.notifyDataSetChanged();
                    } else {
                        Toast.makeText(ListViewWithCheckboxActivity.this, INTERN_SERVER_ERROR, Toast.LENGTH_LONG).show();
                        Log.i(TAG, INTERN_SERVER_ERROR + ": " + response.message());
                    }

                }

                @Override
                public void onFailure(Call<List<Feature>> call, Throwable t) {

                    Toast.makeText(ListViewWithCheckboxActivity.this, OPERATION_FAILED_CHECK_CONNECTION, Toast.LENGTH_LONG).show();
                }
            });
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        outState.putBoolean("isDataLoaded",isDataLoaded);

        super.onSaveInstanceState(outState);
    }
}