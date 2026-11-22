.class Lcom/bereket/alacakverecek/MainActivity$Bridge$2;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->saveFile(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

.field final synthetic val$f:Ljava/io/File;

.field final synthetic val$m:Ljava/lang/String;

.field final synthetic val$name:Ljava/lang/String;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/io/File;Ljava/lang/String;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 917
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->val$f:Ljava/io/File;

    iput-object p3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->val$m:Ljava/lang/String;

    iput-object p4, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->val$name:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 4

    .prologue
    const/4 v3, 0x0

    .line 920
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$1600(Lcom/bereket/alacakverecek/MainActivity;)Ljava/io/File;

    move-result-object v0

    if-eqz v0, :cond_0

    .line 921
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$1600(Lcom/bereket/alacakverecek/MainActivity;)Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->delete()Z

    .line 922
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0, v3}, Lcom/bereket/alacakverecek/MainActivity;->access$1300(Lcom/bereket/alacakverecek/MainActivity;Z)V

    .line 924
    :cond_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->val$f:Ljava/io/File;

    invoke-static {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->access$1602(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;)Ljava/io/File;

    .line 925
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.CREATE_DOCUMENT"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 926
    const-string v1, "android.intent.category.OPENABLE"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    .line 927
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->val$m:Ljava/lang/String;

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    .line 928
    const-string v1, "android.intent.extra.TITLE"

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->val$name:Ljava/lang/String;

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 930
    :try_start_0
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v1, v1, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const/16 v2, 0x3eb

    invoke-virtual {v1, v0, v2}, Lcom/bereket/alacakverecek/MainActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 938
    :goto_0
    return-void

    .line 931
    :catch_0
    move-exception v0

    .line 932
    const-string v1, "BereketDefter"

    const-string v2, "create document"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 933
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->access$1602(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;)Ljava/io/File;

    .line 934
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->val$f:Ljava/io/File;

    invoke-virtual {v0}, Ljava/io/File;->delete()Z

    .line 935
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    const-string v1, "Kaydetme ekran\u0131 a\u00e7\u0131lamad\u0131"

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity$Bridge;->toast(Ljava/lang/String;)V

    .line 936
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$2;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0, v3}, Lcom/bereket/alacakverecek/MainActivity;->access$1300(Lcom/bereket/alacakverecek/MainActivity;Z)V

    goto :goto_0
.end method
