.class Lcom/bereket/alacakverecek/MainActivity$Bridge$4;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->openFile(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

.field final synthetic val$m:Ljava/lang/String;

.field final synthetic val$uri:Landroid/net/Uri;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Landroid/net/Uri;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 988
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->val$uri:Landroid/net/Uri;

    iput-object p3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->val$m:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    .line 991
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.VIEW"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 992
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->val$uri:Landroid/net/Uri;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->val$m:Ljava/lang/String;

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setDataAndType(Landroid/net/Uri;Ljava/lang/String;)Landroid/content/Intent;

    .line 993
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 995
    :try_start_0
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v1, v1, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v1, v0}, Lcom/bereket/alacakverecek/MainActivity;->startActivity(Landroid/content/Intent;)V
    :try_end_0
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_0} :catch_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_1

    .line 1002
    :goto_0
    return-void

    .line 996
    :catch_0
    move-exception v0

    .line 997
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    const-string v1, "Bu dosyay\u0131 a\u00e7acak uygulama yok"

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity$Bridge;->toast(Ljava/lang/String;)V

    goto :goto_0

    .line 998
    :catch_1
    move-exception v0

    .line 999
    const-string v1, "BereketDefter"

    const-string v2, "open"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 1000
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$4;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    const-string v1, "Bu dosyay\u0131 a\u00e7acak uygulama yok"

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity$Bridge;->toast(Ljava/lang/String;)V

    goto :goto_0
.end method
