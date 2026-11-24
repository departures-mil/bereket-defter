.class public final Lcom/departuresmil/ortak/FcDelta$Header;
.super Ljava/lang/Object;
.source "FcDelta.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/departuresmil/ortak/FcDelta;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x19
    name = "Header"
.end annotation


# instance fields
.field public final dstLen:J

.field public final dstSha256:[B

.field public final srcLen:J

.field public final srcSha256:[B


# direct methods
.method constructor <init>(J[BJ[B)V
    .registers 7

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-wide p1, p0, Lcom/departuresmil/ortak/FcDelta$Header;->srcLen:J

    iput-object p3, p0, Lcom/departuresmil/ortak/FcDelta$Header;->srcSha256:[B

    iput-wide p4, p0, Lcom/departuresmil/ortak/FcDelta$Header;->dstLen:J

    iput-object p6, p0, Lcom/departuresmil/ortak/FcDelta$Header;->dstSha256:[B

    return-void
.end method


# virtual methods
.method public dstSha256Hex()Ljava/lang/String;
    .registers 2

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Header;->dstSha256:[B

    invoke-static {v0}, Lcom/departuresmil/ortak/FcDelta;->hex([B)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public srcSha256Hex()Ljava/lang/String;
    .registers 2

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Header;->srcSha256:[B

    invoke-static {v0}, Lcom/departuresmil/ortak/FcDelta;->hex([B)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
