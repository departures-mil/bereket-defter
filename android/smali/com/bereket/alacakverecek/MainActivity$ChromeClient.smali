.class final Lcom/bereket/alacakverecek/MainActivity$ChromeClient;
.super Landroid/webkit/WebChromeClient;
.source "MainActivity.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/bereket/alacakverecek/MainActivity;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x10
    name = "ChromeClient"
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;)V
    .locals 0

    .prologue
    .line 484
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {p0}, Landroid/webkit/WebChromeClient;-><init>()V

    return-void
.end method


# virtual methods
.method public onConsoleMessage(Landroid/webkit/ConsoleMessage;)Z
    .locals 3

    .prologue
    .line 525
    const-string v0, "BereketDefter"

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "console: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p1}, Landroid/webkit/ConsoleMessage;->message()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, " @"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p1}, Landroid/webkit/ConsoleMessage;->sourceId()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ":"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p1}, Landroid/webkit/ConsoleMessage;->lineNumber()I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 526
    const/4 v0, 0x1

    return v0
.end method

.method public onJsAlert(Landroid/webkit/WebView;Ljava/lang/String;Ljava/lang/String;Landroid/webkit/JsResult;)Z
    .locals 4

    .prologue
    const/4 v0, 0x0

    .line 531
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v1}, Lcom/bereket/alacakverecek/MainActivity;->isFinishing()Z

    move-result v1

    if-eqz v1, :cond_0

    .line 550
    :goto_0
    return v0

    .line 533
    :cond_0
    :try_start_0
    new-instance v1, Landroid/app/AlertDialog$Builder;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {v1, v2}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    .line 534
    invoke-virtual {v1, p3}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    const-string v2, "Tamam"

    new-instance v3, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$2;

    invoke-direct {v3, p0, p4}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$2;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsResult;)V

    .line 535
    invoke-virtual {v1, v2, v3}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$1;

    invoke-direct {v2, p0, p4}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$1;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsResult;)V

    .line 541
    invoke-virtual {v1, v2}, Landroid/app/AlertDialog$Builder;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    .line 547
    invoke-virtual {v1}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 548
    const/4 v0, 0x1

    goto :goto_0

    .line 549
    :catch_0
    move-exception v1

    goto :goto_0
.end method

.method public onJsConfirm(Landroid/webkit/WebView;Ljava/lang/String;Ljava/lang/String;Landroid/webkit/JsResult;)Z
    .locals 4

    .prologue
    const/4 v0, 0x0

    .line 556
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v1}, Lcom/bereket/alacakverecek/MainActivity;->isFinishing()Z

    move-result v1

    if-eqz v1, :cond_0

    .line 581
    :goto_0
    return v0

    .line 558
    :cond_0
    :try_start_0
    new-instance v1, Landroid/app/AlertDialog$Builder;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {v1, v2}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    .line 559
    invoke-virtual {v1, p3}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    const-string v2, "Tamam"

    new-instance v3, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$5;

    invoke-direct {v3, p0, p4}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$5;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsResult;)V

    .line 560
    invoke-virtual {v1, v2, v3}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    const-string v2, "\u0130ptal"

    new-instance v3, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$4;

    invoke-direct {v3, p0, p4}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$4;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsResult;)V

    .line 566
    invoke-virtual {v1, v2, v3}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$3;

    invoke-direct {v2, p0, p4}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$3;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsResult;)V

    .line 572
    invoke-virtual {v1, v2}, Landroid/app/AlertDialog$Builder;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v1

    .line 578
    invoke-virtual {v1}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 579
    const/4 v0, 0x1

    goto :goto_0

    .line 580
    :catch_0
    move-exception v1

    goto :goto_0
.end method

.method public onJsPrompt(Landroid/webkit/WebView;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Landroid/webkit/JsPromptResult;)Z
    .locals 6

    .prologue
    const/4 v1, 0x1

    const/4 v0, 0x0

    .line 588
    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v2}, Lcom/bereket/alacakverecek/MainActivity;->isFinishing()Z

    move-result v2

    if-eqz v2, :cond_0

    .line 617
    :goto_0
    return v0

    .line 590
    :cond_0
    :try_start_0
    new-instance v2, Landroid/widget/EditText;

    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {v2, v3}, Landroid/widget/EditText;-><init>(Landroid/content/Context;)V

    .line 591
    const/4 v3, 0x1

    invoke-virtual {v2, v3}, Landroid/widget/EditText;->setSingleLine(Z)V

    .line 592
    if-eqz p4, :cond_1

    invoke-virtual {v2, p4}, Landroid/widget/EditText;->setText(Ljava/lang/CharSequence;)V

    .line 593
    :cond_1
    new-instance v3, Landroid/app/AlertDialog$Builder;

    iget-object v4, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {v3, v4}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    .line 594
    invoke-virtual {v3, p3}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v3

    .line 595
    invoke-virtual {v3, v2}, Landroid/app/AlertDialog$Builder;->setView(Landroid/view/View;)Landroid/app/AlertDialog$Builder;

    move-result-object v3

    const-string v4, "Tamam"

    new-instance v5, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;

    invoke-direct {v5, p0, p5, v2}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsPromptResult;Landroid/widget/EditText;)V

    .line 596
    invoke-virtual {v3, v4, v5}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v2

    const-string v3, "\u0130ptal"

    new-instance v4, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$7;

    invoke-direct {v4, p0, p5}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$7;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsPromptResult;)V

    .line 602
    invoke-virtual {v2, v3, v4}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v2

    new-instance v3, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$6;

    invoke-direct {v3, p0, p5}, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$6;-><init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsPromptResult;)V

    .line 608
    invoke-virtual {v2, v3}, Landroid/app/AlertDialog$Builder;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)Landroid/app/AlertDialog$Builder;

    move-result-object v2

    .line 614
    invoke-virtual {v2}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    move v0, v1

    .line 615
    goto :goto_0

    .line 616
    :catch_0
    move-exception v1

    goto :goto_0
.end method

.method public onPermissionRequest(Landroid/webkit/PermissionRequest;)V
    .locals 8

    .prologue
    const/4 v1, 0x1

    const/4 v3, 0x0

    .line 506
    .line 507
    invoke-virtual {p1}, Landroid/webkit/PermissionRequest;->getResources()[Ljava/lang/String;

    move-result-object v4

    array-length v5, v4

    move v2, v3

    move v0, v3

    :goto_0
    if-ge v2, v5, :cond_1

    aget-object v6, v4, v2

    .line 508
    const-string v7, "android.webkit.resource.VIDEO_CAPTURE"

    invoke-virtual {v7, v6}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6

    if-eqz v6, :cond_0

    move v0, v1

    .line 507
    :cond_0
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 510
    :cond_1
    if-eqz v0, :cond_2

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {p1}, Landroid/webkit/PermissionRequest;->getOrigin()Landroid/net/Uri;

    move-result-object v2

    invoke-virtual {v0, v2}, Lcom/bereket/alacakverecek/MainActivity;->isOwnOrigin(Landroid/net/Uri;)Z

    move-result v0

    if-nez v0, :cond_3

    .line 511
    :cond_2
    invoke-virtual {p1}, Landroid/webkit/PermissionRequest;->deny()V

    .line 521
    :goto_1
    return-void

    .line 514
    :cond_3
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const-string v2, "android.permission.CAMERA"

    invoke-static {v0, v2}, Lcom/bereket/alacakverecek/MainActivity;->access$1000(Lcom/bereket/alacakverecek/MainActivity;Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_4

    .line 515
    new-array v0, v1, [Ljava/lang/String;

    const-string v1, "android.webkit.resource.VIDEO_CAPTURE"

    aput-object v1, v0, v3

    invoke-virtual {p1, v0}, Landroid/webkit/PermissionRequest;->grant([Ljava/lang/String;)V

    goto :goto_1

    .line 517
    :cond_4
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$1100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/PermissionRequest;

    move-result-object v0

    if-eqz v0, :cond_5

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$1100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/PermissionRequest;

    move-result-object v0

    invoke-virtual {v0}, Landroid/webkit/PermissionRequest;->deny()V

    .line 518
    :cond_5
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0, p1}, Lcom/bereket/alacakverecek/MainActivity;->access$1102(Lcom/bereket/alacakverecek/MainActivity;Landroid/webkit/PermissionRequest;)Landroid/webkit/PermissionRequest;

    .line 519
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    new-array v1, v1, [Ljava/lang/String;

    const-string v2, "android.permission.CAMERA"

    aput-object v2, v1, v3

    const/16 v2, 0x7d3

    invoke-virtual {v0, v1, v2}, Lcom/bereket/alacakverecek/MainActivity;->requestPermissions([Ljava/lang/String;I)V

    goto :goto_1
.end method

.method public onShowFileChooser(Landroid/webkit/WebView;Landroid/webkit/ValueCallback;Landroid/webkit/WebChromeClient$FileChooserParams;)Z
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/webkit/WebView;",
            "Landroid/webkit/ValueCallback",
            "<[",
            "Landroid/net/Uri;",
            ">;",
            "Landroid/webkit/WebChromeClient$FileChooserParams;",
            ")Z"
        }
    .end annotation

    .prologue
    const/4 v0, 0x0

    const/4 v2, 0x0

    const/4 v1, 0x1

    .line 488
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v3, v0}, Lcom/bereket/alacakverecek/MainActivity;->access$300(Lcom/bereket/alacakverecek/MainActivity;[Landroid/net/Uri;)V

    .line 489
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v3, p2}, Lcom/bereket/alacakverecek/MainActivity;->access$402(Lcom/bereket/alacakverecek/MainActivity;Landroid/webkit/ValueCallback;)Landroid/webkit/ValueCallback;

    .line 490
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    if-eqz p3, :cond_0

    invoke-virtual {p3}, Landroid/webkit/WebChromeClient$FileChooserParams;->getAcceptTypes()[Ljava/lang/String;

    move-result-object v0

    :cond_0
    invoke-static {v0}, Lcom/bereket/alacakverecek/Util;->acceptToMimes([Ljava/lang/String;)Ljava/util/List;

    move-result-object v0

    invoke-static {v3, v0}, Lcom/bereket/alacakverecek/MainActivity;->access$502(Lcom/bereket/alacakverecek/MainActivity;Ljava/util/List;)Ljava/util/List;

    .line 491
    iget-object v3, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    if-eqz p3, :cond_2

    invoke-virtual {p3}, Landroid/webkit/WebChromeClient$FileChooserParams;->getMode()I

    move-result v0

    if-ne v0, v1, :cond_2

    move v0, v1

    :goto_0
    invoke-static {v3, v0}, Lcom/bereket/alacakverecek/MainActivity;->access$602(Lcom/bereket/alacakverecek/MainActivity;Z)Z

    .line 492
    if-eqz p3, :cond_1

    invoke-virtual {p3}, Landroid/webkit/WebChromeClient$FileChooserParams;->isCaptureEnabled()Z

    move-result v0

    if-eqz v0, :cond_1

    move v2, v1

    .line 493
    :cond_1
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$500(Lcom/bereket/alacakverecek/MainActivity;)Ljava/util/List;

    move-result-object v0

    invoke-static {v0}, Lcom/bereket/alacakverecek/Util;->acceptsImages(Ljava/util/List;)Z

    move-result v0

    .line 494
    if-eqz v2, :cond_3

    if-eqz v0, :cond_3

    .line 495
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$700(Lcom/bereket/alacakverecek/MainActivity;)V

    .line 501
    :goto_1
    return v1

    :cond_2
    move v0, v2

    .line 491
    goto :goto_0

    .line 496
    :cond_3
    if-nez v0, :cond_4

    .line 497
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$800(Lcom/bereket/alacakverecek/MainActivity;)V

    goto :goto_1

    .line 499
    :cond_4
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$900(Lcom/bereket/alacakverecek/MainActivity;)V

    goto :goto_1
.end method
