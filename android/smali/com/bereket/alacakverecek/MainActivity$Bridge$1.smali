.class Lcom/bereket/alacakverecek/MainActivity$Bridge$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->printHtml(Ljava/lang/String;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

.field final synthetic val$html:Ljava/lang/String;

.field final synthetic val$jobName:Ljava/lang/String;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;Ljava/lang/String;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 897
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;->val$html:Ljava/lang/String;

    iput-object p3, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;->val$jobName:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    .line 900
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;->val$html:Ljava/lang/String;

    iget-object v2, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$1;->val$jobName:Ljava/lang/String;

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/MainActivity;->access$1500(Lcom/bereket/alacakverecek/MainActivity;Ljava/lang/String;Ljava/lang/String;)V

    .line 901
    return-void
.end method
