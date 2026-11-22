.class Lcom/bereket/alacakverecek/MainActivity$5;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->evalJs(Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;

.field final synthetic val$js:Ljava/lang/String;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 331
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$5;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$5;->val$js:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    .line 334
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$5;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$5;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$5;->val$js:Ljava/lang/String;

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V

    .line 335
    :cond_0
    return-void
.end method
