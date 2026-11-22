.class Lcom/bereket/alacakverecek/MainActivity$10;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->notifySaved(Z)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;

.field final synthetic val$ok:Z


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;Z)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 793
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$10;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iput-boolean p2, p0, Lcom/bereket/alacakverecek/MainActivity$10;->val$ok:Z

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    .line 796
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$10;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    if-nez v0, :cond_0

    .line 804
    :goto_0
    return-void

    .line 797
    :cond_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$10;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$100(Lcom/bereket/alacakverecek/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "(function(){if(typeof window.onAndroidSaved===\'function\'){window.onAndroidSaved("

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    iget-boolean v2, p0, Lcom/bereket/alacakverecek/MainActivity$10;->val$ok:Z

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Z)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ");return 1}return 0})()"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    new-instance v2, Lcom/bereket/alacakverecek/MainActivity$10$1;

    invoke-direct {v2, p0}, Lcom/bereket/alacakverecek/MainActivity$10$1;-><init>(Lcom/bereket/alacakverecek/MainActivity$10;)V

    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V

    goto :goto_0
.end method
