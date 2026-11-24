import com.android.tools.smali.baksmali.BaksmaliOptions;
import com.android.tools.smali.dexlib2.DexFileFactory;
import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.iface.MultiDexContainer;

import java.io.File;

/** classes.dex → smali klasörü, apktool 2.12.1 jar'ındaki baksmali ile (apktool sürümü araclar/apk.py ile aynı olmalı).
 *  Kullanım: java -cp apktool.jar:. Baksmali classes.dex çıktı/ */
public class Baksmali {
    public static void main(String[] a) throws Exception {
        MultiDexContainer c = DexFileFactory.loadDexContainer(new File(a[0]), new Opcodes(23, -1));
        String name = (String) c.getDexEntryNames().get(0);
        BaksmaliOptions o = new BaksmaliOptions();
        o.debugInfo = false;
        o.sequentialLabels = true;
        com.android.tools.smali.baksmali.Baksmali.disassembleDexFile(c.getEntry(name).getDexFile(), new File(a[1]), 1, o);
    }
}
