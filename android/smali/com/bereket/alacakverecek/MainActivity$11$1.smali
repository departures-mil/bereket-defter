.class Lcom/bereket/alacakverecek/MainActivity$11$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$11;->onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$11;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$11;)V
    .locals 0

    .prologue
    .line 860
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$11$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$11;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    .line 863
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$11$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$11;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$11;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$11$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$11;

    iget-object v1, v1, Lcom/bereket/alacakverecek/MainActivity$11;->val$pw:Landroid/webkit/WebView;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$11$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$11;

    iget-object v2, v2, Lcom/bereket/alacakverecek/MainActivity$11;->val$name:Ljava/lang/String;

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/MainActivity;->access$1400(Lcom/bereket/alacakverecek/MainActivity;Landroid/webkit/WebView;Ljava/lang/String;)V

    .line 864
    return-void
.end method
