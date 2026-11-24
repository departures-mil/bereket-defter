.class public final Lcom/bereket/alacakverecek/FcGuncelle;
.super Ljava/lang/Object;
.source "FcGuncelle.java"


# static fields
.field private static volatile busy:Z = false


# direct methods
.method static constructor <clinit>()V
    .registers 0

    return-void
.end method

.method private constructor <init>()V
    .registers 1

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method static synthetic access$000(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;Ljava/io/File;JZ)V
    .registers 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    invoke-static/range {p0 .. p6}, Lcom/bereket/alacakverecek/FcGuncelle;->download(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;Ljava/io/File;JZ)V

    return-void
.end method

.method static synthetic access$100(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V
    .registers 3

    invoke-static {p0, p1, p2}, Lcom/bereket/alacakverecek/FcGuncelle;->emit(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V

    return-void
.end method

.method static synthetic access$202(Z)Z
    .registers 1

    sput-boolean p0, Lcom/bereket/alacakverecek/FcGuncelle;->busy:Z

    return p0
.end method

.method public static apkUpdate(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V
    .registers 5

    sget-boolean v0, Lcom/bereket/alacakverecek/FcGuncelle;->busy:Z

    if-eqz v0, :cond_0

    const-string p2, "{\"type\":\"error\",\"error\":\"BUSY\"}"

    invoke-static {p0, p1, p2}, Lcom/bereket/alacakverecek/FcGuncelle;->emit(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V

    return-void

    :cond_0
    const/4 v0, 0x1

    sput-boolean v0, Lcom/bereket/alacakverecek/FcGuncelle;->busy:Z

    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/bereket/alacakverecek/FcGuncelle$1;

    invoke-direct {v1, p2, p0, p1}, Lcom/bereket/alacakverecek/FcGuncelle$1;-><init>(Ljava/lang/String;Landroid/app/Activity;Landroid/webkit/WebView;)V

    const-string p0, "fc-guncelle"

    invoke-direct {v0, v1, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method private static download(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;Ljava/io/File;JZ)V
    .registers 27
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    move-object/from16 v0, p0

    move-object/from16 v1, p1

    move-object/from16 v2, p2

    move/from16 v3, p6

    const-string v4, "https://github.com/"

    invoke-virtual {v2, v4}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v4

    if-nez v4, :cond_1

    const-string v4, "https://objects.githubusercontent.com/"

    invoke-virtual {v2, v4}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v4

    if-nez v4, :cond_1

    const-string v4, "https://release-assets.githubusercontent.com/"

    invoke-virtual {v2, v4}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v4

    if-eqz v4, :cond_0

    goto :goto_0

    :cond_0
    new-instance v0, Ljava/io/IOException;

    const-string v1, "BAD_URL"

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_1
    :goto_0
    const/4 v4, 0x0

    const/4 v5, 0x0

    move v6, v4

    :goto_1
    const/4 v7, 0x6

    if-ge v6, v7, :cond_5

    new-instance v5, Ljava/net/URL;

    invoke-direct {v5, v2}, Ljava/net/URL;-><init>(Ljava/lang/String;)V

    invoke-virtual {v5}, Ljava/net/URL;->openConnection()Ljava/net/URLConnection;

    move-result-object v2

    move-object v5, v2

    check-cast v5, Ljava/net/HttpURLConnection;

    invoke-virtual {v5, v4}, Ljava/net/HttpURLConnection;->setInstanceFollowRedirects(Z)V

    const/16 v2, 0x4e20

    invoke-virtual {v5, v2}, Ljava/net/HttpURLConnection;->setConnectTimeout(I)V

    const v2, 0xea60

    invoke-virtual {v5, v2}, Ljava/net/HttpURLConnection;->setReadTimeout(I)V

    const-string v2, "User-Agent"

    const-string v7, "BereketDefter-Android"

    invoke-virtual {v5, v2, v7}, Ljava/net/HttpURLConnection;->setRequestProperty(Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {v5}, Ljava/net/HttpURLConnection;->getResponseCode()I

    move-result v2

    const/16 v7, 0x12c

    const-string v8, "HTTP "

    if-lt v2, v7, :cond_3

    const/16 v7, 0x190

    if-ge v2, v7, :cond_3

    const-string v7, "Location"

    invoke-virtual {v5, v7}, Ljava/net/HttpURLConnection;->getHeaderField(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v5}, Ljava/net/HttpURLConnection;->disconnect()V

    if-eqz v7, :cond_2

    const-string v9, "https://"

    invoke-virtual {v7, v9}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v9

    if-eqz v9, :cond_2

    add-int/lit8 v6, v6, 0x1

    move-object v2, v7

    goto :goto_1

    :cond_2
    new-instance v0, Ljava/io/IOException;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_3
    const/16 v6, 0xc8

    if-ne v2, v6, :cond_4

    goto :goto_2

    :cond_4
    invoke-virtual {v5}, Ljava/net/HttpURLConnection;->disconnect()V

    new-instance v0, Ljava/io/IOException;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_5
    :goto_2
    const-wide/16 v6, 0x0

    cmp-long v2, p4, v6

    if-lez v2, :cond_6

    move-wide/from16 v8, p4

    goto :goto_3

    :cond_6
    invoke-virtual {v5}, Ljava/net/HttpURLConnection;->getContentLength()I

    move-result v2

    invoke-static {v4, v2}, Ljava/lang/Math;->max(II)I

    move-result v2

    int-to-long v8, v2

    :goto_3
    invoke-virtual {v5}, Ljava/net/HttpURLConnection;->getInputStream()Ljava/io/InputStream;

    move-result-object v2

    new-instance v10, Ljava/io/FileOutputStream;

    move-object/from16 v11, p3

    invoke-direct {v10, v11}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    const/high16 v11, 0x10000

    :try_start_0
    new-array v11, v11, [B

    move-wide v12, v6

    :goto_4
    invoke-virtual {v2, v11}, Ljava/io/InputStream;->read([B)I

    move-result v14
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_1

    const-string v15, ",\"total\":"

    const-string v4, ",\"done\":"

    move-object/from16 p2, v5

    const-string v5, "{\"type\":\"progress\",\"patch\":"

    if-lez v14, :cond_8

    move-object/from16 p4, v2

    const/4 v2, 0x0

    :try_start_1
    invoke-virtual {v10, v11, v2, v14}, Ljava/io/FileOutputStream;->write([BII)V

    int-to-long v2, v14

    add-long/2addr v6, v2

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v2

    sub-long v16, v2, v12

    const-wide/16 v18, 0xc8

    cmp-long v14, v16, v18

    if-lez v14, :cond_7

    new-instance v12, Ljava/lang/StringBuilder;

    invoke-direct {v12}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v12, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move/from16 v14, p6

    invoke-virtual {v12, v14}, Ljava/lang/StringBuilder;->append(Z)Ljava/lang/StringBuilder;

    invoke-virtual {v12, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v12, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    invoke-virtual {v12, v15}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v12, v8, v9}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v4, "}"

    invoke-virtual {v12, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {v0, v1, v4}, Lcom/bereket/alacakverecek/FcGuncelle;->emit(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    move-wide v12, v2

    goto :goto_5

    :cond_7
    move/from16 v14, p6

    :goto_5
    move-object/from16 v5, p2

    move-object/from16 v2, p4

    move v3, v14

    const/4 v4, 0x0

    goto :goto_4

    :catchall_0
    move-exception v0

    goto :goto_6

    :cond_8
    move-object/from16 p4, v2

    move v14, v3

    :try_start_2
    invoke-virtual {v10}, Ljava/io/FileOutputStream;->close()V
    :try_end_2
    .catch Ljava/io/IOException; {:try_start_2 .. :try_end_2} :catch_0

    :catch_0
    :try_start_3
    invoke-virtual/range {p4 .. p4}, Ljava/io/InputStream;->close()V
    :try_end_3
    .catch Ljava/io/IOException; {:try_start_3 .. :try_end_3} :catch_1

    :catch_1
    invoke-virtual/range {p2 .. p2}, Ljava/net/HttpURLConnection;->disconnect()V

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, v14}, Ljava/lang/StringBuilder;->append(Z)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v15}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v8, v9}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v3, ",\"finished\":true}"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/FcGuncelle;->emit(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V

    return-void

    :catchall_1
    move-exception v0

    move-object/from16 p4, v2

    move-object/from16 p2, v5

    :goto_6
    :try_start_4
    invoke-virtual {v10}, Ljava/io/FileOutputStream;->close()V
    :try_end_4
    .catch Ljava/io/IOException; {:try_start_4 .. :try_end_4} :catch_2

    :catch_2
    :try_start_5
    invoke-virtual/range {p4 .. p4}, Ljava/io/InputStream;->close()V
    :try_end_5
    .catch Ljava/io/IOException; {:try_start_5 .. :try_end_5} :catch_3

    :catch_3
    invoke-virtual/range {p2 .. p2}, Ljava/net/HttpURLConnection;->disconnect()V

    throw v0
.end method

.method private static emit(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V
    .registers 4

    if-nez p1, :cond_0

    return-void

    :cond_0
    new-instance v0, Lcom/bereket/alacakverecek/FcGuncelle$2;

    invoke-direct {v0, p1, p2}, Lcom/bereket/alacakverecek/FcGuncelle$2;-><init>(Landroid/webkit/WebView;Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    return-void
.end method

.method public static notify(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V
    .registers 4

    :try_start_0
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    move-result-object p0

    const-string v0, "fc_agent"

    invoke-static {p0, v0, p1, p2}, Lcom/bereket/alacakverecek/Reminders;->show(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :catchall_0
    return-void
.end method
