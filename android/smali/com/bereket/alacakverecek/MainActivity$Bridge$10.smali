.class Lcom/bereket/alacakverecek/MainActivity$Bridge$10;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$Bridge;->exitApp()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$Bridge;)V
    .locals 0

    .prologue
    .line 1145
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$10;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 1

    .prologue
    .line 1148
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$Bridge$10;->this$1:Lcom/bereket/alacakverecek/MainActivity$Bridge;

    iget-object v0, v0, Lcom/bereket/alacakverecek/MainActivity$Bridge;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->finish()V

    .line 1149
    return-void
.end method
