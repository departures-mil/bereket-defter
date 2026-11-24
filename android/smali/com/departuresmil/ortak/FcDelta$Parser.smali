.class final Lcom/departuresmil/ortak/FcDelta$Parser;
.super Ljava/lang/Object;
.source "FcDelta.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/departuresmil/ortak/FcDelta;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x1a
    name = "Parser"
.end annotation


# instance fields
.field final copyBuf:[B

.field emitted:J

.field ended:Z

.field final fields:[J

.field final hd:Lcom/departuresmil/ortak/FcDelta$Header;

.field final md:Ljava/security/MessageDigest;

.field need:I

.field nf:I

.field final old:Ljava/io/RandomAccessFile;

.field op:I

.field final out:Ljava/io/OutputStream;

.field final progress:Lcom/departuresmil/ortak/FcDelta$Progress;

.field remain:J

.field shift:I

.field state:I

.field v:J

.field written:J


# direct methods
.method constructor <init>(Lcom/departuresmil/ortak/FcDelta$Header;Ljava/io/RandomAccessFile;Ljava/io/OutputStream;Ljava/security/MessageDigest;Lcom/departuresmil/ortak/FcDelta$Progress;)V
    .registers 9

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/high16 v0, 0x100000

    new-array v0, v0, [B

    iput-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->copyBuf:[B

    const/4 v0, 0x0

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->state:I

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->op:I

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->need:I

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->nf:I

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->shift:I

    const/4 v1, 0x2

    new-array v1, v1, [J

    iput-object v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->fields:[J

    const-wide/16 v1, 0x0

    iput-wide v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->v:J

    iput-wide v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->remain:J

    iput-wide v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->written:J

    iput-wide v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->emitted:J

    iput-boolean v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->ended:Z

    iput-object p1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->hd:Lcom/departuresmil/ortak/FcDelta$Header;

    iput-object p2, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->old:Ljava/io/RandomAccessFile;

    iput-object p3, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->out:Ljava/io/OutputStream;

    iput-object p4, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->md:Ljava/security/MessageDigest;

    iput-object p5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->progress:Lcom/departuresmil/ortak/FcDelta$Progress;

    return-void
.end method

.method private emit([BII)V
    .registers 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->out:Ljava/io/OutputStream;

    invoke-virtual {v0, p1, p2, p3}, Ljava/io/OutputStream;->write([BII)V

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->md:Ljava/security/MessageDigest;

    invoke-virtual {v0, p1, p2, p3}, Ljava/security/MessageDigest;->update([BII)V

    iget-wide p1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->emitted:J

    int-to-long v0, p3

    add-long/2addr p1, v0

    iput-wide p1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->emitted:J

    iget-object p3, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->progress:Lcom/departuresmil/ortak/FcDelta$Progress;

    if-eqz p3, :cond_0

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->hd:Lcom/departuresmil/ortak/FcDelta$Header;

    iget-wide v0, v0, Lcom/departuresmil/ortak/FcDelta$Header;->dstLen:J

    invoke-interface {p3, p1, p2, v0, v1}, Lcom/departuresmil/ortak/FcDelta$Progress;->onProgress(JJ)V

    :cond_0
    return-void
.end method

.method private exec()V
    .registers 14
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    iget v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->op:I

    const-wide/16 v1, 0x0

    const/4 v3, 0x0

    const/4 v4, 0x1

    if-ne v0, v4, :cond_2

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->fields:[J

    aget-wide v5, v0, v3

    aget-wide v7, v0, v4

    add-long v9, v5, v7

    cmp-long v0, v9, v1

    if-ltz v0, :cond_1

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->hd:Lcom/departuresmil/ortak/FcDelta$Header;

    iget-wide v11, v0, Lcom/departuresmil/ortak/FcDelta$Header;->srcLen:J

    cmp-long v0, v9, v11

    if-gtz v0, :cond_1

    invoke-direct {p0, v7, v8}, Lcom/departuresmil/ortak/FcDelta$Parser;->grow(J)V

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->old:Ljava/io/RandomAccessFile;

    invoke-virtual {v0, v5, v6}, Ljava/io/RandomAccessFile;->seek(J)V

    :goto_0
    cmp-long v0, v7, v1

    if-lez v0, :cond_0

    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->copyBuf:[B

    array-length v0, v0

    int-to-long v4, v0

    invoke-static {v7, v8, v4, v5}, Ljava/lang/Math;->min(JJ)J

    move-result-wide v4

    long-to-int v0, v4

    iget-object v4, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->old:Ljava/io/RandomAccessFile;

    iget-object v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->copyBuf:[B

    invoke-virtual {v4, v5, v3, v0}, Ljava/io/RandomAccessFile;->readFully([BII)V

    iget-object v4, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->copyBuf:[B

    invoke-direct {p0, v4, v3, v0}, Lcom/departuresmil/ortak/FcDelta$Parser;->emit([BII)V

    int-to-long v4, v0

    sub-long/2addr v7, v4

    goto :goto_0

    :cond_0
    iput v3, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->state:I

    goto :goto_1

    :cond_1
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: COPY aral\u0131\u011f\u0131 kaynak d\u0131\u015f\u0131nda"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_2
    iget-object v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->fields:[J

    aget-wide v4, v0, v3

    invoke-direct {p0, v4, v5}, Lcom/departuresmil/ortak/FcDelta$Parser;->grow(J)V

    iput-wide v4, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->remain:J

    cmp-long v0, v4, v1

    if-lez v0, :cond_3

    const/4 v3, 0x2

    :cond_3
    iput v3, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->state:I

    :goto_1
    return-void
.end method

.method private grow(J)V
    .registers 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/departuresmil/ortak/FcDelta$FcDeltaException;
        }
    .end annotation

    iget-wide v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->written:J

    add-long/2addr v0, p1

    iput-wide v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->written:J

    const-wide/16 p1, 0x0

    cmp-long p1, v0, p1

    if-ltz p1, :cond_0

    iget-object p1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->hd:Lcom/departuresmil/ortak/FcDelta$Header;

    iget-wide p1, p1, Lcom/departuresmil/ortak/FcDelta$Header;->dstLen:J

    cmp-long p1, v0, p1

    if-gtz p1, :cond_0

    return-void

    :cond_0
    new-instance p1, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string p2, "FCD1: \u00e7\u0131kt\u0131 dstLen de\u011ferini a\u015f\u0131yor"

    invoke-direct {p1, p2}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p1
.end method


# virtual methods
.method feed([BI)V
    .registers 14
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/4 v0, 0x0

    move v1, v0

    :cond_0
    :goto_0
    if-ge v1, p2, :cond_a

    iget-boolean v2, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->ended:Z

    if-nez v2, :cond_9

    iget v2, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->state:I

    const-wide/16 v3, 0x0

    const/4 v5, 0x1

    if-nez v2, :cond_5

    add-int/lit8 v2, v1, 0x1

    aget-byte v1, p1, v1

    and-int/lit16 v1, v1, 0xff

    iput v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->op:I

    if-nez v1, :cond_1

    iput-boolean v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->ended:Z

    goto :goto_2

    :cond_1
    const/4 v6, 0x2

    if-ne v1, v5, :cond_2

    iput v6, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->need:I

    goto :goto_1

    :cond_2
    if-ne v1, v6, :cond_4

    iput v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->need:I

    :goto_1
    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->nf:I

    iput-wide v3, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->v:J

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->shift:I

    iput v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->state:I

    :cond_3
    :goto_2
    move v1, v2

    goto :goto_0

    :cond_4
    new-instance p1, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    new-instance p2, Ljava/lang/StringBuilder;

    const-string v0, "FCD1: ge\u00e7ersiz op "

    invoke-direct {p2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->op:I

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p1

    :cond_5
    if-ne v2, v5, :cond_8

    add-int/lit8 v2, v1, 0x1

    aget-byte v1, p1, v1

    and-int/lit16 v5, v1, 0xff

    iget v6, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->shift:I

    const/16 v7, 0x38

    if-gt v6, v7, :cond_7

    iget-wide v7, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->v:J

    and-int/lit8 v1, v1, 0x7f

    int-to-long v9, v1

    shl-long/2addr v9, v6

    or-long/2addr v7, v9

    iput-wide v7, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->v:J

    add-int/lit8 v6, v6, 0x7

    iput v6, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->shift:I

    const/16 v1, 0x80

    if-ge v5, v1, :cond_3

    cmp-long v1, v7, v3

    if-ltz v1, :cond_6

    iget-object v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->fields:[J

    iget v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->nf:I

    add-int/lit8 v6, v5, 0x1

    iput v6, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->nf:I

    aput-wide v7, v1, v5

    iput-wide v3, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->v:J

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->shift:I

    iget v1, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->need:I

    if-ne v6, v1, :cond_3

    invoke-direct {p0}, Lcom/departuresmil/ortak/FcDelta$Parser;->exec()V

    goto :goto_2

    :cond_6
    new-instance p1, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string p2, "FCD1: varint \u00e7ok b\u00fcy\u00fck"

    invoke-direct {p1, p2}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p1

    :cond_7
    new-instance p1, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string p2, "FCD1: varint \u00e7ok uzun"

    invoke-direct {p1, p2}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p1

    :cond_8
    iget-wide v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->remain:J

    sub-int v2, p2, v1

    int-to-long v7, v2

    invoke-static {v5, v6, v7, v8}, Ljava/lang/Math;->min(JJ)J

    move-result-wide v5

    long-to-int v2, v5

    invoke-direct {p0, p1, v1, v2}, Lcom/departuresmil/ortak/FcDelta$Parser;->emit([BII)V

    add-int/2addr v1, v2

    iget-wide v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->remain:J

    int-to-long v7, v2

    sub-long/2addr v5, v7

    iput-wide v5, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->remain:J

    cmp-long v2, v5, v3

    if-nez v2, :cond_0

    iput v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->state:I

    goto/16 :goto_0

    :cond_9
    new-instance p1, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string p2, "FCD1: END sonras\u0131 fazla veri"

    invoke-direct {p1, p2}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p1

    :cond_a
    return-void
.end method

.method finish()V
    .registers 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/departuresmil/ortak/FcDelta$FcDeltaException;
        }
    .end annotation

    iget-boolean v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->ended:Z

    if-eqz v0, :cond_1

    iget-wide v0, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->written:J

    iget-object v2, p0, Lcom/departuresmil/ortak/FcDelta$Parser;->hd:Lcom/departuresmil/ortak/FcDelta$Header;

    iget-wide v2, v2, Lcom/departuresmil/ortak/FcDelta$Header;->dstLen:J

    cmp-long v0, v0, v2

    if-nez v0, :cond_0

    return-void

    :cond_0
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: \u00e7\u0131kt\u0131 uzunlu\u011fu dstLen ile uyu\u015fmuyor"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_1
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: END op yok (yama kesik)"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0
.end method
