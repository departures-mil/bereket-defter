.class Lcom/bereket/alacakverecek/FcGuncelle$1$2;
.super Ljava/lang/Object;
.source "FcGuncelle.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/FcGuncelle$1;->run()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

.field final synthetic val$apk:Ljava/io/File;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/FcGuncelle$1;Ljava/io/File;)V
    .registers 3
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010
        }
        names = {
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    iput-object p1, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$2;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    iput-object p2, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$2;->val$apk:Ljava/io/File;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 4

    :try_start_0
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.VIEW"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    iget-object v1, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$2;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    iget-object v1, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v2, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$2;->val$apk:Ljava/io/File;

    invoke-static {v1, v2}, Lcom/bereket/alacakverecek/FilesProvider;->uriFor(Landroid/content/Context;Ljava/io/File;)Landroid/net/Uri;

    move-result-object v1

    const-string v2, "application/vnd.android.package-archive"

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setDataAndType(Landroid/net/Uri;Ljava/lang/String;)Landroid/content/Intent;

    const v1, 0x10000001

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    iget-object v1, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$2;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    iget-object v1, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    invoke-virtual {v1, v0}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    goto :goto_0

    :catchall_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$2;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    iget-object v0, v0, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    iget-object v1, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$2;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    iget-object v1, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$w:Landroid/webkit/WebView;

    const-string v2, "{\"type\":\"error\",\"error\":\"INSTALLER\"}"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/FcGuncelle;->access$100(Landroid/app/Activity;Landroid/webkit/WebView;Ljava/lang/String;)V

    :goto_0
    return-void
.end method
