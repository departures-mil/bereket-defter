.class public final Lcom/bereket/alacakverecek/MainActivity$Bridge;
.super Ljava/lang/Object;
.source "MainActivity.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/bereket/alacakverecek/MainActivity;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x11
    name = "Bridge"
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;


# direct methods
.method public constructor <init>(Lcom/bereket/alacakverecek/MainActivity;)V
    .locals 0

    .prologue
    .line 893
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public appVersion()Ljava/lang/String;
    .locals 1
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1045
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->appVersionName()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public bundleOk()V
    .locals 1
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1061
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    invoke-static {v0}, Lcom/bereket/alacakverecek/Updates;->markOk(Landroid/content/Context;)V

    .line 1062
    return-void
.end method

.method public cancelReminder(Ljava/lang/String;)V
    .locals 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1035
    if-eqz p1, :cond_0

    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v0

    if-nez v0, :cond_1

    .line 1041
    :cond_0
    :goto_0
    return-void

    .line 1037
    :cond_1
    :try_start_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    invoke-static {v0, p1}, Lcom/bereket/alacakverecek/Reminders;->cancel(Landroid/content/Context;Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 1038
    :catch_0
    move-exception v0

    .line 1039
    const-string v1, "BereketDefter"

    const-string v2, "cancelReminder"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    goto :goto_0
.end method

.method public exitApp()V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1145
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge$10;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$Bridge$10;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;)V

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 1151
    return-void
.end method

.method public installApk(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 4
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1096
    :try_start_0
    invoke-static {p1}, Lcom/bereket/alacakverecek/MainActivity;->decodeBase64(Ljava/lang/String;)[B

    move-result-object v1

    .line 1097
    invoke-static {v1}, Lcom/bereket/alacakverecek/Updates;->sha256Hex([B)Ljava/lang/String;

    move-result-object v2

    if-nez p2, :cond_0

    const-string v0, ""

    :goto_0
    invoke-virtual {v2, v0}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_1

    const-string v0, "BAD_PACKAGE"

    .line 1140
    :goto_1
    return-object v0

    .line 1097
    :cond_0
    invoke-virtual {p2}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    goto :goto_0

    .line 1098
    :cond_1
    new-instance v0, Ljava/io/File;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v2}, Lcom/bereket/alacakverecek/MainActivity;->getCacheDir()Ljava/io/File;

    move-result-object v2

    const-string v3, "apk"

    invoke-direct {v0, v2, v3}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 1099
    invoke-static {v0}, Lcom/bereket/alacakverecek/Updates;->deleteTree(Ljava/io/File;)V

    .line 1100
    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    .line 1101
    new-instance v2, Ljava/io/File;

    const-string v3, "BereketDefter.apk"

    invoke-direct {v2, v0, v3}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 1102
    new-instance v0, Ljava/io/FileOutputStream;

    invoke-direct {v0, v2}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 1104
    :try_start_1
    invoke-virtual {v0, v1}, Ljava/io/OutputStream;->write([B)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    .line 1106
    :try_start_2
    invoke-virtual {v0}, Ljava/io/OutputStream;->close()V
    :try_end_2
    .catch Ljava/lang/Throwable; {:try_start_2 .. :try_end_2} :catch_0

    .line 1112
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1a

    if-lt v0, v1, :cond_2

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->canInstallPackages()Z

    move-result v0

    if-nez v0, :cond_2

    .line 1113
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge$8;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$Bridge$8;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;)V

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 1124
    const-string v0, "IZIN"

    goto :goto_1

    .line 1106
    :catchall_0
    move-exception v1

    :try_start_3
    invoke-virtual {v0}, Ljava/io/OutputStream;->close()V

    .line 1107
    throw v1
    :try_end_3
    .catch Ljava/lang/Throwable; {:try_start_3 .. :try_end_3} :catch_0

    .line 1108
    :catch_0
    move-exception v0

    .line 1109
    const-string v1, "BereketDefter"

    const-string v2, "installApk"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 1110
    const-string v0, "WRITE"

    goto :goto_1

    .line 1126
    :cond_2
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;

    invoke-direct {v1, p0, v2}, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/io/File;)V

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 1140
    const-string v0, "ok"

    goto :goto_1
.end method

.method public installBundle(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1068
    :try_start_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    invoke-static {v0, p1, p2, p3}, Lcom/bereket/alacakverecek/Updates;->installBundle(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v0

    .line 1071
    :goto_0
    return-object v0

    .line 1069
    :catch_0
    move-exception v0

    .line 1070
    const-string v1, "BereketDefter"

    const-string v2, "installBundle"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 1071
    const-string v0, "WRITE"

    goto :goto_0
.end method

.method public minimizeApp()V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->moveTaskToBack(Z)Z

    return-void
.end method

.method public nativeCode()I
    .locals 4
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    const/4 v0, 0x0

    .line 1052
    :try_start_0
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v1}, Lcom/bereket/alacakverecek/MainActivity;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v1

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v2}, Lcom/bereket/alacakverecek/MainActivity;->getPackageName()Ljava/lang/String;

    move-result-object v2

    const/4 v3, 0x0

    invoke-virtual {v1, v2, v3}, Landroid/content/pm/PackageManager;->getPackageInfo(Ljava/lang/String;I)Landroid/content/pm/PackageInfo;

    move-result-object v1

    iget v0, v1, Landroid/content/pm/PackageInfo;->versionCode:I
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 1054
    :goto_0
    return v0

    .line 1053
    :catch_0
    move-exception v1

    goto :goto_0
.end method

.method public openFile(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 978
    invoke-static {p2, p3}, Lcom/bereket/alacakverecek/Util;->effectiveMime(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 979
    invoke-static {p3, v0}, Lcom/bereket/alacakverecek/Util;->safeFileName(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 982
    :try_start_0
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const-string v4, "open"

    invoke-static {p1}, Lcom/bereket/alacakverecek/MainActivity;->decodeBase64(Ljava/lang/String;)[B

    move-result-object v5

    invoke-virtual {v3, v4, v1, v5}, Lcom/bereket/alacakverecek/MainActivity;->writeTemp(Ljava/lang/String;Ljava/lang/String;[B)Ljava/io/File;

    move-result-object v1

    invoke-static {v2, v1}, Lcom/bereket/alacakverecek/FilesProvider;->uriFor(Landroid/content/Context;Ljava/io/File;)Landroid/net/Uri;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v1

    .line 988
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v3, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;

    invoke-direct {v3, p0, v1, v0}, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Landroid/net/Uri;Ljava/lang/String;)V

    invoke-virtual {v2, v3}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 1004
    :goto_0
    return-void

    .line 983
    :catch_0
    move-exception v0

    .line 984
    const-string v1, "BereketDefter"

    const-string v2, "openFile"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 985
    const-string v0, "Dosya a\u00e7\u0131lamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity$Bridge;->toast(Ljava/lang/String;)V

    goto :goto_0
.end method

.method public openUrl(Ljava/lang/String;)V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1008
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge$5;

    invoke-direct {v1, p0, p1}, Lcom/bereket/alacakverecek/MainActivity$Bridge$5;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 1014
    return-void
.end method

.method public printHtml(Ljava/lang/String;Ljava/lang/String;)V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 897
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;

    invoke-direct {v1, p0, p1, p2}, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 903
    return-void
.end method

.method public restartApp()V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1078
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge$7;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$Bridge$7;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;)V

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 1086
    return-void
.end method

.method public saveFile(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 5
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 907
    invoke-static {p2, p3}, Lcom/bereket/alacakverecek/Util;->effectiveMime(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 908
    invoke-static {p3, v0}, Lcom/bereket/alacakverecek/Util;->safeFileName(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 911
    :try_start_0
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const-string v3, "save"

    invoke-static {p1}, Lcom/bereket/alacakverecek/MainActivity;->decodeBase64(Ljava/lang/String;)[B

    move-result-object v4

    invoke-virtual {v2, v3, v1, v4}, Lcom/bereket/alacakverecek/MainActivity;->writeTemp(Ljava/lang/String;Ljava/lang/String;[B)Ljava/io/File;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v2

    .line 917
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v4, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;

    invoke-direct {v4, p0, v2, v0, v1}, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/io/File;Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {v3, v4}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 940
    :goto_0
    return-void

    .line 912
    :catch_0
    move-exception v0

    .line 913
    const-string v1, "BereketDefter"

    const-string v2, "saveFile"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 914
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->access$1300(Lcom/bereket/alacakverecek/MainActivity;Z)V

    goto :goto_0
.end method

.method public scheduleReminder(Ljava/lang/String;DLjava/lang/String;Ljava/lang/String;)V
    .locals 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1019
    if-eqz p1, :cond_0

    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v0

    if-eqz v0, :cond_0

    invoke-static {p2, p3}, Ljava/lang/Double;->isNaN(D)Z

    move-result v0

    if-eqz v0, :cond_1

    .line 1031
    :cond_0
    :goto_0
    return-void

    .line 1021
    :cond_1
    :try_start_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    double-to-long v2, p2

    move-object v1, p1

    move-object v4, p4

    move-object v5, p5

    invoke-static/range {v0 .. v5}, Lcom/bereket/alacakverecek/Reminders;->schedule(Landroid/content/Context;Ljava/lang/String;JLjava/lang/String;Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 1025
    :goto_1
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge$6;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$Bridge$6;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;)V

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    goto :goto_0

    .line 1022
    :catch_0
    move-exception v0

    .line 1023
    const-string v1, "BereketDefter"

    const-string v2, "scheduleReminder"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    goto :goto_1
.end method

.method public shareFile(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 944
    invoke-static {p2, p3}, Lcom/bereket/alacakverecek/Util;->effectiveMime(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 945
    invoke-static {p3, v0}, Lcom/bereket/alacakverecek/Util;->safeFileName(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 948
    :try_start_0
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const-string v4, "share"

    invoke-static {p1}, Lcom/bereket/alacakverecek/MainActivity;->decodeBase64(Ljava/lang/String;)[B

    move-result-object v5

    invoke-virtual {v3, v4, v1, v5}, Lcom/bereket/alacakverecek/MainActivity;->writeTemp(Ljava/lang/String;Ljava/lang/String;[B)Ljava/io/File;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/bereket/alacakverecek/FilesProvider;->uriFor(Landroid/content/Context;Ljava/io/File;)Landroid/net/Uri;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v2

    .line 954
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-instance v4, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;

    invoke-direct {v4, p0, v0, v2, v1}, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;-><init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/lang/String;Landroid/net/Uri;Ljava/lang/String;)V

    invoke-virtual {v3, v4}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 974
    :goto_0
    return-void

    .line 949
    :catch_0
    move-exception v0

    .line 950
    const-string v1, "BereketDefter"

    const-string v2, "shareFile"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 951
    const-string v0, "Dosya payla\u015f\u0131lamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity$Bridge;->toast(Ljava/lang/String;)V

    goto :goto_0
.end method

.method public toast(Ljava/lang/String;)V
    .locals 1
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    .prologue
    .line 1155
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0, p1}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    .line 1156
    return-void
.end method

# ---- v1.21: ortak çekirdek köprüsü (FC.host android sözleşmesi). Kaynak: android/java/…/FcGuncelle.java
.method public moveTaskToBack()V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->moveTaskToBack(Z)Z

    return-void
.end method

.method public openExternal(Ljava/lang/String;)V
    .locals 1
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0, p1}, Lcom/bereket/alacakverecek/MainActivity;->openExternal(Ljava/lang/String;)V

    return-void
.end method

.method public notify(Ljava/lang/String;Ljava/lang/String;)V
    .locals 1
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0, p1, p2}, Lcom/bereket/alacakverecek/FcGuncelle;->notify(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method

.method public apkUpdate(Ljava/lang/String;)V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;

    move-result-object v1

    invoke-static {v0, v1, p1}, Lcom/bereket/alacakverecek/FcGuncelle;->apkUpdate(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V

    return-void
.end method
