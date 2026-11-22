.class Lcom/bereket/alacakverecek/MainActivity$11;
.super Lcom/bereket/alacakverecek/MainActivity$AppClient;
.source "MainActivity.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->printHtmlOnUi(Ljava/lang/String;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field started:Z

.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;

.field final synthetic val$name:Ljava/lang/String;

.field final synthetic val$pw:Landroid/webkit/WebView;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;ZLandroid/webkit/WebView;Ljava/lang/String;)V
    .locals 0

    .prologue
    .line 852
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$11;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iput-object p3, p0, Lcom/bereket/alacakverecek/MainActivity$11;->val$pw:Landroid/webkit/WebView;

    iput-object p4, p0, Lcom/bereket/alacakverecek/MainActivity$11;->val$name:Ljava/lang/String;

    invoke-direct {p0, p1, p2}, Lcom/bereket/alacakverecek/MainActivity$AppClient;-><init>(Lcom/bereket/alacakverecek/MainActivity;Z)V

    return-void
.end method


# virtual methods
.method public onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V
    .locals 4

    .prologue
    .line 857
    iget-boolean v0, p0, Lcom/bereket/alacakverecek/MainActivity$11;->started:Z

    if-eqz v0, :cond_0

    .line 866
    :goto_0
    return-void

    .line 858
    :cond_0
    const/4 v0, 0x1

    iput-boolean v0, p0, Lcom/bereket/alacakverecek/MainActivity$11;->started:Z

    .line 860
    new-instance v0, Lcom/bereket/alacakverecek/MainActivity$11$1;

    invoke-direct {v0, p0}, Lcom/bereket/alacakverecek/MainActivity$11$1;-><init>(Lcom/bereket/alacakverecek/MainActivity$11;)V

    const-wide/16 v2, 0x12c

    invoke-virtual {p1, v0, v2, v3}, Landroid/webkit/WebView;->postDelayed(Ljava/lang/Runnable;J)Z

    goto :goto_0
.end method
