+++
title= "Bypassing Kakao Login Signature Check for Tampered Android Application"
categories = [
    "trick",
]
date= "2017-11-23 11:48:14"
+++

I was experiencing something like can't login with Kakao when the app has been tampered. After going some trials and errors, I've found out that it requires Signature hash check for Login in. In `com.kakao.util.helper.Utility`

```java
public static String getKeyHash(Context context) {
    String str = null;
    PackageInfo packageInfo = getPackageInfo(context, 64);
    if (packageInfo != null) {
        Signature\[\] signatureArr = packageInfo.signatures;
        int length = signatureArr.length;
        int i = 0;
        while (i < length) {
            Signature signature = signatureArr\[i\];
            try {
                MessageDigest md = MessageDigest.getInstance("SHA");
                byte\[\] toByteArray = signature.toByteArray();
                md.update(signature.toByteArray());
                str = Base64.encodeToString(md.digest(), 2);
                break;
            } catch (NoSuchAlgorithmException e) {
                Log.w(TAG, "Unable to get MessageDigest. signature=" + signature, e);
                i++;
            }
        }
    }
    return str;
}
```

This function returns the application signature SHA1 hash encoded in base64. Sure enough I just need replace `str` with original application signature to prevent apps using my crafted signature but thats _**too plain.**_ I want a library that can be used again in the future if need it. So, my approach was using this another handcrafted class to return Signature.

```java
import android.content.pm.Signature;
import java.math.BigInteger;

public class xSign {
    public static String bits = "3082037130820259a003...............";
    public static byte\[\] byte = new BigInteger(bits, 16).toByteArray();

    public static Signature\[\] arraySig() {
        return new Signature\[\] { new Signature(bits) };
    }
}
```

This looks a bit nasty, but it works. How this code should be used? copy Actual application signature hex encoded into `Signature bits`. As a /skid/ that needz toolz, use lohan+ tool for extracting signature from APK, from there you could get the APK signature bits too. (http://androidcracking.blogspot.com/2010/12/getting-apk-signature-outside-of.html) Then, do change code into something looks like this.

```java
                MessageDigest md = MessageDigest.getInstance("SHA");
                byte\[\] toByteArray = signature.toByteArray();
                md.update(xSign.byte);
                str = Base64.encodeToString(md.digest(), 2);
```

All is set, recompile the code, run application, then profit. I could login with Kakao in a modified application. What have I learned from this? Signature checking isn't really proof from a _skid_ to reverse engineer application. This code might come in handy if someone really need to _spoof_ the Application signature.