.class public final Lcom/departuresmil/ortak/FcDelta;
.super Ljava/lang/Object;
.source "FcDelta.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/departuresmil/ortak/FcDelta$Header;,
        Lcom/departuresmil/ortak/FcDelta$FcDeltaException;,
        Lcom/departuresmil/ortak/FcDelta$Parser;,
        Lcom/departuresmil/ortak/FcDelta$Progress;
    }
.end annotation


# static fields
.field public static final CODEC_ZLIB:I = 0x1

.field public static final HEADER_LEN:I = 0x55

.field private static final IO_BLOCK:I = 0x100000

.field private static final MAGIC:[B

.field private static final OP_COPY:I = 0x1

.field private static final OP_END:I = 0x0

.field private static final OP_INSERT:I = 0x2


# direct methods
.method static constructor <clinit>()V
    .registers 1

    const/4 v0, 0x4

    new-array v0, v0, [B

    fill-array-data v0, :array_0

    sput-object v0, Lcom/departuresmil/ortak/FcDelta;->MAGIC:[B

    return-void

    nop

    :array_0
    .array-data 1
        0x46t
        0x43t
        0x44t
        0x31t
    .end array-data
.end method

.method private constructor <init>()V
    .registers 1

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static apply(Ljava/io/File;Ljava/io/File;Ljava/io/File;Lcom/departuresmil/ortak/FcDelta$Progress;)Lcom/departuresmil/ortak/FcDelta$Header;
    .registers 20
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    move-object/from16 v0, p2

    invoke-static/range {p1 .. p1}, Lcom/departuresmil/ortak/FcDelta;->readHeader(Ljava/io/File;)Lcom/departuresmil/ortak/FcDelta$Header;

    move-result-object v7

    invoke-virtual/range {p0 .. p0}, Ljava/io/File;->length()J

    move-result-wide v1

    iget-wide v3, v7, Lcom/departuresmil/ortak/FcDelta$Header;->srcLen:J

    cmp-long v1, v1, v3

    if-nez v1, :cond_a

    invoke-static/range {p0 .. p0}, Lcom/departuresmil/ortak/FcDelta;->sha256(Ljava/io/File;)[B

    move-result-object v1

    iget-object v2, v7, Lcom/departuresmil/ortak/FcDelta$Header;->srcSha256:[B

    invoke-static {v1, v2}, Ljava/util/Arrays;->equals([B[B)Z

    move-result v1

    if-eqz v1, :cond_a

    new-instance v8, Ljava/io/File;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v2, ".part"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v8, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    new-instance v9, Ljava/io/RandomAccessFile;

    const-string v1, "r"

    move-object/from16 v2, p0

    invoke-direct {v9, v2, v1}, Ljava/io/RandomAccessFile;-><init>(Ljava/io/File;Ljava/lang/String;)V

    new-instance v10, Ljava/io/FileOutputStream;

    invoke-direct {v10, v8}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    new-instance v11, Ljava/io/FileInputStream;

    move-object/from16 v1, p1

    invoke-direct {v11, v1}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    new-instance v12, Ljava/util/zip/Inflater;

    const/4 v13, 0x0

    invoke-direct {v12, v13}, Ljava/util/zip/Inflater;-><init>(Z)V

    const-wide/16 v1, 0x55

    :try_start_0
    invoke-static {v11, v1, v2}, Lcom/departuresmil/ortak/FcDelta;->skipFully(Ljava/io/InputStream;J)V

    invoke-static {}, Lcom/departuresmil/ortak/FcDelta;->newSha()Ljava/security/MessageDigest;

    move-result-object v14

    new-instance v15, Lcom/departuresmil/ortak/FcDelta$Parser;

    move-object v1, v15

    move-object v2, v7

    move-object v3, v9

    move-object v4, v10

    move-object v5, v14

    move-object/from16 v6, p3

    invoke-direct/range {v1 .. v6}, Lcom/departuresmil/ortak/FcDelta$Parser;-><init>(Lcom/departuresmil/ortak/FcDelta$Header;Ljava/io/RandomAccessFile;Ljava/io/OutputStream;Ljava/security/MessageDigest;Lcom/departuresmil/ortak/FcDelta$Progress;)V

    const/high16 v1, 0x40000

    new-array v2, v1, [B

    new-array v1, v1, [B

    :goto_0
    invoke-virtual {v12}, Ljava/util/zip/Inflater;->finished()Z

    move-result v3

    if-eqz v3, :cond_5

    invoke-virtual {v12}, Ljava/util/zip/Inflater;->getRemaining()I

    move-result v1

    if-gtz v1, :cond_4

    invoke-virtual {v11}, Ljava/io/InputStream;->read()I

    move-result v1

    if-gez v1, :cond_4

    invoke-virtual {v15}, Lcom/departuresmil/ortak/FcDelta$Parser;->finish()V

    invoke-virtual {v10}, Ljava/io/OutputStream;->close()V

    const/4 v10, 0x0

    invoke-virtual {v14}, Ljava/security/MessageDigest;->digest()[B

    move-result-object v1

    iget-object v2, v7, Lcom/departuresmil/ortak/FcDelta$Header;->dstSha256:[B

    invoke-static {v1, v2}, Ljava/util/Arrays;->equals([B[B)Z

    move-result v1

    if-eqz v1, :cond_3

    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->exists()Z

    move-result v1

    if-eqz v1, :cond_1

    invoke-virtual/range {p2 .. p2}, Ljava/io/File;->delete()Z

    move-result v1

    if-eqz v1, :cond_0

    goto :goto_1

    :cond_0
    new-instance v1, Ljava/io/IOException;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "silinemedi: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v1

    :cond_1
    :goto_1
    invoke-virtual {v8, v0}, Ljava/io/File;->renameTo(Ljava/io/File;)Z

    move-result v1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v1, :cond_2

    invoke-virtual {v12}, Ljava/util/zip/Inflater;->end()V

    invoke-static {v11}, Lcom/departuresmil/ortak/FcDelta;->closeQuietly(Ljava/io/Closeable;)V

    invoke-static {v10}, Lcom/departuresmil/ortak/FcDelta;->closeQuietly(Ljava/io/Closeable;)V

    invoke-static {v9}, Lcom/departuresmil/ortak/FcDelta;->closeQuietly(Ljava/io/Closeable;)V

    return-object v7

    :cond_2
    :try_start_1
    new-instance v1, Ljava/io/IOException;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "ta\u015f\u0131namad\u0131: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v1

    :cond_3
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: sonu\u00e7 SHA-256 uyu\u015fmuyor"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_4
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: zlib ak\u0131\u015f\u0131ndan sonra fazla veri"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_5
    invoke-virtual {v12}, Ljava/util/zip/Inflater;->needsInput()Z

    move-result v3

    if-eqz v3, :cond_7

    invoke-virtual {v11, v2}, Ljava/io/InputStream;->read([B)I

    move-result v3

    if-ltz v3, :cond_6

    invoke-virtual {v12, v2, v13, v3}, Ljava/util/zip/Inflater;->setInput([BII)V

    goto :goto_2

    :cond_6
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: zlib ak\u0131\u015f\u0131 kesik"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    :cond_7
    :goto_2
    :try_start_2
    invoke-virtual {v12, v1}, Ljava/util/zip/Inflater;->inflate([B)I

    move-result v3
    :try_end_2
    .catch Ljava/util/zip/DataFormatException; {:try_start_2 .. :try_end_2} :catch_0
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    if-lez v3, :cond_8

    :try_start_3
    invoke-virtual {v15, v1, v3}, Lcom/departuresmil/ortak/FcDelta$Parser;->feed([BI)V

    goto/16 :goto_0

    :cond_8
    invoke-virtual {v12}, Ljava/util/zip/Inflater;->needsDictionary()Z

    move-result v3

    if-nez v3, :cond_9

    goto/16 :goto_0

    :cond_9
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: zlib s\u00f6zl\u00fck istiyor"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0

    :catch_0
    move-exception v0

    move-object v1, v0

    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "FCD1: bozuk zlib verisi: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/util/zip/DataFormatException;->getMessage()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_0

    :catchall_0
    move-exception v0

    invoke-virtual {v12}, Ljava/util/zip/Inflater;->end()V

    invoke-static {v11}, Lcom/departuresmil/ortak/FcDelta;->closeQuietly(Ljava/io/Closeable;)V

    invoke-static {v10}, Lcom/departuresmil/ortak/FcDelta;->closeQuietly(Ljava/io/Closeable;)V

    invoke-static {v9}, Lcom/departuresmil/ortak/FcDelta;->closeQuietly(Ljava/io/Closeable;)V

    invoke-virtual {v8}, Ljava/io/File;->delete()Z

    throw v0

    :cond_a
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v1, "FCD1: kurulu dosya yaman\u0131n kayna\u011f\u0131 de\u011fil"

    invoke-direct {v0, v1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method private static closeQuietly(Ljava/io/Closeable;)V
    .registers 1

    if-nez p0, :cond_0

    return-void

    :cond_0
    :try_start_0
    invoke-interface {p0}, Ljava/io/Closeable;->close()V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    :catch_0
    return-void
.end method

.method public static hex([B)Ljava/lang/String;
    .registers 7

    new-instance v0, Ljava/lang/StringBuilder;

    array-length v1, p0

    mul-int/lit8 v1, v1, 0x2

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(I)V

    array-length v1, p0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_0

    aget-byte v3, p0, v2

    shr-int/lit8 v4, v3, 0x4

    and-int/lit8 v4, v4, 0xf

    const/16 v5, 0x10

    invoke-static {v4, v5}, Ljava/lang/Character;->forDigit(II)C

    move-result v4

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    and-int/lit8 v3, v3, 0xf

    invoke-static {v3, v5}, Ljava/lang/Character;->forDigit(II)C

    move-result v3

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_0
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method

.method public static main([Ljava/lang/String;)V
    .registers 8

    const-string v0, "ok "

    array-length v1, p0

    const/4 v2, 0x4

    const/4 v3, 0x2

    if-ne v1, v2, :cond_0

    const/4 v1, 0x0

    aget-object v1, p0, v1

    const-string v2, "apply"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_1

    :cond_0
    sget-object v1, Ljava/lang/System;->err:Ljava/io/PrintStream;

    const-string v2, "kullan\u0131m: FcDelta apply <old> <patch> <out>"

    invoke-virtual {v1, v2}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    invoke-static {v3}, Ljava/lang/System;->exit(I)V

    :cond_1
    const/4 v1, 0x1

    :try_start_0
    new-instance v2, Ljava/io/File;

    aget-object v4, p0, v1

    invoke-direct {v2, v4}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    new-instance v4, Ljava/io/File;

    aget-object v3, p0, v3

    invoke-direct {v4, v3}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    new-instance v3, Ljava/io/File;

    const/4 v5, 0x3

    aget-object v6, p0, v5

    invoke-direct {v3, v6}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    const/4 v6, 0x0

    invoke-static {v2, v4, v3, v6}, Lcom/departuresmil/ortak/FcDelta;->apply(Ljava/io/File;Ljava/io/File;Ljava/io/File;Lcom/departuresmil/ortak/FcDelta$Progress;)Lcom/departuresmil/ortak/FcDelta$Header;

    move-result-object v2

    sget-object v3, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    aget-object p0, p0, v5

    invoke-virtual {v4, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, " sha256="

    invoke-virtual {v4, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Lcom/departuresmil/ortak/FcDelta$Header;->dstSha256Hex()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v4, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v3, p0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception p0

    sget-object v0, Ljava/lang/System;->err:Ljava/io/PrintStream;

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "hata: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0}, Ljava/io/IOException;->getMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    invoke-static {v1}, Ljava/lang/System;->exit(I)V

    :goto_0
    return-void
.end method

.method private static newSha()Ljava/security/MessageDigest;
    .registers 2

    :try_start_0
    const-string v0, "SHA-256"

    invoke-static {v0}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;

    move-result-object v0
    :try_end_0
    .catch Ljava/security/NoSuchAlgorithmException; {:try_start_0 .. :try_end_0} :catch_0

    return-object v0

    :catch_0
    move-exception v0

    new-instance v1, Ljava/lang/IllegalStateException;

    invoke-direct {v1, v0}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/Throwable;)V

    throw v1
.end method

.method public static parseHeader([B)Lcom/departuresmil/ortak/FcDelta$Header;
    .registers 11
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/departuresmil/ortak/FcDelta$FcDeltaException;
        }
    .end annotation

    array-length v0, p0

    const/16 v1, 0x55

    if-lt v0, v1, :cond_4

    const/4 v0, 0x0

    :goto_0
    const/4 v2, 0x4

    if-ge v0, v2, :cond_1

    aget-byte v2, p0, v0

    sget-object v3, Lcom/departuresmil/ortak/FcDelta;->MAGIC:[B

    aget-byte v3, v3, v0

    if-ne v2, v3, :cond_0

    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_0
    new-instance p0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v0, "FCD1: yama dosyas\u0131 de\u011fil"

    invoke-direct {p0, v0}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p0

    :cond_1
    aget-byte v0, p0, v2

    and-int/lit16 v0, v0, 0xff

    const/4 v3, 0x1

    if-ne v0, v3, :cond_3

    const/4 v0, 0x5

    invoke-static {p0, v0}, Lcom/departuresmil/ortak/FcDelta;->u64([BI)J

    move-result-wide v3

    const/16 v0, 0x2d

    invoke-static {p0, v0}, Lcom/departuresmil/ortak/FcDelta;->u64([BI)J

    move-result-wide v6

    const-wide/16 v8, 0x0

    cmp-long v2, v3, v8

    if-ltz v2, :cond_2

    cmp-long v2, v6, v8

    if-ltz v2, :cond_2

    new-instance v9, Lcom/departuresmil/ortak/FcDelta$Header;

    const/16 v2, 0xd

    invoke-static {p0, v2, v0}, Ljava/util/Arrays;->copyOfRange([BII)[B

    move-result-object v5

    const/16 v0, 0x35

    invoke-static {p0, v0, v1}, Ljava/util/Arrays;->copyOfRange([BII)[B

    move-result-object v8

    move-object v2, v9

    invoke-direct/range {v2 .. v8}, Lcom/departuresmil/ortak/FcDelta$Header;-><init>(J[BJ[B)V

    return-object v9

    :cond_2
    new-instance p0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v0, "FCD1: uzunluk \u00e7ok b\u00fcy\u00fck"

    invoke-direct {p0, v0}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p0

    :cond_3
    new-instance v0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v3, "FCD1: bilinmeyen codec "

    invoke-direct {v1, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    aget-byte p0, p0, v2

    and-int/lit16 p0, p0, 0xff

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_4
    new-instance p0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string v0, "FCD1: yama \u00e7ok k\u0131sa"

    invoke-direct {p0, v0}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p0
.end method

.method private static readFully(Ljava/io/InputStream;[BII)V
    .registers 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    :goto_0
    if-lez p3, :cond_1

    invoke-virtual {p0, p1, p2, p3}, Ljava/io/InputStream;->read([BII)I

    move-result v0

    if-ltz v0, :cond_0

    add-int/2addr p2, v0

    sub-int/2addr p3, v0

    goto :goto_0

    :cond_0
    new-instance p0, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;

    const-string p1, "FCD1: yama \u00e7ok k\u0131sa"

    invoke-direct {p0, p1}, Lcom/departuresmil/ortak/FcDelta$FcDeltaException;-><init>(Ljava/lang/String;)V

    throw p0

    :cond_1
    return-void
.end method

.method public static readHeader(Ljava/io/File;)Lcom/departuresmil/ortak/FcDelta$Header;
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    new-instance v0, Ljava/io/FileInputStream;

    invoke-direct {v0, p0}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    const/16 p0, 0x55

    :try_start_0
    new-array v1, p0, [B

    const/4 v2, 0x0

    invoke-static {v0, v1, v2, p0}, Lcom/departuresmil/ortak/FcDelta;->readFully(Ljava/io/InputStream;[BII)V

    invoke-static {v1}, Lcom/departuresmil/ortak/FcDelta;->parseHeader([B)Lcom/departuresmil/ortak/FcDelta$Header;

    move-result-object p0
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    invoke-virtual {v0}, Ljava/io/InputStream;->close()V

    return-object p0

    :catchall_0
    move-exception p0

    invoke-virtual {v0}, Ljava/io/InputStream;->close()V

    throw p0
.end method

.method public static sha256(Ljava/io/File;)[B
    .registers 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    invoke-static {}, Lcom/departuresmil/ortak/FcDelta;->newSha()Ljava/security/MessageDigest;

    move-result-object v0

    new-instance v1, Ljava/io/FileInputStream;

    invoke-direct {v1, p0}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    const/high16 p0, 0x100000

    :try_start_0
    new-array p0, p0, [B

    :goto_0
    invoke-virtual {v1, p0}, Ljava/io/InputStream;->read([B)I

    move-result v2

    if-lez v2, :cond_0

    const/4 v3, 0x0

    invoke-virtual {v0, p0, v3, v2}, Ljava/security/MessageDigest;->update([BII)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    goto :goto_0

    :cond_0
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V

    invoke-virtual {v0}, Ljava/security/MessageDigest;->digest()[B

    move-result-object p0

    return-object p0

    :catchall_0
    move-exception p0

    invoke-virtual {v1}, Ljava/io/InputStream;->close()V

    throw p0
.end method

.method private static skipFully(Ljava/io/InputStream;J)V
    .registers 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    long-to-int p1, p1

    new-array p2, p1, [B

    const/4 v0, 0x0

    invoke-static {p0, p2, v0, p1}, Lcom/departuresmil/ortak/FcDelta;->readFully(Ljava/io/InputStream;[BII)V

    return-void
.end method

.method private static u64([BI)J
    .registers 9

    const-wide/16 v0, 0x0

    const/4 v2, 0x7

    :goto_0
    if-ltz v2, :cond_0

    const/16 v3, 0x8

    shl-long/2addr v0, v3

    add-int v3, p1, v2

    aget-byte v3, p0, v3

    int-to-long v3, v3

    const-wide/16 v5, 0xff

    and-long/2addr v3, v5

    or-long/2addr v0, v3

    add-int/lit8 v2, v2, -0x1

    goto :goto_0

    :cond_0
    return-wide v0
.end method
