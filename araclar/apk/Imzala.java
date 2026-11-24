import com.android.apksig.ApkSigner;
import com.android.apksig.ApkVerifier;

import java.io.File;
import java.io.FileInputStream;
import java.security.KeyStore;
import java.security.MessageDigest;
import java.security.PrivateKey;
import java.security.cert.X509Certificate;
import java.util.Collections;

/** APK imzalama (v1+v2+v3) ve doğrulama.
 *  İmzala:    java -cp apksig.jar:. Imzala <ks> <depo şifresi> <alias> <girdi.apk> <çıktı.apk> [anahtar şifresi]   (PKCS12 ya da JKS)
 *  Sertifika: java -cp apksig.jar:. Imzala sertifika <apk>   → imzalayan sertifikanın SHA-256'sı (aynı anahtar denetimi) */
public class Imzala {
    static String sha(X509Certificate c) throws Exception {
        byte[] d = MessageDigest.getInstance("SHA-256").digest(c.getEncoded());
        StringBuilder sb = new StringBuilder();
        for (byte b : d) sb.append(String.format("%02x", b));
        return sb.toString();
    }

    public static void main(String[] a) throws Exception {
        if (a.length == 2 && "sertifika".equals(a[0])) {
            ApkVerifier.Result r = new ApkVerifier.Builder(new File(a[1])).build().verify();
            if (!r.isVerified()) { System.err.println("DOĞRULANAMADI: " + r.getErrors()); System.exit(1); }
            System.out.println(sha(r.getSignerCertificates().get(0)));
            return;
        }
        KeyStore ks = null;
        for (String type : new String[]{"PKCS12", "JKS"}) {
            try (FileInputStream in = new FileInputStream(a[0])) {
                KeyStore k = KeyStore.getInstance(type);
                k.load(in, a[1].toCharArray());
                ks = k;
                break;
            } catch (Exception ignored) { }
        }
        if (ks == null) { System.err.println("anahtar deposu açılamadı (şifre?)"); System.exit(1); }
        char[] kp = (a.length > 5 && !a[5].isEmpty() ? a[5] : a[1]).toCharArray();
        PrivateKey key = (PrivateKey) ks.getKey(a[2], kp);
        X509Certificate cert = (X509Certificate) ks.getCertificate(a[2]);
        if (key == null || cert == null) { System.err.println("alias bulunamadı: " + a[2]); System.exit(1); }
        ApkSigner.SignerConfig sc = new ApkSigner.SignerConfig.Builder("bereket", key, Collections.singletonList(cert)).build();
        new ApkSigner.Builder(Collections.singletonList(sc))
                .setInputApk(new File(a[3])).setOutputApk(new File(a[4]))
                .setV1SigningEnabled(true).setV2SigningEnabled(true).setV3SigningEnabled(true)
                .setMinSdkVersion(23).build().sign();
        ApkVerifier.Result r = new ApkVerifier.Builder(new File(a[4])).build().verify();
        if (!r.isVerified()) { System.err.println("DOĞRULAMA BAŞARISIZ: " + r.getErrors()); System.exit(1); }
        System.out.println("imza doğrulandı (v1=" + r.isVerifiedUsingV1Scheme() + " v2=" + r.isVerifiedUsingV2Scheme() + " v3=" + r.isVerifiedUsingV3Scheme() + "), sertifika SHA-256 " + sha(r.getSignerCertificates().get(0)));
    }
}
