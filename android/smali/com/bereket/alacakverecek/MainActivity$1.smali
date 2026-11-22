.class Lcom/bereket/alacakverecek/MainActivity$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/webkit/DownloadListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;)V
    .locals 0

    .prologue
    .line 122
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$1;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onDownloadStart(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)V
    .locals 2

    .prologue
    .line 126
    if-eqz p1, :cond_1

    const-string v0, "http://"

    invoke-virtual {p1, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_0

    const-string v0, "https://"

    invoke-virtual {p1, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_1

    :cond_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$1;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    .line 127
    invoke-static {p1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v1

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->isOwnOrigin(Landroid/net/Uri;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 128
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$1;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0, p1}, Lcom/bereket/alacakverecek/MainActivity;->openExternal(Ljava/lang/String;)V

    .line 132
    :goto_0
    return-void

    .line 130
    :cond_1
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$1;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const-string v1, "Bu indirme t\u00fcr\u00fc desteklenmiyor"

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->toast(Ljava/lang/String;)V

    goto :goto_0
.end method
