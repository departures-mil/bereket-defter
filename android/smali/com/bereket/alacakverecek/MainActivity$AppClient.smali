.class Lcom/bereket/alacakverecek/MainActivity$AppClient;
.super Landroid/webkit/WebViewClient;
.source "MainActivity.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/bereket/alacakverecek/MainActivity;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = "AppClient"
.end annotation


# instance fields
.field final printMode:Z

.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;Z)V
    .locals 0

    .prologue
    .line 451
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$AppClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V

    .line 452
    iput-boolean p2, p0, Lcom/bereket/alacakverecek/MainActivity$AppClient;->printMode:Z

    .line 453
    return-void
.end method


# virtual methods
.method public shouldInterceptRequest(Landroid/webkit/WebView;Landroid/webkit/WebResourceRequest;)Landroid/webkit/WebResourceResponse;
    .locals 6

    .prologue
    const/4 v1, 0x0

    .line 457
    if-eqz p2, :cond_1

    invoke-interface {p2}, Landroid/webkit/WebResourceRequest;->getUrl()Landroid/net/Uri;

    move-result-object v0

    .line 458
    :goto_0
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$AppClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v2, v0}, Lcom/bereket/alacakverecek/MainActivity;->isOwnOrigin(Landroid/net/Uri;)Z

    move-result v2

    if-eqz v2, :cond_0

    .line 460
    :try_start_0
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$AppClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v2, v0}, Lcom/bereket/alacakverecek/MainActivity;->serveAsset(Landroid/content/Context;Landroid/net/Uri;)Landroid/webkit/WebResourceResponse;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v1

    .line 466
    :cond_0
    :goto_1
    return-object v1

    :cond_1
    move-object v0, v1

    .line 457
    goto :goto_0

    .line 461
    :catch_0
    move-exception v2

    .line 462
    const-string v3, "BereketDefter"

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    const-string v5, "serve "

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v3, v0, v2}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    goto :goto_1
.end method

.method public shouldOverrideUrlLoading(Landroid/webkit/WebView;Ljava/lang/String;)Z
    .locals 4

    .prologue
    const/4 v2, 0x0

    const/4 v1, 0x1

    .line 471
    if-nez p2, :cond_0

    move v0, v1

    .line 478
    :goto_0
    return v0

    .line 472
    :cond_0
    iget-boolean v0, p0, Lcom/bereket/alacakverecek/MainActivity$AppClient;->printMode:Z

    if-eqz v0, :cond_1

    move v0, v1

    goto :goto_0

    .line 473
    :cond_1
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v0

    .line 474
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$AppClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v3, v0}, Lcom/bereket/alacakverecek/MainActivity;->isOwnOrigin(Landroid/net/Uri;)Z

    move-result v3

    if-eqz v3, :cond_2

    move v0, v2

    goto :goto_0

    .line 475
    :cond_2
    invoke-virtual {v0}, Landroid/net/Uri;->getScheme()Ljava/lang/String;

    move-result-object v3

    if-nez v3, :cond_3

    const-string v0, ""

    .line 476
    :goto_1
    const-string v3, "about"

    invoke-virtual {v0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4

    move v0, v2

    goto :goto_0

    .line 475
    :cond_3
    invoke-virtual {v0}, Landroid/net/Uri;->getScheme()Ljava/lang/String;

    move-result-object v0

    sget-object v3, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v0, v3}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v0

    goto :goto_1

    .line 477
    :cond_4
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$AppClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0, p2}, Lcom/bereket/alacakverecek/MainActivity;->openExternal(Ljava/lang/String;)V

    move v0, v1

    .line 478
    goto :goto_0
.end method
