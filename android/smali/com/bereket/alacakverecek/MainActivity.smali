.class public Lcom/bereket/alacakverecek/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/bereket/alacakverecek/MainActivity$AppClient;,
        Lcom/bereket/alacakverecek/MainActivity$ChromeClient;,
        Lcom/bereket/alacakverecek/MainActivity$Bridge;
    }
.end annotation


# static fields
.field static final HOST:Ljava/lang/String; = "appassets.androidplatform.net"

.field static final ORIGIN:Ljava/lang/String; = "https://appassets.androidplatform.net"

.field static final PERM_CAMERA:I = 0x7d1

.field static final PERM_NOTIF:I = 0x7d2

.field static final PERM_POST_NOTIFICATIONS:Ljava/lang/String; = "android.permission.POST_NOTIFICATIONS"

.field static final PERM_WEBCAM:I = 0x7d3

.field static final REQ_CAMERA:I = 0x3ea

.field static final REQ_FILES:I = 0x3e9

.field static final REQ_SAVE:I = 0x3eb

.field static final SDK_TIRAMISU:I = 0x21

.field static final START_URL:Ljava/lang/String; = "https://appassets.androidplatform.net/www/index.html"

.field static final STATUS_BAR_COLOR:I = -0xf9aec1

.field static final TAG:Ljava/lang/String; = "BereketDefter"

.field static volatile activeBundle:Ljava/io/File;


# instance fields
.field private cameraFile:Ljava/io/File;

.field private cameraPermissionPending:Z

.field private cameraUri:Landroid/net/Uri;

.field private chooserMimes:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List",
            "<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private chooserMultiple:Z

.field private exitDialog:Landroid/app/AlertDialog;

.field private fileCallback:Landroid/webkit/ValueCallback;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Landroid/webkit/ValueCallback",
            "<[",
            "Landroid/net/Uri;",
            ">;"
        }
    .end annotation
.end field

.field private pendingSaveFile:Ljava/io/File;

.field private pendingWebPermission:Landroid/webkit/PermissionRequest;

.field private printWebView:Landroid/webkit/WebView;

.field private web:Landroid/webkit/WebView;


# direct methods
.method public constructor <init>()V
    .locals 1

    .prologue
    .line 58
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 84
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMimes:Ljava/util/List;

    return-void
.end method

.method static synthetic access$000(Lcom/bereket/alacakverecek/MainActivity;)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->askExit()V

    return-void
.end method

.method static synthetic access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;
    .locals 1

    .prologue
    .line 58
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    return-object v0
.end method

.method static synthetic access$1000(Lcom/bereket/alacakverecek/MainActivity;Ljava/lang/String;)Z
    .locals 1

    .prologue
    .line 58
    invoke-direct {p0, p1}, Lcom/bereket/alacakverecek/MainActivity;->hasPermission(Ljava/lang/String;)Z

    move-result v0

    return v0
.end method

.method static synthetic access$1100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/PermissionRequest;
    .locals 1

    .prologue
    .line 58
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingWebPermission:Landroid/webkit/PermissionRequest;

    return-object v0
.end method

.method static synthetic access$1102(Lcom/bereket/alacakverecek/MainActivity;Landroid/webkit/PermissionRequest;)Landroid/webkit/PermissionRequest;
    .locals 0

    .prologue
    .line 58
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingWebPermission:Landroid/webkit/PermissionRequest;

    return-object p1
.end method

.method static synthetic access$1200(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;Landroid/net/Uri;)Z
    .locals 1

    .prologue
    .line 58
    invoke-direct {p0, p1, p2}, Lcom/bereket/alacakverecek/MainActivity;->copyToUri(Ljava/io/File;Landroid/net/Uri;)Z

    move-result v0

    return v0
.end method

.method static synthetic access$1300(Lcom/bereket/alacakverecek/MainActivity;Z)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0, p1}, Lcom/bereket/alacakverecek/MainActivity;->notifySaved(Z)V

    return-void
.end method

.method static synthetic access$1400(Lcom/bereket/alacakverecek/MainActivity;Landroid/webkit/WebView;Ljava/lang/String;)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0, p1, p2}, Lcom/bereket/alacakverecek/MainActivity;->startPrintJob(Landroid/webkit/WebView;Ljava/lang/String;)V

    return-void
.end method

.method static synthetic access$1500(Lcom/bereket/alacakverecek/MainActivity;Ljava/lang/String;Ljava/lang/String;)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0, p1, p2}, Lcom/bereket/alacakverecek/MainActivity;->printHtmlOnUi(Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method

.method static synthetic access$1600(Lcom/bereket/alacakverecek/MainActivity;)Ljava/io/File;
    .locals 1

    .prologue
    .line 58
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingSaveFile:Ljava/io/File;

    return-object v0
.end method

.method static synthetic access$1602(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;)Ljava/io/File;
    .locals 0

    .prologue
    .line 58
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingSaveFile:Ljava/io/File;

    return-object p1
.end method

.method static synthetic access$200(Ljava/io/File;JZ)V
    .locals 1

    .prologue
    .line 58
    invoke-static {p0, p1, p2, p3}, Lcom/bereket/alacakverecek/MainActivity;->deleteOld(Ljava/io/File;JZ)V

    return-void
.end method

.method static synthetic access$300(Lcom/bereket/alacakverecek/MainActivity;[Landroid/net/Uri;)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0, p1}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    return-void
.end method

.method static synthetic access$402(Lcom/bereket/alacakverecek/MainActivity;Landroid/webkit/ValueCallback;)Landroid/webkit/ValueCallback;
    .locals 0

    .prologue
    .line 58
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity;->fileCallback:Landroid/webkit/ValueCallback;

    return-object p1
.end method

.method static synthetic access$500(Lcom/bereket/alacakverecek/MainActivity;)Ljava/util/List;
    .locals 1

    .prologue
    .line 58
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMimes:Ljava/util/List;

    return-object v0
.end method

.method static synthetic access$502(Lcom/bereket/alacakverecek/MainActivity;Ljava/util/List;)Ljava/util/List;
    .locals 0

    .prologue
    .line 58
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMimes:Ljava/util/List;

    return-object p1
.end method

.method static synthetic access$602(Lcom/bereket/alacakverecek/MainActivity;Z)Z
    .locals 0

    .prologue
    .line 58
    iput-boolean p1, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMultiple:Z

    return p1
.end method

.method static synthetic access$700(Lcom/bereket/alacakverecek/MainActivity;)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->startCamera()V

    return-void
.end method

.method static synthetic access$800(Lcom/bereket/alacakverecek/MainActivity;)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->startFilePicker()V

    return-void
.end method

.method static synthetic access$900(Lcom/bereket/alacakverecek/MainActivity;)V
    .locals 0

    .prologue
    .line 58
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->showSourceDialog()V

    return-void
.end method

.method private answerFileChooser([Landroid/net/Uri;)V
    .locals 3

    .prologue
    .line 623
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->fileCallback:Landroid/webkit/ValueCallback;

    .line 624
    const/4 v1, 0x0

    iput-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->fileCallback:Landroid/webkit/ValueCallback;

    .line 625
    if-eqz v0, :cond_0

    .line 627
    :try_start_0
    invoke-interface {v0, p1}, Landroid/webkit/ValueCallback;->onReceiveValue(Ljava/lang/Object;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 632
    :cond_0
    :goto_0
    return-void

    .line 628
    :catch_0
    move-exception v0

    .line 629
    const-string v1, "BereketDefter"

    const-string v2, "file callback"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    goto :goto_0
.end method

.method private askExit()V
    .locals 3

    .prologue
    .line 260
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->isFinishing()Z

    move-result v0

    if-nez v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;

    if-eqz v0, :cond_1

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;

    invoke-virtual {v0}, Landroid/app/AlertDialog;->isShowing()Z

    move-result v0

    if-eqz v0, :cond_1

    .line 275
    :cond_0
    :goto_0
    return-void

    .line 262
    :cond_1
    :try_start_0
    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string v1, "\u00c7\u0131k\u0131ls\u0131n m\u0131?"

    .line 263
    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "Evet"

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$3;

    invoke-direct {v2, p0}, Lcom/bereket/alacakverecek/MainActivity$3;-><init>(Lcom/bereket/alacakverecek/MainActivity;)V

    .line 264
    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    const-string v1, "Hay\u0131r"

    const/4 v2, 0x0

    .line 270
    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    .line 271
    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;

    move-result-object v0

    iput-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 272
    :catch_0
    move-exception v0

    .line 273
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->finish()V

    goto :goto_0
.end method

.method private cleanCacheAsync()V
    .locals 3

    .prologue
    .line 362
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getCacheDir()Ljava/io/File;

    move-result-object v0

    .line 363
    new-instance v1, Ljava/lang/Thread;

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$6;

    invoke-direct {v2, p0, v0}, Lcom/bereket/alacakverecek/MainActivity$6;-><init>(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;)V

    const-string v0, "cache-clean"

    invoke-direct {v1, v2, v0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 371
    invoke-virtual {v1}, Ljava/lang/Thread;->start()V

    .line 372
    return-void
.end method

.method private configureWebView(Landroid/webkit/WebView;)V
    .locals 5

    .prologue
    const/4 v4, -0x1

    const/4 v3, 0x1

    const/4 v2, 0x0

    .line 154
    invoke-virtual {p1}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;

    move-result-object v1

    .line 155
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V

    .line 156
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V

    .line 157
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setDatabaseEnabled(Z)V

    .line 158
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setAllowFileAccess(Z)V

    .line 159
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setAllowContentAccess(Z)V

    .line 160
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowFileAccessFromFileURLs(Z)V

    .line 161
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowUniversalAccessFromFileURLs(Z)V

    .line 162
    # v1.8: https sayfadan yerel ağdaki bilgisayara (http://192.168.x.x:47341) Wi‑Fi eşitleme istekleri için 0 = MIXED_CONTENT_ALWAYS_ALLOW
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setMixedContentMode(I)V

    .line 163
    const/16 v0, 0x64

    invoke-virtual {v1, v0}, Landroid/webkit/WebSettings;->setTextZoom(I)V

    .line 164
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setMediaPlaybackRequiresUserGesture(Z)V

    .line 165
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setSupportMultipleWindows(Z)V

    .line 166
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptCanOpenWindowsAutomatically(Z)V

    .line 167
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setSupportZoom(Z)V

    .line 168
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setBuiltInZoomControls(Z)V

    .line 169
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setDisplayZoomControls(Z)V

    .line 170
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setLoadWithOverviewMode(Z)V

    .line 171
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setUseWideViewPort(Z)V

    .line 172
    invoke-virtual {v1, v4}, Landroid/webkit/WebSettings;->setCacheMode(I)V

    .line 173
    invoke-virtual {v1}, Landroid/webkit/WebSettings;->getUserAgentString()Ljava/lang/String;

    move-result-object v0

    .line 174
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    if-nez v0, :cond_0

    const-string v0, ""

    :cond_0
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v2, " BereketDefter/"

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->appVersionName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Landroid/webkit/WebSettings;->setUserAgentString(Ljava/lang/String;)V

    .line 175
    invoke-virtual {p1, v4}, Landroid/webkit/WebView;->setBackgroundColor(I)V

    .line 176
    const/4 v0, 0x2

    invoke-virtual {p1, v0}, Landroid/webkit/WebView;->setOverScrollMode(I)V

    .line 177
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getApplicationInfo()Landroid/content/pm/ApplicationInfo;

    move-result-object v0

    iget v0, v0, Landroid/content/pm/ApplicationInfo;->flags:I

    and-int/lit8 v0, v0, 0x2

    if-eqz v0, :cond_1

    .line 178
    invoke-static {v3}, Landroid/webkit/WebView;->setWebContentsDebuggingEnabled(Z)V

    .line 180
    :cond_1
    return-void
.end method

.method private copyToUri(Ljava/io/File;Landroid/net/Uri;)Z
    .locals 6

    .prologue
    const/4 v3, 0x0

    const/4 v0, 0x0

    .line 771
    .line 774
    :try_start_0
    new-instance v4, Ljava/io/FileInputStream;

    invoke-direct {v4, p1}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_9
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 775
    :try_start_1
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v1

    const-string v2, "w"

    invoke-virtual {v1, p2, v2}, Landroid/content/ContentResolver;->openOutputStream(Landroid/net/Uri;Ljava/lang/String;)Ljava/io/OutputStream;
    :try_end_1
    .catch Ljava/lang/Throwable; {:try_start_1 .. :try_end_1} :catch_a
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    move-result-object v2

    .line 776
    if-nez v2, :cond_2

    .line 786
    if-eqz v4, :cond_0

    :try_start_2
    invoke-virtual {v4}, Ljava/io/InputStream;->close()V
    :try_end_2
    .catch Ljava/io/IOException; {:try_start_2 .. :try_end_2} :catch_3

    .line 787
    :cond_0
    :goto_0
    if-eqz v2, :cond_1

    :try_start_3
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V
    :try_end_3
    .catch Ljava/io/IOException; {:try_start_3 .. :try_end_3} :catch_4

    .line 784
    :cond_1
    :goto_1
    return v0

    .line 777
    :cond_2
    const/high16 v1, 0x10000

    :try_start_4
    new-array v1, v1, [B

    .line 779
    :goto_2
    invoke-virtual {v4, v1}, Ljava/io/InputStream;->read([B)I

    move-result v3

    if-lez v3, :cond_4

    const/4 v5, 0x0

    invoke-virtual {v2, v1, v5, v3}, Ljava/io/OutputStream;->write([BII)V
    :try_end_4
    .catch Ljava/lang/Throwable; {:try_start_4 .. :try_end_4} :catch_0
    .catchall {:try_start_4 .. :try_end_4} :catchall_2

    goto :goto_2

    .line 782
    :catch_0
    move-exception v1

    .line 783
    :goto_3
    :try_start_5
    const-string v3, "BereketDefter"

    const-string v5, "save"

    invoke-static {v3, v5, v1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    :try_end_5
    .catchall {:try_start_5 .. :try_end_5} :catchall_2

    .line 786
    if-eqz v4, :cond_3

    :try_start_6
    invoke-virtual {v4}, Ljava/io/InputStream;->close()V
    :try_end_6
    .catch Ljava/io/IOException; {:try_start_6 .. :try_end_6} :catch_6

    .line 787
    :cond_3
    :goto_4
    if-eqz v2, :cond_1

    :try_start_7
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V
    :try_end_7
    .catch Ljava/io/IOException; {:try_start_7 .. :try_end_7} :catch_1

    goto :goto_1

    :catch_1
    move-exception v1

    goto :goto_1

    .line 780
    :cond_4
    :try_start_8
    invoke-virtual {v2}, Ljava/io/OutputStream;->flush()V
    :try_end_8
    .catch Ljava/lang/Throwable; {:try_start_8 .. :try_end_8} :catch_0
    .catchall {:try_start_8 .. :try_end_8} :catchall_2

    .line 781
    const/4 v0, 0x1

    .line 786
    if-eqz v4, :cond_5

    :try_start_9
    invoke-virtual {v4}, Ljava/io/InputStream;->close()V
    :try_end_9
    .catch Ljava/io/IOException; {:try_start_9 .. :try_end_9} :catch_5

    .line 787
    :cond_5
    :goto_5
    if-eqz v2, :cond_1

    :try_start_a
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V
    :try_end_a
    .catch Ljava/io/IOException; {:try_start_a .. :try_end_a} :catch_2

    goto :goto_1

    :catch_2
    move-exception v1

    goto :goto_1

    .line 786
    :catchall_0
    move-exception v0

    move-object v2, v3

    move-object v4, v3

    :goto_6
    if-eqz v4, :cond_6

    :try_start_b
    invoke-virtual {v4}, Ljava/io/InputStream;->close()V
    :try_end_b
    .catch Ljava/io/IOException; {:try_start_b .. :try_end_b} :catch_7

    .line 787
    :cond_6
    :goto_7
    if-eqz v2, :cond_7

    :try_start_c
    invoke-virtual {v2}, Ljava/io/OutputStream;->close()V
    :try_end_c
    .catch Ljava/io/IOException; {:try_start_c .. :try_end_c} :catch_8

    .line 788
    :cond_7
    :goto_8
    throw v0

    .line 786
    :catch_3
    move-exception v1

    goto :goto_0

    .line 787
    :catch_4
    move-exception v1

    goto :goto_1

    .line 786
    :catch_5
    move-exception v1

    goto :goto_5

    :catch_6
    move-exception v1

    goto :goto_4

    :catch_7
    move-exception v1

    goto :goto_7

    .line 787
    :catch_8
    move-exception v1

    goto :goto_8

    .line 786
    :catchall_1
    move-exception v0

    move-object v2, v3

    goto :goto_6

    :catchall_2
    move-exception v0

    goto :goto_6

    .line 782
    :catch_9
    move-exception v1

    move-object v2, v3

    move-object v4, v3

    goto :goto_3

    :catch_a
    move-exception v1

    move-object v2, v3

    goto :goto_3
.end method

.method static decodeBase64(Ljava/lang/String;)[B
    .locals 3

    .prologue
    .line 354
    invoke-static {p0}, Lcom/bereket/alacakverecek/Util;->stripDataUrl(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 355
    const/4 v0, 0x0

    .line 356
    invoke-static {v1}, Lcom/bereket/alacakverecek/Util;->isUrlSafeBase64(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_0

    const/16 v0, 0x8

    .line 357
    :cond_0
    invoke-static {v1, v0}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v0

    return-object v0
.end method

.method private static deleteOld(Ljava/io/File;JZ)V
    .locals 5

    .prologue
    .line 376
    :try_start_0
    invoke-virtual {p0}, Ljava/io/File;->listFiles()[Ljava/io/File;

    move-result-object v1

    .line 377
    if-eqz v1, :cond_0

    array-length v2, v1

    const/4 v0, 0x0

    :goto_0
    if-ge v0, v2, :cond_0

    aget-object v3, v1, v0

    const/4 v4, 0x1

    invoke-static {v3, p1, p2, v4}, Lcom/bereket/alacakverecek/MainActivity;->deleteOld(Ljava/io/File;JZ)V

    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    .line 378
    :cond_0
    if-eqz p3, :cond_2

    invoke-virtual {p0}, Ljava/io/File;->lastModified()J

    move-result-wide v0

    cmp-long v0, v0, p1

    if-gez v0, :cond_2

    .line 379
    invoke-virtual {p0}, Ljava/io/File;->listFiles()[Ljava/io/File;

    move-result-object v0

    .line 380
    if-eqz v0, :cond_1

    array-length v0, v0

    if-nez v0, :cond_2

    :cond_1
    invoke-virtual {p0}, Ljava/io/File;->delete()Z
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 384
    :cond_2
    :goto_1
    return-void

    .line 382
    :catch_0
    move-exception v0

    goto :goto_1
.end method

.method private evalJs(Ljava/lang/String;)V
    .locals 1

    .prologue
    .line 331
    new-instance v0, Lcom/bereket/alacakverecek/MainActivity$5;

    invoke-direct {v0, p0, p1}, Lcom/bereket/alacakverecek/MainActivity$5;-><init>(Lcom/bereket/alacakverecek/MainActivity;Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 337
    return-void
.end method

.method private hasPermission(Ljava/lang/String;)Z
    .locals 1

    .prologue
    .line 314
    invoke-virtual {p0, p1}, Lcom/bereket/alacakverecek/MainActivity;->checkSelfPermission(Ljava/lang/String;)I

    move-result v0

    if-nez v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method private launchCamera()V
    .locals 7

    .prologue
    const/4 v6, 0x0

    .line 673
    :try_start_0
    new-instance v0, Ljava/io/File;

    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getCacheDir()Ljava/io/File;

    move-result-object v1

    const-string v2, "camera"

    invoke-direct {v0, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 674
    invoke-virtual {v0}, Ljava/io/File;->isDirectory()Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    move-result v1

    if-nez v1, :cond_0

    new-instance v0, Ljava/io/IOException;

    const-string v1, "mkdirs camera"

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_0
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_0} :catch_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_1

    .line 684
    :catch_0
    move-exception v0

    .line 685
    const-string v0, "Kamera uygulamas\u0131 bulunamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    .line 686
    invoke-direct {p0, v6}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    .line 692
    :goto_0
    return-void

    .line 675
    :cond_0
    :try_start_1
    new-instance v1, Ljava/io/File;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "Foto_"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    new-instance v3, Ljava/text/SimpleDateFormat;

    const-string v4, "yyyyMMdd_HHmmss"

    sget-object v5, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-direct {v3, v4, v5}, Ljava/text/SimpleDateFormat;-><init>(Ljava/lang/String;Ljava/util/Locale;)V

    new-instance v4, Ljava/util/Date;

    invoke-direct {v4}, Ljava/util/Date;-><init>()V

    .line 676
    invoke-virtual {v3, v4}, Ljava/text/SimpleDateFormat;->format(Ljava/util/Date;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, ".jpg"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-direct {v1, v0, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    iput-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    .line 677
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v0

    if-nez v0, :cond_1

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->createNewFile()Z

    .line 678
    :cond_1
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-static {p0, v0}, Lcom/bereket/alacakverecek/FilesProvider;->uriFor(Landroid/content/Context;Ljava/io/File;)Landroid/net/Uri;

    move-result-object v0

    iput-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraUri:Landroid/net/Uri;

    .line 679
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.media.action.IMAGE_CAPTURE"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 680
    const-string v1, "output"

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraUri:Landroid/net/Uri;

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 681
    const-string v1, "photo"

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraUri:Landroid/net/Uri;

    invoke-static {v1, v2}, Landroid/content/ClipData;->newRawUri(Ljava/lang/CharSequence;Landroid/net/Uri;)Landroid/content/ClipData;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setClipData(Landroid/content/ClipData;)V

    .line 682
    const/4 v1, 0x3

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 683
    const/16 v1, 0x3ea

    invoke-virtual {p0, v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_1
    .catch Landroid/content/ActivityNotFoundException; {:try_start_1 .. :try_end_1} :catch_0
    .catch Ljava/lang/Throwable; {:try_start_1 .. :try_end_1} :catch_1

    goto :goto_0

    .line 687
    :catch_1
    move-exception v0

    .line 688
    const-string v1, "BereketDefter"

    const-string v2, "camera"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 689
    const-string v0, "Kamera a\u00e7\u0131lamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    .line 690
    invoke-direct {p0, v6}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    goto :goto_0
.end method

.method private notifySaved(Z)V
    .locals 1

    .prologue
    .line 793
    new-instance v0, Lcom/bereket/alacakverecek/MainActivity$10;

    invoke-direct {v0, p0, p1}, Lcom/bereket/alacakverecek/MainActivity$10;-><init>(Lcom/bereket/alacakverecek/MainActivity;Z)V

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 806
    return-void
.end method

.method private printHtmlOnUi(Ljava/lang/String;Ljava/lang/String;)V
    .locals 6

    .prologue
    const/4 v5, 0x0

    .line 839
    if-eqz p2, :cond_0

    invoke-virtual {p2}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v0

    if-nez v0, :cond_2

    :cond_0
    const-string v0, "Bereket Defter"

    move-object v1, v0

    .line 840
    :goto_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    if-eqz v0, :cond_1

    .line 841
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->destroy()V

    .line 842
    iput-object v5, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    .line 846
    :cond_1
    :try_start_0
    new-instance v0, Landroid/webkit/WebView;

    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 851
    invoke-direct {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->configureWebView(Landroid/webkit/WebView;)V

    .line 852
    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$11;

    const/4 v3, 0x1

    invoke-direct {v2, p0, v3, v0, v1}, Lcom/bereket/alacakverecek/MainActivity$11;-><init>(Lcom/bereket/alacakverecek/MainActivity;ZLandroid/webkit/WebView;Ljava/lang/String;)V

    invoke-virtual {v0, v2}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    .line 868
    iput-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    .line 869
    const-string v1, "https://appassets.androidplatform.net/www/"

    if-nez p1, :cond_3

    const-string v2, ""

    :goto_1
    const-string v3, "text/html"

    const-string v4, "UTF-8"

    invoke-virtual/range {v0 .. v5}, Landroid/webkit/WebView;->loadDataWithBaseURL(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    .line 870
    :goto_2
    return-void

    .line 839
    :cond_2
    invoke-virtual {p2}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    move-object v1, v0

    goto :goto_0

    .line 847
    :catch_0
    move-exception v0

    .line 848
    const-string v0, "Yazd\u0131rma ba\u015flat\u0131lamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    goto :goto_2

    :cond_3
    move-object v2, p1

    .line 869
    goto :goto_1
.end method

.method static serveAsset(Landroid/content/Context;Landroid/net/Uri;)Landroid/webkit/WebResourceResponse;
    .locals 10

    .prologue
    const/4 v7, 0x0

    .line 416
    invoke-virtual {p1}, Landroid/net/Uri;->getPath()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/bereket/alacakverecek/Util;->assetPathForUrlPath(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    .line 417
    new-instance v5, Ljava/util/HashMap;

    invoke-direct {v5}, Ljava/util/HashMap;-><init>()V

    .line 418
    const-string v0, "Cache-Control"

    const-string v1, "no-cache"

    invoke-interface {v5, v0, v1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 419
    const-string v0, "Access-Control-Allow-Origin"

    const-string v1, "*"

    invoke-interface {v5, v0, v1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 420
    const-string v0, "X-Content-Type-Options"

    const-string v1, "nosniff"

    invoke-interface {v5, v0, v1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 421
    if-eqz v8, :cond_2

    .line 422
    sget-object v0, Lcom/bereket/alacakverecek/MainActivity;->activeBundle:Ljava/io/File;

    .line 423
    if-eqz v0, :cond_1

    const-string v1, "www/"

    invoke-virtual {v8, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_1

    .line 425
    :try_start_0
    new-instance v9, Ljava/io/File;

    const/4 v1, 0x4

    invoke-virtual {v8, v1}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v9, v0, v1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 426
    invoke-virtual {v9}, Ljava/io/File;->isFile()Z

    move-result v1

    if-eqz v1, :cond_1

    invoke-virtual {v9}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;

    move-result-object v1

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v2, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_1

    .line 427
    const-string v0, "application/octet-stream"

    invoke-static {v8, v0}, Lcom/bereket/alacakverecek/Util;->mimeForNameOr(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 428
    invoke-static {v1}, Lcom/bereket/alacakverecek/Util;->isTextMime(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    const-string v2, "UTF-8"

    .line 429
    :goto_0
    new-instance v0, Landroid/webkit/WebResourceResponse;

    const/16 v3, 0xc8

    const-string v4, "OK"

    new-instance v6, Ljava/io/FileInputStream;

    invoke-direct {v6, v9}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    invoke-direct/range {v0 .. v6}, Landroid/webkit/WebResourceResponse;-><init>(Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;Ljava/util/Map;Ljava/io/InputStream;)V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    .line 444
    :goto_1
    return-object v0

    :cond_0
    move-object v2, v7

    .line 428
    goto :goto_0

    .line 431
    :catch_0
    move-exception v0

    .line 436
    :cond_1
    :try_start_1
    invoke-virtual {p0}, Landroid/content/Context;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v0

    invoke-virtual {v0, v8}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v6

    .line 437
    const-string v0, "application/octet-stream"

    invoke-static {v8, v0}, Lcom/bereket/alacakverecek/Util;->mimeForNameOr(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 438
    invoke-static {v1}, Lcom/bereket/alacakverecek/Util;->isTextMime(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_3

    const-string v2, "UTF-8"

    .line 439
    :goto_2
    new-instance v0, Landroid/webkit/WebResourceResponse;

    const/16 v3, 0xc8

    const-string v4, "OK"

    invoke-direct/range {v0 .. v6}, Landroid/webkit/WebResourceResponse;-><init>(Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;Ljava/util/Map;Ljava/io/InputStream;)V
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_1

    goto :goto_1

    .line 440
    :catch_1
    move-exception v0

    .line 444
    :cond_2
    new-instance v0, Landroid/webkit/WebResourceResponse;

    const-string v1, "text/plain"

    const-string v2, "UTF-8"

    const/16 v3, 0x194

    const-string v4, "Not Found"

    new-instance v6, Ljava/io/ByteArrayInputStream;

    new-instance v7, Ljava/lang/StringBuilder;

    invoke-direct {v7}, Ljava/lang/StringBuilder;-><init>()V

    const-string v8, "404 "

    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    .line 445
    invoke-virtual {p1}, Landroid/net/Uri;->getPath()Ljava/lang/String;

    move-result-object v8

    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/String;->getBytes()[B

    move-result-object v7

    invoke-direct {v6, v7}, Ljava/io/ByteArrayInputStream;-><init>([B)V

    invoke-direct/range {v0 .. v6}, Landroid/webkit/WebResourceResponse;-><init>(Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;Ljava/util/Map;Ljava/io/InputStream;)V

    goto :goto_1

    :cond_3
    move-object v2, v7

    .line 438
    goto :goto_2
.end method

.method private showSourceDialog()V
    .locals 4

    .prologue
    const/4 v3, 0x0

    .line 635
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->isFinishing()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 636
    invoke-direct {p0, v3}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    .line 660
    :goto_0
    return-void

    .line 639
    :cond_0
    const/4 v0, 0x2

    new-array v1, v0, [Ljava/lang/String;

    const/4 v0, 0x0

    const-string v2, "Foto\u011fraf \u00e7ek (kamera)"

    aput-object v2, v1, v0

    const/4 v2, 0x1

    iget-boolean v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMultiple:Z

    if-eqz v0, :cond_1

    const-string v0, "Dosya se\u00e7 (birden \u00e7ok)"

    :goto_1
    aput-object v0, v1, v2

    .line 641
    :try_start_0
    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string v2, "Dosya ekle"

    .line 642
    invoke-virtual {v0, v2}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$8;

    invoke-direct {v2, p0}, Lcom/bereket/alacakverecek/MainActivity$8;-><init>(Lcom/bereket/alacakverecek/MainActivity;)V

    .line 643
    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setItems([Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$7;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$7;-><init>(Lcom/bereket/alacakverecek/MainActivity;)V

    .line 650
    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    .line 656
    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 657
    :catch_0
    move-exception v0

    .line 658
    invoke-direct {p0, v3}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    goto :goto_0

    .line 639
    :cond_1
    const-string v0, "Dosya se\u00e7"

    goto :goto_1
.end method

.method private startCamera()V
    .locals 3

    .prologue
    const/4 v1, 0x1

    .line 663
    const-string v0, "android.permission.CAMERA"

    invoke-direct {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->hasPermission(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_0

    .line 664
    iput-boolean v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraPermissionPending:Z

    .line 665
    new-array v0, v1, [Ljava/lang/String;

    const/4 v1, 0x0

    const-string v2, "android.permission.CAMERA"

    aput-object v2, v0, v1

    const/16 v1, 0x7d1

    invoke-virtual {p0, v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->requestPermissions([Ljava/lang/String;I)V

    .line 669
    :goto_0
    return-void

    .line 668
    :cond_0
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->launchCamera()V

    goto :goto_0
.end method

.method private startFilePicker()V
    .locals 6

    .prologue
    const/4 v5, 0x0

    const/4 v3, 0x0

    const/4 v4, 0x1

    .line 695
    new-instance v1, Landroid/content/Intent;

    const-string v0, "android.intent.action.GET_CONTENT"

    invoke-direct {v1, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 696
    const-string v0, "android.intent.category.OPENABLE"

    invoke-virtual {v1, v0}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    .line 697
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMimes:Ljava/util/List;

    invoke-interface {v0}, Ljava/util/List;->size()I

    move-result v0

    if-ne v0, v4, :cond_2

    .line 698
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMimes:Ljava/util/List;

    invoke-interface {v0, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    invoke-virtual {v1, v0}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    .line 703
    :cond_0
    :goto_0
    iget-boolean v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMultiple:Z

    if-eqz v0, :cond_1

    const-string v0, "android.intent.extra.ALLOW_MULTIPLE"

    invoke-virtual {v1, v0, v4}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 705
    :cond_1
    const/16 v0, 0x3e9

    :try_start_0
    invoke-virtual {p0, v1, v0}, Lcom/bereket/alacakverecek/MainActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_0
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_0} :catch_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_2

    .line 717
    :goto_1
    return-void

    .line 700
    :cond_2
    const-string v0, "*/*"

    invoke-virtual {v1, v0}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    .line 701
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMimes:Ljava/util/List;

    invoke-interface {v0}, Ljava/util/List;->size()I

    move-result v0

    if-le v0, v4, :cond_0

    const-string v2, "android.intent.extra.MIME_TYPES"

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMimes:Ljava/util/List;

    new-array v3, v3, [Ljava/lang/String;

    invoke-interface {v0, v3}, Ljava/util/List;->toArray([Ljava/lang/Object;)[Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Ljava/lang/String;

    invoke-virtual {v1, v2, v0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;[Ljava/lang/String;)Landroid/content/Intent;

    goto :goto_0

    .line 706
    :catch_0
    move-exception v0

    .line 708
    :try_start_1
    const-string v0, "Dosya se\u00e7"

    invoke-static {v1, v0}, Landroid/content/Intent;->createChooser(Landroid/content/Intent;Ljava/lang/CharSequence;)Landroid/content/Intent;

    move-result-object v0

    const/16 v1, 0x3e9

    invoke-virtual {p0, v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_1
    .catch Ljava/lang/Throwable; {:try_start_1 .. :try_end_1} :catch_1

    goto :goto_1

    .line 709
    :catch_1
    move-exception v0

    .line 710
    const-string v0, "Dosya se\u00e7ici bulunamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    .line 711
    invoke-direct {p0, v5}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    goto :goto_1

    .line 713
    :catch_2
    move-exception v0

    .line 714
    const-string v1, "BereketDefter"

    const-string v2, "picker"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 715
    invoke-direct {p0, v5}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    goto :goto_1
.end method

.method private startPrintJob(Landroid/webkit/WebView;Ljava/lang/String;)V
    .locals 4

    .prologue
    .line 873
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->isFinishing()Z

    move-result v0

    if-nez v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    if-eq p1, v0, :cond_1

    .line 885
    :cond_0
    :goto_0
    return-void

    .line 875
    :cond_1
    :try_start_0
    const-string v0, "print"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/print/PrintManager;

    .line 876
    invoke-virtual {p1, p2}, Landroid/webkit/WebView;->createPrintDocumentAdapter(Ljava/lang/String;)Landroid/print/PrintDocumentAdapter;

    move-result-object v1

    .line 877
    new-instance v2, Landroid/print/PrintAttributes$Builder;

    invoke-direct {v2}, Landroid/print/PrintAttributes$Builder;-><init>()V

    sget-object v3, Landroid/print/PrintAttributes$MediaSize;->ISO_A4:Landroid/print/PrintAttributes$MediaSize;

    .line 878
    invoke-virtual {v2, v3}, Landroid/print/PrintAttributes$Builder;->setMediaSize(Landroid/print/PrintAttributes$MediaSize;)Landroid/print/PrintAttributes$Builder;

    move-result-object v2

    .line 879
    invoke-virtual {v2}, Landroid/print/PrintAttributes$Builder;->build()Landroid/print/PrintAttributes;

    move-result-object v2

    .line 880
    invoke-virtual {v0, p2, v1, v2}, Landroid/print/PrintManager;->print(Ljava/lang/String;Landroid/print/PrintDocumentAdapter;Landroid/print/PrintAttributes;)Landroid/print/PrintJob;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 881
    :catch_0
    move-exception v0

    .line 882
    const-string v1, "BereketDefter"

    const-string v2, "print"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 883
    const-string v0, "Yazd\u0131rma ba\u015flat\u0131lamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    goto :goto_0
.end method

.method private styleSystemBars()V
    .locals 3

    .prologue
    .line 143
    :try_start_0
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    .line 144
    const/high16 v1, 0x4000000

    invoke-virtual {v0, v1}, Landroid/view/Window;->clearFlags(I)V

    .line 145
    const/high16 v1, -0x80000000

    invoke-virtual {v0, v1}, Landroid/view/Window;->addFlags(I)V

    .line 146
    const v1, -0xf9aec1

    invoke-virtual {v0, v1}, Landroid/view/Window;->setStatusBarColor(I)V

    .line 147
    const v1, -0xf9aec1

    invoke-virtual {v0, v1}, Landroid/view/Window;->setNavigationBarColor(I)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 151
    :goto_0
    return-void

    .line 148
    :catch_0
    move-exception v0

    .line 149
    const-string v1, "BereketDefter"

    const-string v2, "bars"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    goto :goto_0
.end method


# virtual methods
.method appVersionName()Ljava/lang/String;
    .locals 3

    .prologue
    .line 295
    :try_start_0
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v0

    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getPackageName()Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Landroid/content/pm/PackageManager;->getPackageInfo(Ljava/lang/String;I)Landroid/content/pm/PackageInfo;

    move-result-object v0

    iget-object v0, v0, Landroid/content/pm/PackageInfo;->versionName:Ljava/lang/String;

    .line 296
    if-eqz v0, :cond_0

    .line 298
    :goto_0
    return-object v0

    .line 296
    :cond_0
    const-string v0, ""
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 297
    :catch_0
    move-exception v0

    .line 298
    const-string v0, ""

    goto :goto_0
.end method

.method canInstallPackages()Z
    .locals 3

    .prologue
    .line 286
    :try_start_0
    const-class v0, Landroid/content/pm/PackageManager;

    const-string v1, "canRequestPackageInstalls"

    const/4 v2, 0x0

    new-array v2, v2, [Ljava/lang/Class;

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v1

    const/4 v2, 0x0

    new-array v2, v2, [Ljava/lang/Object;

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    .line 287
    sget-object v1, Ljava/lang/Boolean;->TRUE:Ljava/lang/Boolean;

    invoke-virtual {v1, v0}, Ljava/lang/Boolean;->equals(Ljava/lang/Object;)Z
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    move-result v0

    .line 289
    :goto_0
    return v0

    .line 288
    :catch_0
    move-exception v0

    .line 289
    const/4 v0, 0x1

    goto :goto_0
.end method

.method isOwnOrigin(Landroid/net/Uri;)Z
    .locals 2

    .prologue
    .line 280
    if-eqz p1, :cond_0

    const-string v0, "https"

    invoke-virtual {p1}, Landroid/net/Uri;->getScheme()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    const-string v0, "appassets.androidplatform.net"

    invoke-virtual {p1}, Landroid/net/Uri;->getHost()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method maybeAskNotificationPermission()V
    .locals 4

    .prologue
    const/4 v3, 0x1

    const/4 v2, 0x0

    .line 319
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x21

    if-lt v0, v1, :cond_0

    const-string v0, "android.permission.POST_NOTIFICATIONS"

    invoke-direct {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->hasPermission(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_1

    .line 328
    :cond_0
    :goto_0
    return-void

    .line 320
    :cond_1
    const-string v0, "bereket"

    invoke-virtual {p0, v0, v2}, Lcom/bereket/alacakverecek/MainActivity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v0

    .line 321
    const-string v1, "notifAsked"

    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    move-result v1

    if-nez v1, :cond_0

    .line 322
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    const-string v1, "notifAsked"

    invoke-interface {v0, v1, v3}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V

    .line 324
    const/4 v0, 0x1

    :try_start_0
    new-array v0, v0, [Ljava/lang/String;

    const/4 v1, 0x0

    const-string v2, "android.permission.POST_NOTIFICATIONS"

    aput-object v2, v0, v1

    const/16 v1, 0x7d2

    invoke-virtual {p0, v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->requestPermissions([Ljava/lang/String;I)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 325
    :catch_0
    move-exception v0

    .line 326
    const-string v1, "BereketDefter"

    const-string v2, "notif perm"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    goto :goto_0
.end method

.method protected onActivityResult(IILandroid/content/Intent;)V
    .locals 8

    .prologue
    const-wide/16 v4, 0x0

    const/4 v7, 0x1

    const/4 v2, -0x1

    const/4 v3, 0x0

    const/4 v1, 0x0

    .line 721
    invoke-super {p0, p1, p2, p3}, Landroid/app/Activity;->onActivityResult(IILandroid/content/Intent;)V

    .line 722
    const/16 v0, 0x3e9

    if-ne p1, v0, :cond_4

    .line 724
    if-ne p2, v2, :cond_d

    if-eqz p3, :cond_d

    .line 725
    new-instance v2, Ljava/util/ArrayList;

    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 726
    invoke-virtual {p3}, Landroid/content/Intent;->getClipData()Landroid/content/ClipData;

    move-result-object v4

    .line 727
    if-eqz v4, :cond_1

    move v0, v1

    .line 728
    :goto_0
    invoke-virtual {v4}, Landroid/content/ClipData;->getItemCount()I

    move-result v5

    if-ge v0, v5, :cond_1

    .line 729
    invoke-virtual {v4, v0}, Landroid/content/ClipData;->getItemAt(I)Landroid/content/ClipData$Item;

    move-result-object v5

    invoke-virtual {v5}, Landroid/content/ClipData$Item;->getUri()Landroid/net/Uri;

    move-result-object v5

    .line 730
    if-eqz v5, :cond_0

    invoke-interface {v2, v5}, Ljava/util/List;->contains(Ljava/lang/Object;)Z

    move-result v6

    if-nez v6, :cond_0

    invoke-interface {v2, v5}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 728
    :cond_0
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    .line 733
    :cond_1
    invoke-interface {v2}, Ljava/util/List;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_2

    invoke-virtual {p3}, Landroid/content/Intent;->getData()Landroid/net/Uri;

    move-result-object v0

    if-eqz v0, :cond_2

    invoke-virtual {p3}, Landroid/content/Intent;->getData()Landroid/net/Uri;

    move-result-object v0

    invoke-interface {v2, v0}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 734
    :cond_2
    iget-boolean v0, p0, Lcom/bereket/alacakverecek/MainActivity;->chooserMultiple:Z

    if-nez v0, :cond_e

    invoke-interface {v2}, Ljava/util/List;->size()I

    move-result v0

    if-le v0, v7, :cond_e

    invoke-interface {v2, v1, v7}, Ljava/util/List;->subList(II)Ljava/util/List;

    move-result-object v0

    .line 735
    :goto_1
    invoke-interface {v0}, Ljava/util/List;->isEmpty()Z

    move-result v2

    if-nez v2, :cond_d

    new-array v1, v1, [Landroid/net/Uri;

    invoke-interface {v0, v1}, Ljava/util/List;->toArray([Ljava/lang/Object;)[Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Landroid/net/Uri;

    .line 737
    :goto_2
    invoke-direct {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    .line 768
    :cond_3
    :goto_3
    return-void

    .line 738
    :cond_4
    const/16 v0, 0x3ea

    if-ne p1, v0, :cond_8

    .line 740
    if-ne p2, v2, :cond_7

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    if-eqz v0, :cond_7

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->isFile()Z

    move-result v0

    if-eqz v0, :cond_7

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->length()J

    move-result-wide v0

    cmp-long v0, v0, v4

    if-lez v0, :cond_7

    .line 742
    const/4 v0, 0x1

    :try_start_0
    new-array v0, v0, [Landroid/net/Uri;

    const/4 v2, 0x0

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraUri:Landroid/net/Uri;

    if-eqz v1, :cond_6

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraUri:Landroid/net/Uri;

    :goto_4
    aput-object v1, v0, v2
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    move-object v3, v0

    .line 749
    :cond_5
    :goto_5
    invoke-direct {p0, v3}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    goto :goto_3

    .line 742
    :cond_6
    :try_start_1
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-static {p0, v1}, Lcom/bereket/alacakverecek/FilesProvider;->uriFor(Landroid/content/Context;Ljava/io/File;)Landroid/net/Uri;
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_0

    move-result-object v1

    goto :goto_4

    .line 746
    :cond_7
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    if-eqz v0, :cond_5

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->isFile()Z

    move-result v0

    if-eqz v0, :cond_5

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->length()J

    move-result-wide v0

    cmp-long v0, v0, v4

    if-nez v0, :cond_5

    .line 747
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->delete()Z

    goto :goto_5

    .line 750
    :cond_8
    const/16 v0, 0x3eb

    if-ne p1, v0, :cond_3

    .line 751
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingSaveFile:Ljava/io/File;

    .line 752
    iput-object v3, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingSaveFile:Ljava/io/File;

    .line 753
    if-ne p2, v2, :cond_9

    if-eqz p3, :cond_9

    invoke-virtual {p3}, Landroid/content/Intent;->getData()Landroid/net/Uri;

    move-result-object v3

    .line 754
    :cond_9
    if-eqz v0, :cond_a

    if-eqz v3, :cond_a

    invoke-virtual {v0}, Ljava/io/File;->isFile()Z

    move-result v2

    if-nez v2, :cond_c

    .line 755
    :cond_a
    if-eqz v0, :cond_b

    invoke-virtual {v0}, Ljava/io/File;->delete()Z

    .line 756
    :cond_b
    invoke-direct {p0, v1}, Lcom/bereket/alacakverecek/MainActivity;->notifySaved(Z)V

    goto :goto_3

    .line 759
    :cond_c
    new-instance v1, Ljava/lang/Thread;

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$9;

    invoke-direct {v2, p0, v0, v3}, Lcom/bereket/alacakverecek/MainActivity$9;-><init>(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;Landroid/net/Uri;)V

    const-string v0, "save-file"

    invoke-direct {v1, v2, v0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 766
    invoke-virtual {v1}, Ljava/lang/Thread;->start()V

    goto/16 :goto_3

    .line 743
    :catch_0
    move-exception v0

    goto :goto_5

    :cond_d
    move-object v0, v3

    goto/16 :goto_2

    :cond_e
    move-object v0, v2

    goto/16 :goto_1
.end method

.method public onBackPressed()V
    .locals 3

    .prologue
    .line 244
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    if-nez v0, :cond_1

    .line 245
    invoke-super {p0}, Landroid/app/Activity;->onBackPressed()V

    .line 257
    :cond_0
    :goto_0
    return-void

    .line 248
    :cond_1
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;

    if-eqz v0, :cond_2

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;

    invoke-virtual {v0}, Landroid/app/AlertDialog;->isShowing()Z

    move-result v0

    if-nez v0, :cond_0

    .line 249
    :cond_2
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    const-string v1, "(function(){try{return !!window.onAndroidBack && window.onAndroidBack()===true;}catch(e){return false;}})()"

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$2;

    invoke-direct {v2, p0}, Lcom/bereket/alacakverecek/MainActivity$2;-><init>(Lcom/bereket/alacakverecek/MainActivity;)V

    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V

    goto :goto_0
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4

    .prologue
    const/4 v2, -0x1

    const/16 v3, 0x30

    .line 100
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 101
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->styleSystemBars()V

    .line 103
    :try_start_0
    new-instance v0, Landroid/webkit/WebView;

    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 115
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    new-instance v1, Landroid/view/ViewGroup$LayoutParams;

    invoke-direct {v1, v2, v2}, Landroid/view/ViewGroup$LayoutParams;-><init>(II)V

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    .line 117
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->setContentView(Landroid/view/View;)V

    .line 118
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    invoke-direct {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->configureWebView(Landroid/webkit/WebView;)V

    .line 119
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$AppClient;

    const/4 v2, 0x0

    invoke-direct {v1, p0, v2}, Lcom/bereket/alacakverecek/MainActivity$AppClient;-><init>(Lcom/bereket/alacakverecek/MainActivity;Z)V

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    .line 120
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;-><init>(Lcom/bereket/alacakverecek/MainActivity;)V

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebChromeClient(Landroid/webkit/WebChromeClient;)V

    .line 121
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$Bridge;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$Bridge;-><init>(Lcom/bereket/alacakverecek/MainActivity;)V

    const-string v2, "AndroidBridge"

    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V

    .line 122
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    new-instance v1, Lcom/bereket/alacakverecek/MainActivity$1;

    invoke-direct {v1, p0}, Lcom/bereket/alacakverecek/MainActivity$1;-><init>(Lcom/bereket/alacakverecek/MainActivity;)V

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setDownloadListener(Landroid/webkit/DownloadListener;)V

    .line 135
    invoke-static {p0}, Lcom/bereket/alacakverecek/Reminders;->ensureChannel(Landroid/content/Context;)V

    .line 136
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->cleanCacheAsync()V

    .line 137
    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->appVersionName()Ljava/lang/String;

    move-result-object v0

    invoke-static {p0, v0}, Lcom/bereket/alacakverecek/Updates;->resolveActive(Landroid/content/Context;Ljava/lang/String;)Ljava/io/File;

    move-result-object v0

    sput-object v0, Lcom/bereket/alacakverecek/MainActivity;->activeBundle:Ljava/io/File;

    .line 138
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    const-string v1, "https://appassets.androidplatform.net/www/index.html"

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    .line 139
    :goto_0
    return-void

    .line 104
    :catch_0
    move-exception v0

    .line 106
    const-string v1, "BereketDefter"

    const-string v2, "WebView"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 107
    new-instance v0, Landroid/widget/TextView;

    invoke-direct {v0, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    .line 108
    const-string v1, "Android System WebView bulunamad\u0131 veya g\u00fcncelleniyor.\nL\u00fctfen Play Store\'dan \"Android System WebView\" uygulamas\u0131n\u0131 g\u00fcncelleyip tekrar a\u00e7\u0131n."

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 110
    const/16 v1, 0x11

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setGravity(I)V

    .line 111
    invoke-virtual {v0, v3, v3, v3, v3}, Landroid/widget/TextView;->setPadding(IIII)V

    .line 112
    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->setContentView(Landroid/view/View;)V

    goto :goto_0
.end method

.method protected onDestroy()V
    .locals 3

    .prologue
    const/4 v2, 0x0

    .line 208
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;

    invoke-virtual {v0}, Landroid/app/AlertDialog;->isShowing()Z

    move-result v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->exitDialog:Landroid/app/AlertDialog;

    invoke-virtual {v0}, Landroid/app/AlertDialog;->dismiss()V

    .line 209
    :cond_0
    invoke-direct {p0, v2}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    .line 210
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    if-eqz v0, :cond_1

    .line 211
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->destroy()V

    .line 212
    iput-object v2, p0, Lcom/bereket/alacakverecek/MainActivity;->printWebView:Landroid/webkit/WebView;

    .line 214
    :cond_1
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    if-eqz v0, :cond_3

    .line 215
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getParent()Landroid/view/ViewParent;

    move-result-object v0

    check-cast v0, Landroid/view/ViewGroup;

    .line 216
    if-eqz v0, :cond_2

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {v0, v1}, Landroid/view/ViewGroup;->removeView(Landroid/view/View;)V

    .line 217
    :cond_2
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->destroy()V

    .line 218
    iput-object v2, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    .line 220
    :cond_3
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V

    .line 221
    return-void
.end method

.method protected onNewIntent(Landroid/content/Intent;)V
    .locals 5

    .prologue
    const/4 v1, 0x0

    .line 184
    invoke-super {p0, p1}, Landroid/app/Activity;->onNewIntent(Landroid/content/Intent;)V

    .line 185
    invoke-virtual {p0, p1}, Lcom/bereket/alacakverecek/MainActivity;->setIntent(Landroid/content/Intent;)V

    .line 187
    if-eqz p1, :cond_1

    const-string v0, "reminderId"

    invoke-virtual {p1, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 188
    :goto_0
    if-eqz v0, :cond_0

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    if-eqz v2, :cond_0

    .line 189
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "window.onAndroidReminder && window.onAndroidReminder("

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-static {v0}, Lcom/bereket/alacakverecek/Util;->jsString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v3, ")"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0, v1}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V

    .line 192
    :cond_0
    return-void

    :cond_1
    move-object v0, v1

    .line 187
    goto :goto_0
.end method

.method protected onPause()V
    .locals 1

    .prologue
    .line 202
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->onPause()V

    .line 203
    :cond_0
    invoke-super {p0}, Landroid/app/Activity;->onPause()V

    .line 204
    return-void
.end method

.method public onRequestPermissionsResult(I[Ljava/lang/String;[I)V
    .locals 5

    .prologue
    const/4 v4, 0x0

    const/4 v1, 0x1

    const/4 v2, 0x0

    .line 810
    if-eqz p3, :cond_1

    array-length v0, p3

    if-lez v0, :cond_1

    aget v0, p3, v2

    if-nez v0, :cond_1

    move v0, v1

    .line 812
    :goto_0
    const/16 v3, 0x7d1

    if-ne p1, v3, :cond_4

    .line 813
    iget-boolean v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraPermissionPending:Z

    if-nez v1, :cond_2

    .line 834
    :cond_0
    :goto_1
    return-void

    :cond_1
    move v0, v2

    .line 810
    goto :goto_0

    .line 814
    :cond_2
    iput-boolean v2, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraPermissionPending:Z

    .line 815
    if-eqz v0, :cond_3

    .line 816
    invoke-direct {p0}, Lcom/bereket/alacakverecek/MainActivity;->launchCamera()V

    goto :goto_1

    .line 818
    :cond_3
    const-string v0, "Kamera izni verilmedi"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    .line 819
    invoke-direct {p0, v4}, Lcom/bereket/alacakverecek/MainActivity;->answerFileChooser([Landroid/net/Uri;)V

    goto :goto_1

    .line 821
    :cond_4
    const/16 v3, 0x7d3

    if-ne p1, v3, :cond_6

    .line 822
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingWebPermission:Landroid/webkit/PermissionRequest;

    .line 823
    iput-object v4, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingWebPermission:Landroid/webkit/PermissionRequest;

    .line 824
    if-eqz v3, :cond_0

    .line 825
    if-eqz v0, :cond_5

    new-array v0, v1, [Ljava/lang/String;

    const-string v1, "android.webkit.resource.VIDEO_CAPTURE"

    aput-object v1, v0, v2

    invoke-virtual {v3, v0}, Landroid/webkit/PermissionRequest;->grant([Ljava/lang/String;)V

    goto :goto_1

    .line 826
    :cond_5
    invoke-virtual {v3}, Landroid/webkit/PermissionRequest;->deny()V

    goto :goto_1

    .line 828
    :cond_6
    const/16 v0, 0x7d2

    if-ne p1, v0, :cond_0

    .line 829
    if-eqz p3, :cond_7

    array-length v0, p3

    if-nez v0, :cond_0

    .line 831
    :cond_7
    const-string v0, "bereket"

    invoke-virtual {p0, v0, v2}, Lcom/bereket/alacakverecek/MainActivity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v0

    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    const-string v1, "notifAsked"

    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V

    goto :goto_1
.end method

.method protected onRestoreInstanceState(Landroid/os/Bundle;)V
    .locals 2

    .prologue
    .line 232
    invoke-super {p0, p1}, Landroid/app/Activity;->onRestoreInstanceState(Landroid/os/Bundle;)V

    .line 234
    const-string v0, "cameraFile"

    invoke-virtual {p1, v0}, Landroid/os/Bundle;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 235
    if-eqz v0, :cond_0

    new-instance v1, Ljava/io/File;

    invoke-direct {v1, v0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    iput-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    .line 236
    :cond_0
    const-string v0, "pendingSaveFile"

    invoke-virtual {p1, v0}, Landroid/os/Bundle;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 237
    if-eqz v0, :cond_1

    new-instance v1, Ljava/io/File;

    invoke-direct {v1, v0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    iput-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingSaveFile:Ljava/io/File;

    .line 238
    :cond_1
    return-void
.end method

.method protected onResume()V
    .locals 1

    .prologue
    .line 196
    invoke-super {p0}, Landroid/app/Activity;->onResume()V

    .line 197
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->onResume()V

    .line 198
    :cond_0
    return-void
.end method

.method protected onSaveInstanceState(Landroid/os/Bundle;)V
    .locals 2

    .prologue
    .line 225
    invoke-super {p0, p1}, Landroid/app/Activity;->onSaveInstanceState(Landroid/os/Bundle;)V

    .line 226
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    if-eqz v0, :cond_0

    const-string v0, "cameraFile"

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->cameraFile:Ljava/io/File;

    invoke-virtual {v1}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p1, v0, v1}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 227
    :cond_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingSaveFile:Ljava/io/File;

    if-eqz v0, :cond_1

    const-string v0, "pendingSaveFile"

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity;->pendingSaveFile:Ljava/io/File;

    invoke-virtual {v1}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p1, v0, v1}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 228
    :cond_1
    return-void
.end method

.method openExternal(Ljava/lang/String;)V
    .locals 4

    .prologue
    .line 387
    if-nez p1, :cond_1

    .line 411
    :cond_0
    :goto_0
    return-void

    .line 388
    :cond_1
    invoke-virtual {p1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v1

    .line 389
    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v0

    if-eqz v0, :cond_0

    .line 390
    sget-object v0, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v1, v0}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v0

    .line 391
    const-string v2, "javascript:"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-nez v2, :cond_2

    const-string v2, "file:"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-nez v2, :cond_2

    const-string v2, "content:"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-nez v2, :cond_2

    const-string v2, "intent:"

    .line 392
    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-nez v2, :cond_2

    const-string v2, "data:"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-nez v2, :cond_2

    const-string v2, "blob:"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_3

    .line 393
    :cond_2
    const-string v0, "BereketDefter"

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "blocked url scheme: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_0

    .line 397
    :cond_3
    const-string v2, "tel:"

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_4

    .line 398
    new-instance v0, Landroid/content/Intent;

    const-string v2, "android.intent.action.DIAL"

    invoke-static {v1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v1

    invoke-direct {v0, v2, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 404
    :goto_1
    :try_start_0
    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->startActivity(Landroid/content/Intent;)V
    :try_end_0
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_0} :catch_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_1

    goto :goto_0

    .line 405
    :catch_0
    move-exception v0

    .line 406
    const-string v0, "Bu ba\u011flant\u0131y\u0131 a\u00e7acak uygulama yok"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    goto :goto_0

    .line 400
    :cond_4
    new-instance v0, Landroid/content/Intent;

    const-string v2, "android.intent.action.VIEW"

    invoke-static {v1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v1

    invoke-direct {v0, v2, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 401
    const-string v1, "android.intent.category.BROWSABLE"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    goto :goto_1

    .line 407
    :catch_1
    move-exception v0

    .line 408
    const-string v1, "BereketDefter"

    const-string v2, "openUrl"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 409
    const-string v0, "Ba\u011flant\u0131 a\u00e7\u0131lamad\u0131"

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    goto/16 :goto_0
.end method

.method toast(Ljava/lang/String;)V
    .locals 1

    .prologue
    .line 303
    new-instance v0, Lcom/bereket/alacakverecek/MainActivity$4;

    invoke-direct {v0, p0, p1}, Lcom/bereket/alacakverecek/MainActivity$4;-><init>(Lcom/bereket/alacakverecek/MainActivity;Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lcom/bereket/alacakverecek/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 311
    return-void
.end method

.method writeTemp(Ljava/lang/String;Ljava/lang/String;[B)Ljava/io/File;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 341
    new-instance v0, Ljava/io/File;

    new-instance v1, Ljava/io/File;

    invoke-virtual {p0}, Lcom/bereket/alacakverecek/MainActivity;->getCacheDir()Ljava/io/File;

    move-result-object v2

    invoke-direct {v1, v2, p1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v2

    invoke-static {v2, v3}, Ljava/lang/String;->valueOf(J)Ljava/lang/String;

    move-result-object v2

    invoke-direct {v0, v1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 342
    invoke-virtual {v0}, Ljava/io/File;->isDirectory()Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    move-result v1

    if-nez v1, :cond_0

    new-instance v1, Ljava/io/IOException;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "mkdirs "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v1

    .line 343
    :cond_0
    new-instance v1, Ljava/io/File;

    invoke-direct {v1, v0, p2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 344
    new-instance v0, Ljava/io/FileOutputStream;

    invoke-direct {v0, v1}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    .line 346
    :try_start_0
    invoke-virtual {v0, p3}, Ljava/io/FileOutputStream;->write([B)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 348
    invoke-virtual {v0}, Ljava/io/FileOutputStream;->close()V

    .line 350
    return-object v1

    .line 348
    :catchall_0
    move-exception v1

    invoke-virtual {v0}, Ljava/io/FileOutputStream;->close()V

    .line 349
    throw v1
.end method
