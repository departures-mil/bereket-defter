.class Lcom/bereket/alacakverecek/MainActivity$Bridge$3;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->shareFile(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

.field final synthetic val$m:Ljava/lang/String;

.field final synthetic val$name:Ljava/lang/String;

.field final synthetic val$uri:Landroid/net/Uri;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/lang/String;Landroid/net/Uri;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 954
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$m:Ljava/lang/String;

    iput-object p3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$uri:Landroid/net/Uri;

    iput-object p4, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$name:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 4

    .prologue
    const/4 v3, 0x1

    .line 957
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.SEND"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 958
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$m:Ljava/lang/String;

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    .line 959
    const-string v1, "android.intent.extra.STREAM"

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$uri:Landroid/net/Uri;

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 960
    const-string v1, "android.intent.extra.SUBJECT"

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$name:Ljava/lang/String;

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 961
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$name:Ljava/lang/String;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$uri:Landroid/net/Uri;

    invoke-static {v1, v2}, Landroid/content/ClipData;->newRawUri(Ljava/lang/CharSequence;Landroid/net/Uri;)Landroid/content/ClipData;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setClipData(Landroid/content/ClipData;)V

    .line 962
    invoke-virtual {v0, v3}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 963
    const-string v1, "Payla\u015f"

    invoke-static {v0, v1}, Landroid/content/Intent;->createChooser(Landroid/content/Intent;Ljava/lang/CharSequence;)Landroid/content/Intent;

    move-result-object v0

    .line 964
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$name:Ljava/lang/String;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->val$uri:Landroid/net/Uri;

    invoke-static {v1, v2}, Landroid/content/ClipData;->newRawUri(Ljava/lang/CharSequence;Landroid/net/Uri;)Landroid/content/ClipData;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setClipData(Landroid/content/ClipData;)V

    .line 965
    invoke-virtual {v0, v3}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 967
    :try_start_0
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v1, v1, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v1, v0}, Lcom/bereket/alacakverecek/MainActivity;->startActivity(Landroid/content/Intent;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 972
    :goto_0
    return-void

    .line 968
    :catch_0
    move-exception v0

    .line 969
    const-string v1, "BereketDefter"

    const-string v2, "share"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 970
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$3;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    const-string v1, "Payla\u015facak uygulama yok"

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity$Bridge;->toast(Ljava/lang/String;)V

    goto :goto_0
.end method
