.class Lcom/bereket/alacakverecek/MainActivity$7;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/content/DialogInterface$OnCancelListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->showSourceDialog()V
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
    .line 650
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$7;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onCancel(Landroid/content/DialogInterface;)V
    .locals 2

    .prologue
    .line 653
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$7;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lcom/bereket/alacakverecek/MainActivity;->access$300(Lcom/bereket/alacakverecek/MainActivity;[Landroid/net/Uri;)V

    .line 654
    return-void
.end method
