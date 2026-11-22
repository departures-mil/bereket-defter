.class Lcom/bereket/alacakverecek/MainActivity$Bridge$7;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->restartApp()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;)V
    .locals 0

    .prologue
    .line 1078
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$7;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 2

    .prologue
    .line 1081
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$7;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$7;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v1, v1, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v1}, Lcom/bereket/alacakverecek/MainActivity;->appVersionName()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/bereket/alacakverecek/Updates;->resolveActive(Landroid/content/Context;Ljava/lang/String;)Ljava/io/File;

    move-result-object v0

    sput-object v0, Lcom/bereket/alacakverecek/MainActivity;->activeBundle:Ljava/io/File;

    .line 1082
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$7;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->clearCache(Z)V

    .line 1083
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$7;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    const-string v1, "https://appassets.androidplatform.net/www/index.html"

    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    .line 1084
    return-void
.end method
