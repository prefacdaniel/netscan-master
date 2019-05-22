package com.example.dprefac.barcodescanner.component;

import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.ListView;
import android.widget.Toast;

import com.example.dprefac.barcodescanner.MainActivity;
import com.example.dprefac.barcodescanner.NewProductActivity;
import com.example.dprefac.barcodescanner.ProductDetailsActivity;
import com.example.dprefac.barcodescanner.R;
import com.example.dprefac.barcodescanner.dto.Feature;
import com.example.dprefac.barcodescanner.model.Product;
import com.example.dprefac.barcodescanner.service.ProductService;

import java.util.ArrayList;
import java.util.List;

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

    final List<ListViewItemDTO> initItemList = new ArrayList<>();
    ListViewItemCheckboxBaseAdapter listViewDataAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list_view_with_checkbox);

        setTitle("dev2qa.com - Android ListView With CheckBox");
        listViewDataAdapter = new ListViewItemCheckboxBaseAdapter(getApplicationContext(), initItemList);

        // Get listview checkbox.
        final ListView listViewWithCheckbox = (ListView) findViewById(R.id.list_view_with_checkbox);

        listViewDataAdapter.notifyDataSetChanged();

        // Set data adapter to list view.
        listViewWithCheckbox.setAdapter(listViewDataAdapter);

        // When list view item is clicked.
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

                //Toast.makeText(getApplicationContext(), "select item text : " + itemDto.getItemText(), Toast.LENGTH_SHORT).show();
            }
        });

        // Click this button to select all listview items with checkbox checked.
        Button selectAllButton = (Button) findViewById(R.id.list_select_all);
        selectAllButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int size = initItemList.size();
                for (int i = 0; i < size; i++) {
                    ListViewItemDTO dto = initItemList.get(i);
                    dto.setChecked(true);
                }

                listViewDataAdapter.notifyDataSetChanged();
            }
        });

        // Click this button to disselect all listview items with checkbox unchecked.
        Button selectNoneButton = (Button) findViewById(R.id.list_select_none);
        selectNoneButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int size = initItemList.size();
                for (int i = 0; i < size; i++) {
                    ListViewItemDTO dto = initItemList.get(i);
                    dto.setChecked(false);
                }

                listViewDataAdapter.notifyDataSetChanged();
            }
        });

        // Click this button to reverse select listview items.
        Button selectReverseButton = (Button) findViewById(R.id.list_select_reverse);
        selectReverseButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int size = initItemList.size();
                for (int i = 0; i < size; i++) {
                    ListViewItemDTO dto = initItemList.get(i);

                    if (dto.isChecked()) {
                        dto.setChecked(false);
                    } else {
                        dto.setChecked(true);
                    }
                }

                listViewDataAdapter.notifyDataSetChanged();
            }
        });

        // Click this button to remove selected items from listview.
        Button selectRemoveButton = (Button) findViewById(R.id.list_remove_selected_rows);
        selectRemoveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                AlertDialog alertDialog = new AlertDialog.Builder(ListViewWithCheckboxActivity.this).create();
                alertDialog.setMessage("Are you sure to remove selected listview items?");

                alertDialog.setButton(Dialog.BUTTON_POSITIVE, "Confirm", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int which) {
                        int size = initItemList.size();
                        for (int i = 0; i < size; i++) {
                            ListViewItemDTO dto = initItemList.get(i);

                            if (dto.isChecked()) {
                                initItemList.remove(i);
                                i--;
                                size = initItemList.size();
                            }
                        }

                        listViewDataAdapter.notifyDataSetChanged();
                    }
                });

                alertDialog.show();
            }
        });
        getFeatureList();

    }


    private void getFeatureList() {
        Call<List<Feature>> productCall = productService.getAllFeature();

        productCall.enqueue(new Callback<List<Feature>>() {
            @Override
            public void onResponse(Call<List<Feature>> call, Response<List<Feature>> response) {

                if (response.code() == HttpsURLConnection.HTTP_OK) {
                    List<Feature> product = response.body();
                    Log.i(TAG, "Call done!");

                    List<ListViewItemDTO> ret = new ArrayList<ListViewItemDTO>();

                    initItemList.clear();
                    for (Feature feature : product) {
                        ListViewItemDTO dto = new ListViewItemDTO();
                        dto.setChecked(false);
                        dto.setItemText(feature);

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