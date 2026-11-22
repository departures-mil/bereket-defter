.class Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/content/DialogInterface$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity$ChromeClient;->onJsPrompt(Landroid/webkit/WebView;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Landroid/webkit/JsPromptResult;)Z
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/bereket/alacakverecek/MainActivity$ChromeClient;

.field final synthetic val$input:Landroid/widget/EditText;

.field final synthetic val$result:Landroid/webkit/JsPromptResult;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity$ChromeClient;Landroid/webkit/JsPromptResult;Landroid/widget/EditText;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 596
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;->this$1:Lcom/bereket/alacakverecek/MainActivity$ChromeClient;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;->val$result:Landroid/webkit/JsPromptResult;

    iput-object p3, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;->val$input:Landroid/widget/EditText;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/content/DialogInterface;I)V
    .locals 2

    .prologue
    .line 599
    iget-object v0, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;->val$result:Landroid/webkit/JsPromptResult;

    iget-object v1, p0, Lcom/bereket/alacakverecek/MainActivity$ChromeClient$8;->val$input:Landroid/widget/EditText;

    invoke-virtual {v1}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object v1

    invoke-interface {v1}, Landroid/text/Editable;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/webkit/JsPromptResult;->confirm(Ljava/lang/String;)V

    .line 600
    return-void
.end method
