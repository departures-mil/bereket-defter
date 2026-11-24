.class Lcom/bereket/alacakverecek/FcGuncelle$1;
.super Ljava/lang/Object;
.source "FcGuncelle.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/FcGuncelle;->apkUpdate(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic val$a:Landroid/app/Activity;

.field final synthetic val$planJson:Ljava/lang/String;

.field final synthetic val$w:Landroid/webkit/WebView;


# direct methods
.method constructor <init>(Ljava/lang/String;Landroid/app/Activity;Landroid/webkit/WebView;)V
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    iput-object p1, p0, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$planJson:Ljava/lang/String;

    iput-object p2, p0, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iput-object p3, p0, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 26

    move-object/from16 v1, p0

    const-string v0, ""

    const-string v2, "sha256"

    const-string v3, "}"

    const-string v4, "{\"type\":\"patchFailed\",\"error\":"

    const-string v5, "{\"type\":\"error\",\"error\":"

    :try_start_0
    new-instance v7, Lorg/json/JSONObject;

    iget-object v8, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$planJson:Ljava/lang/String;

    invoke-direct {v7, v8}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    const-string v8, "full"

    invoke-virtual {v7, v8}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v8

    const-string v9, "patch"

    invoke-virtual {v7, v9}, Lorg/json/JSONObject;->optJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v7

    new-instance v9, Ljava/io/File;

    iget-object v10, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    invoke-virtual {v10}, Landroid/app/Activity;->getCacheDir()Ljava/io/File;

    move-result-object v10

    const-string v11, "apk"

    invoke-direct {v9, v10, v11}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-virtual {v9}, Ljava/io/File;->isDirectory()Z

    move-result v10

    if-nez v10, :cond_1

    invoke-virtual {v9}, Ljava/io/File;->mkdirs()Z

    move-result v10

    if-eqz v10, :cond_0

    goto :goto_0

    :cond_0
    new-instance v0, Ljava/io/IOException;

    const-string v2, "WRITE"

    invoke-direct {v0, v2}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_1
    :goto_0
    new-instance v14, Ljava/io/File;

    const-string v10, "BereketDefter.apk"

    invoke-direct {v14, v9, v10}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-virtual {v8, v2}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v10

    invoke-virtual {v10}, Ljava/lang/String;->toLowerCase()Ljava/lang/String;

    move-result-object v15
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_3
    .catchall {:try_start_0 .. :try_end_0} :catchall_2

    const-string v12, "size"

    const-string v13, "BAD_HASH"

    const-string v6, "url"

    if-eqz v7, :cond_5

    :try_start_1
    invoke-virtual {v7, v6, v0}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v16

    invoke-virtual/range {v16 .. v16}, Ljava/lang/String;->length()I

    move-result v16

    if-lez v16, :cond_5

    new-instance v10, Ljava/io/File;

    const-string v11, "update.patch"

    invoke-direct {v10, v9, v11}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_3
    .catchall {:try_start_1 .. :try_end_1} :catchall_2

    :try_start_2
    iget-object v9, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v11, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    invoke-virtual {v7, v6}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v19
    :try_end_2
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_2} :catch_1
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    move-object/from16 v16, v5

    move-object/from16 v24, v6

    const-wide/16 v5, 0x0

    :try_start_3
    invoke-virtual {v7, v12, v5, v6}, Lorg/json/JSONObject;->optLong(Ljava/lang/String;J)J

    move-result-wide v21

    const/16 v23, 0x1

    move-object/from16 v17, v9

    move-object/from16 v18, v11

    move-object/from16 v20, v10

    invoke-static/range {v17 .. v23}, Lcom/bereket/alacakverecek/FcGuncelle;->access$000(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;Ljava/io/File;JZ)V

    invoke-virtual {v7, v2, v0}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v2

    if-lez v2, :cond_3

    invoke-static {v10}, Lcom/departuresmil/ortak/FcDelta;->sha256(Ljava/io/File;)[B

    move-result-object v2

    invoke-static {v2}, Lcom/departuresmil/ortak/FcDelta;->hex([B)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v0, v2}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_2

    goto :goto_1

    :cond_2
    new-instance v0, Ljava/io/IOException;

    invoke-direct {v0, v13}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_3
    :goto_1
    new-instance v0, Ljava/io/File;

    iget-object v2, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    invoke-virtual {v2}, Landroid/app/Activity;->getApplicationInfo()Landroid/content/pm/ApplicationInfo;

    move-result-object v2

    iget-object v2, v2, Landroid/content/pm/ApplicationInfo;->sourceDir:Ljava/lang/String;

    invoke-direct {v0, v2}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    const/4 v2, 0x0

    invoke-static {v0, v10, v14, v2}, Lcom/departuresmil/ortak/FcDelta;->apply(Ljava/io/File;Ljava/io/File;Ljava/io/File;Lcom/departuresmil/ortak/FcDelta$Progress;)Lcom/departuresmil/ortak/FcDelta$Header;

    move-result-object v0

    invoke-virtual {v0}, Lcom/departuresmil/ortak/FcDelta$Header;->dstSha256Hex()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v15, v0}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v0
    :try_end_3
    .catch Ljava/lang/Exception; {:try_start_3 .. :try_end_3} :catch_0
    .catchall {:try_start_3 .. :try_end_3} :catchall_1

    if-eqz v0, :cond_4

    :try_start_4
    invoke-virtual {v10}, Ljava/io/File;->delete()Z
    :try_end_4
    .catch Ljava/lang/Exception; {:try_start_4 .. :try_end_4} :catch_2
    .catchall {:try_start_4 .. :try_end_4} :catchall_2

    goto :goto_5

    :cond_4
    :try_start_5
    new-instance v0, Ljava/io/IOException;

    invoke-direct {v0, v13}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_5
    .catch Ljava/lang/Exception; {:try_start_5 .. :try_end_5} :catch_0
    .catchall {:try_start_5 .. :try_end_5} :catchall_1

    :catch_0
    move-exception v0

    goto :goto_2

    :catchall_0
    move-exception v0

    move-object/from16 v16, v5

    goto :goto_3

    :catch_1
    move-exception v0

    move-object/from16 v16, v5

    move-object/from16 v24, v6

    :goto_2
    :try_start_6
    iget-object v2, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v5, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lorg/json/JSONObject;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v6, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v6, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v2, v5, v0}, Lcom/bereket/alacakverecek/FcGuncelle;->access$100(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V
    :try_end_6
    .catchall {:try_start_6 .. :try_end_6} :catchall_1

    :try_start_7
    invoke-virtual {v10}, Ljava/io/File;->delete()Z

    goto :goto_4

    :catchall_1
    move-exception v0

    :goto_3
    invoke-virtual {v10}, Ljava/io/File;->delete()Z

    throw v0

    :cond_5
    move-object/from16 v16, v5

    move-object/from16 v24, v6

    :goto_4
    iget-object v7, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v0, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    move-object/from16 v2, v24

    invoke-virtual {v8, v2}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v9

    const-wide/16 v4, 0x0

    invoke-virtual {v8, v12, v4, v5}, Lorg/json/JSONObject;->optLong(Ljava/lang/String;J)J

    move-result-wide v11

    const/4 v2, 0x0

    move-object v8, v0

    move-object v10, v14

    move-object v4, v13

    move v13, v2

    invoke-static/range {v7 .. v13}, Lcom/bereket/alacakverecek/FcGuncelle;->access$000(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;Ljava/io/File;JZ)V

    invoke-static {v14}, Lcom/departuresmil/ortak/FcDelta;->sha256(Ljava/io/File;)[B

    move-result-object v0

    invoke-static {v0}, Lcom/departuresmil/ortak/FcDelta;->hex([B)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v15, v0}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_8

    :goto_5
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1a

    if-lt v0, v2, :cond_7

    iget-object v0, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    invoke-virtual {v0}, Landroid/app/Activity;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v0

    invoke-virtual {v0}, Landroid/content/pm/PackageManager;->canRequestPackageInstalls()Z

    move-result v0

    if-eqz v0, :cond_6

    goto :goto_6

    :cond_6
    iget-object v0, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    new-instance v2, Lcom/bereket/alacakverecek/FcGuncelle$1$1;

    invoke-direct {v2, v1}, Lcom/bereket/alacakverecek/FcGuncelle$1$1;-><init>(Lcom/bereket/alacakverecek/FcGuncelle$1;)V

    invoke-virtual {v0, v2}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    new-instance v0, Ljava/io/IOException;

    const-string v2, "IZIN"

    invoke-direct {v0, v2}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_7
    :goto_6
    iget-object v0, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v2, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    const-string v4, "{\"type\":\"installing\"}"

    invoke-static {v0, v2, v4}, Lcom/bereket/alacakverecek/FcGuncelle;->access$100(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V

    iget-object v0, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    new-instance v2, Lcom/bereket/alacakverecek/FcGuncelle$1$2;

    invoke-direct {v2, v1, v14}, Lcom/bereket/alacakverecek/FcGuncelle$1$2;-><init>(Lcom/bereket/alacakverecek/FcGuncelle$1;Ljava/io/File;)V

    invoke-virtual {v0, v2}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    iget-object v0, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v2, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    const-string v4, "{\"type\":\"done\",\"result\":\"done\"}"

    invoke-static {v0, v2, v4}, Lcom/bereket/alacakverecek/FcGuncelle;->access$100(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V

    const/4 v2, 0x0

    goto :goto_8

    :catch_2
    move-exception v0

    goto :goto_7

    :cond_8
    invoke-virtual {v14}, Ljava/io/File;->delete()Z

    new-instance v0, Ljava/io/IOException;

    invoke-direct {v0, v4}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_7
    .catch Ljava/lang/Exception; {:try_start_7 .. :try_end_7} :catch_2
    .catchall {:try_start_7 .. :try_end_7} :catchall_2

    :catchall_2
    move-exception v0

    const/4 v2, 0x0

    goto :goto_9

    :catch_3
    move-exception v0

    move-object/from16 v16, v5

    :goto_7
    :try_start_8
    iget-object v2, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v4, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    new-instance v5, Ljava/lang/StringBuilder;

    move-object/from16 v6, v16

    invoke-direct {v5, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lorg/json/JSONObject;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v5, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v2, v4, v0}, Lcom/bereket/alacakverecek/FcGuncelle;->access$100(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V
    :try_end_8
    .catchall {:try_start_8 .. :try_end_8} :catchall_2

    const/4 v2, 0x0

    :goto_8
    invoke-static {v2}, Lcom/bereket/alacakverecek/FcGuncelle;->access$202(Z)Z

    return-void

    :goto_9
    invoke-static {v2}, Lcom/bereket/alacakverecek/FcGuncelle;->access$202(Z)Z

    throw v0
.end method
