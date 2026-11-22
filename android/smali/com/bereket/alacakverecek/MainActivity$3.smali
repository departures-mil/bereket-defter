.class Lcom/bereket/alacakverecek/MainActivity$3;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/content/DialogInterface$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->askExit()V
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
    .line 264
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$3;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/content/DialogInterface;I)V
    .locals 1

    .prologue
    .line 267
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$3;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    invoke-virtual {v0}, Lcom/bereket/alacakverecek/MainActivity;->finish()V

    .line 268
    return-void
.end method
