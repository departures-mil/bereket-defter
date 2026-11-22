.class Lcom/bereket/alacakverecek/MainActivity$Bridge$5;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->openUrl(Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

.field final synthetic val$url:Ljava/lang/String;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 1008
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$5;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$5;->val$url:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 2

    .prologue
    .line 1011
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$5;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$5;->val$url:Ljava/lang/String;

    invoke-virtual {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->openExternal(Ljava/lang/String;)V

    .line 1012
    return-void
.end method
