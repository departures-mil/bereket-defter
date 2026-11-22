.class Lcom/bereket/alacakverecek/MainActivity$10$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/webkit/ValueCallback;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$10;->run()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Landroid/webkit/ValueCallback",
        "<",
        "Ljava/lang/String;",
        ">;"
    }
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$10;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$10;)V
    .locals 0

    .prologue
    .line 798
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$10$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$10;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public bridge synthetic onReceiveValue(Ljava/lang/Object;)V
    .locals 0

    .prologue
    .line 798
    check-cast p1, Ljava/lang/String;

    invoke-virtual {p0, p1}, Lcom/bereket/alacakverecek/MainActivity$10$1;->onReceiveValue(Ljava/lang/String;)V

    return-void
.end method

.method public onReceiveValue(Ljava/lang/String;)V
    .locals 2

    .prologue
    .line 801
    const-string v0, "1"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$10$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$10;

    iget-object v1, v0, Lcom/bereket/alacakverecek/MainActivity$10;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$10$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$10;

    iget-boolean v0, v0, Lcom/bereket/alacakverecek/MainActivity$10;->val$ok:Z

    if-eqz v0, :cond_1

    const-string v0, "Dosya kaydedildi"

    :goto_0
    invoke-virtual {v1, v0}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    .line 802
    :cond_0
    return-void

    .line 801
    :cond_1
    const-string v0, "Dosya kaydedilmedi"

    goto :goto_0
.end method
