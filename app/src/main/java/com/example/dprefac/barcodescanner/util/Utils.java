package com.example.dprefac.barcodescanner.util;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

/**
 * Created by dprefac on 26-Jun-19.
 */

public class Utils {
    public static Bitmap base64StringToBitmap(String image) {
        byte[] imageData = Base64.decode(image, Base64.URL_SAFE);
        return BitmapFactory.decodeByteArray(imageData, 0, imageData.length);
    }
}
