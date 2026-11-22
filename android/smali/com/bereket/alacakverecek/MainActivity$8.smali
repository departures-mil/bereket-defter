.class Lcom/bereket/alacakverecek/MainActivity$8;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/content/DialogInterface$OnClickListener;


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
    .line 643
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$8;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/content/DialogInterface;I)V
    .locals 1

    .prologue
    .line 646
    if-nez p2, :cond_0

    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$8;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$700(Lcom/bereket/alacakverecek/MainActivity;)V

    .line 648
    :goto_0
    return-void

    .line 647
    :cond_0
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$8;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-static {v0}, Lcom/bereket/alacakverecek/MainActivity;->access$800(Lcom/bereket/alacakverecek/MainActivity;)V

    goto :goto_0
.end method
