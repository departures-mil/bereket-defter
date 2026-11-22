.class Lcom/bereket/alacakverecek/MainActivity$6;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/bereket/alacakverecek/MainActivity;->cleanCacheAsync()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/bereket/alacakverecek/MainActivity;

.field final synthetic val$cache:Ljava/io/File;


# direct methods
.method constructor <init>(Lcom/bereket/alacakverecek/MainActivity;Ljava/io/File;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .prologue
    .line 363
    iput-object p1, p0, Lcom/bereket/alacakverecek/MainActivity$6;->this$0:Lcom/bereket/alacakverecek/MainActivity;

    iput-object p2, p0, Lcom/bereket/alacakverecek/MainActivity$6;->val$cache:Ljava/io/File;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 9

    .prologue
    const/4 v1, 0x0

    .line 366
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v2

    const-wide/32 v4, 0x5265c00

    sub-long/2addr v2, v4

    .line 367
    const/4 v0, 0x5

    new-array v4, v0, [Ljava/lang/String;

    const-string v0, "share"

    aput-object v0, v4, v1

    const/4 v0, 0x1

    const-string v5, "open"

    aput-object v5, v4, v0

    const/4 v0, 0x2

    const-string v5, "save"

    aput-object v5, v4, v0

    const/4 v0, 0x3

    const-string v5, "camera"

    aput-object v5, v4, v0

    const/4 v0, 0x4

    const-string v5, "apk"

    aput-object v5, v4, v0

    array-length v5, v4

    move v0, v1

    :goto_0
    if-ge v0, v5, :cond_0

    aget-object v6, v4, v0

    .line 368
    new-instance v7, Ljava/io/File;

    iget-object v8, p0, Lcom/bereket/alacakverecek/MainActivity$6;->val$cache:Ljava/io/File;

    invoke-direct {v7, v8, v6}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-static {v7, v2, v3, v1}, Lcom/bereket/alacakverecek/MainActivity;->access$200(Ljava/io/File;JZ)V

    .line 367
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    .line 370
    :cond_0
    return-void
.end method
