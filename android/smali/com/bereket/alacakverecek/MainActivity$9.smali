.class Lcom/bereket/alacakverecek/MainActivity$9;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->onActivityResult(IILandroid/content/Intent;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;

.field final synthetic val$src:Ljava/io/File;

.field final synthetic val$target:Landroid/net/Uri;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;Landroid/net/Uri;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 759
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$9;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$9;->val$src:Ljava/io/File;

    iput-object p3, p0, Lcom/bereket/alacakverecek/MainActivity$9;->val$target:Landroid/net/Uri;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    .line 762
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$9;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$9;->val$src:Ljava/io/File;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$9;->val$target:Landroid/net/Uri;

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/MainActivity;->access$1200(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;Landroid/net/Uri;)Z

    move-result v0

    .line 763
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$9;->val$src:Ljava/io/File;

    invoke-virtual {v1}, Ljava/io/File;->delete()Z

    .line 764
    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$9;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v1, v0}, Lcom/bereket/alacakverecek/MainActivity;->access$1300(Lcom/bereket/alacakverecek/MainActivity;Z)V

    .line 765
    return-void
.end method
