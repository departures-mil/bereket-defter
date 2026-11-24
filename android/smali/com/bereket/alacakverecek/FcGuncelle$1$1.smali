.class Lcom/bereket/alacakverecek/FcGuncelle$1$1;
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


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/FcGuncelle$1;)V
    .registers 2
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010
        }
        names = {
            null
        }
    .end annotation

    iput-object p1, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$1;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 6

    const-string v0, "package:"

    :try_start_0
    iget-object v1, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$1;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    iget-object v1, v1, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    new-instance v2, Landroid/content/Intent;

    const-string v3, "android.settings.MANAGE_UNKNOWN_APP_SOURCES"

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget-object v0, p0, Lcom/bereket/alacakverecek/FcGuncelle$1$1;->this$0:Lcom/bereket/alacakverecek/FcGuncelle$1;

    iget-object v0, v0, Lcom/bereket/alacakverecek/FcGuncelle$1;->val$a:Landroid/app/Activity;

    invoke-virtual {v0}, Landroid/app/Activity;->getPackageName()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v0

    invoke-direct {v2, v3, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    invoke-virtual {v1, v2}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :catchall_0
    return-void
.end method
