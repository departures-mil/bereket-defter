.class Lcom/bereket/alacakverecek/MainActivity$Bridge$9;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->installApk(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

.field final synthetic val$f:Ljava/io/File;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/io/File;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 1126
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;->val$f:Ljava/io/File;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    .line 1130
    :try_start_0
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.VIEW"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 1131
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v1, v1, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;->val$f:Ljava/io/File;

    invoke-static {v1, v2}, Lcom/bereket/alacakverecek/FilesProvider;->uriFor(Landroid/content/Context;Ljava/io/File;)Landroid/net/Uri;

    move-result-object v1

    const-string v2, "application/vnd.android.package-archive"

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setDataAndType(Landroid/net/Uri;Ljava/lang/String;)Landroid/content/Intent;

    .line 1132
    const v1, 0x10000001

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 1133
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v1, v1, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v1, v0}, Lcom/bereket/alacakverecek/MainActivity;->startActivity(Landroid/content/Intent;)V
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 1138
    :goto_0
    return-void

    .line 1134
    :catch_0
    move-exception v0

    .line 1135
    const-string v1, "BereketDefter"

    const-string v2, "apk install"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 1136
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$9;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    const-string v1, "Kurulum ekran\u0131 a\u00e7\u0131lamad\u0131"

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity$Bridge;->toast(Ljava/lang/String;)V

    goto :goto_0
.end method
