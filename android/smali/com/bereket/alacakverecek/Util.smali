.class final Lcom/bereket/alacakverecek/Util;
.super Ljava/lang/Object;
.source "Util.java"


# static fields
.field private static final EXT2MIME:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private static final MIME2EXT:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field static final OCTET:Ljava/lang/String; = "application/octet-stream"


# direct methods
.method static constructor <clinit>()V
    .locals 4

    .prologue
    const/4 v3, 0x0

    const/4 v2, 0x1

    .line 18
    new-instance v0, Ljava/util/HashMap;

    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    sput-object v0, Lcom/bereket/alacakverecek/Util;->EXT2MIME:Ljava/util/Map;

    .line 19
    new-instance v0, Ljava/util/HashMap;

    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    sput-object v0, Lcom/bereket/alacakverecek/Util;->MIME2EXT:Ljava/util/Map;

    .line 27
    const-string v0, "html"

    const-string v1, "text/html"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 28
    const-string v0, "htm"

    const-string v1, "text/html"

    invoke-static {v0, v1, v3}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 29
    const-string v0, "js"

    const-string v1, "text/javascript"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 30
    const-string v0, "mjs"

    const-string v1, "text/javascript"

    invoke-static {v0, v1, v3}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 31
    const-string v0, "css"

    const-string v1, "text/css"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 32
    const-string v0, "json"

    const-string v1, "application/json"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 33
    const-string v0, "map"

    const-string v1, "application/json"

    invoke-static {v0, v1, v3}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 34
    const-string v0, "webmanifest"

    const-string v1, "application/manifest+json"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 35
    const-string v0, "txt"

    const-string v1, "text/plain"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 36
    const-string v0, "csv"

    const-string v1, "text/csv"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 37
    const-string v0, "xml"

    const-string v1, "application/xml"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 38
    const-string v0, "svg"

    const-string v1, "image/svg+xml"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 39
    const-string v0, "png"

    const-string v1, "image/png"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 40
    const-string v0, "jpg"

    const-string v1, "image/jpeg"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 41
    const-string v0, "jpeg"

    const-string v1, "image/jpeg"

    invoke-static {v0, v1, v3}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 42
    const-string v0, "gif"

    const-string v1, "image/gif"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 43
    const-string v0, "webp"

    const-string v1, "image/webp"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 44
    const-string v0, "ico"

    const-string v1, "image/x-icon"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 45
    const-string v0, "bmp"

    const-string v1, "image/bmp"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 46
    const-string v0, "woff"

    const-string v1, "font/woff"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 47
    const-string v0, "woff2"

    const-string v1, "font/woff2"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 48
    const-string v0, "ttf"

    const-string v1, "font/ttf"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 49
    const-string v0, "otf"

    const-string v1, "font/otf"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 50
    const-string v0, "wasm"

    const-string v1, "application/wasm"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 51
    const-string v0, "pdf"

    const-string v1, "application/pdf"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 52
    const-string v0, "zip"

    const-string v1, "application/zip"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 53
    const-string v0, "apk"

    const-string v1, "application/vnd.android.package-archive"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 54
    const-string v0, "doc"

    const-string v1, "application/msword"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 55
    const-string v0, "docx"

    const-string v1, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 56
    const-string v0, "xls"

    const-string v1, "application/vnd.ms-excel"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 57
    const-string v0, "xlsx"

    const-string v1, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 58
    const-string v0, "mp3"

    const-string v1, "audio/mpeg"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 59
    const-string v0, "wav"

    const-string v1, "audio/wav"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 60
    const-string v0, "ogg"

    const-string v1, "audio/ogg"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 61
    const-string v0, "mp4"

    const-string v1, "video/mp4"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 62
    const-string v0, "webm"

    const-string v1, "video/webm"

    invoke-static {v0, v1, v2}, Lcom/bereket/alacakverecek/Util;->m(Ljava/lang/String;Ljava/lang/String;Z)V

    .line 64
    sget-object v0, Lcom/bereket/alacakverecek/Util;->MIME2EXT:Ljava/util/Map;

    const-string v1, "application/javascript"

    const-string v2, "js"

    invoke-interface {v0, v1, v2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 65
    sget-object v0, Lcom/bereket/alacakverecek/Util;->MIME2EXT:Ljava/util/Map;

    const-string v1, "image/jpg"

    const-string v2, "jpg"

    invoke-interface {v0, v1, v2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 66
    sget-object v0, Lcom/bereket/alacakverecek/Util;->MIME2EXT:Ljava/util/Map;

    const-string v1, "text/comma-separated-values"

    const-string v2, "csv"

    invoke-interface {v0, v1, v2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 67
    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .prologue
    .line 14
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method static acceptToMimes([Ljava/lang/String;)Ljava/util/List;
    .locals 11
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "([",
            "Ljava/lang/String;",
            ")",
            "Ljava/util/List",
            "<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation

    .prologue
    const/4 v5, 0x0

    const/4 v2, 0x1

    .line 209
    new-instance v3, Ljava/util/ArrayList;

    invoke-direct {v3}, Ljava/util/ArrayList;-><init>()V

    .line 210
    if-nez p0, :cond_0

    move-object v0, v3

    .line 232
    :goto_0
    return-object v0

    .line 212
    :cond_0
    array-length v7, p0

    move v6, v5

    move v1, v5

    :goto_1
    if-ge v6, v7, :cond_9

    aget-object v0, p0, v6

    .line 213
    if-nez v0, :cond_2

    .line 212
    :cond_1
    add-int/lit8 v0, v6, 0x1

    move v6, v0

    goto :goto_1

    .line 214
    :cond_2
    const-string v4, ","

    invoke-virtual {v0, v4}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v8

    array-length v9, v8

    move v4, v5

    :goto_2
    if-ge v4, v9, :cond_1

    aget-object v0, v8, v4

    .line 215
    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    sget-object v10, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v0, v10}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v0

    .line 216
    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v10

    if-nez v10, :cond_3

    move v0, v1

    .line 214
    :goto_3
    add-int/lit8 v4, v4, 0x1

    move v1, v0

    goto :goto_2

    .line 218
    :cond_3
    const-string v10, "."

    invoke-virtual {v0, v10}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v10

    if-eqz v10, :cond_4

    .line 219
    sget-object v10, Lcom/bereket/alacakverecek/Util;->EXT2MIME:Ljava/util/Map;

    invoke-virtual {v0, v2}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v0

    invoke-interface {v10, v0}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    .line 220
    if-nez v0, :cond_5

    move v0, v2

    goto :goto_3

    .line 221
    :cond_4
    const/16 v10, 0x2f

    invoke-virtual {v0, v10}, Ljava/lang/String;->indexOf(I)I

    move-result v10

    if-lez v10, :cond_6

    .line 227
    :cond_5
    const-string v10, "*/*"

    invoke-virtual {v0, v10}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v10

    if-eqz v10, :cond_7

    move v0, v2

    goto :goto_3

    :cond_6
    move v0, v2

    .line 225
    goto :goto_3

    .line 228
    :cond_7
    invoke-interface {v3, v0}, Ljava/util/List;->contains(Ljava/lang/Object;)Z

    move-result v10

    if-nez v10, :cond_8

    invoke-interface {v3, v0}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    :cond_8
    move v0, v1

    goto :goto_3

    .line 231
    :cond_9
    if-eqz v1, :cond_a

    invoke-interface {v3}, Ljava/util/List;->clear()V

    :cond_a
    move-object v0, v3

    .line 232
    goto :goto_0
.end method

.method static acceptsImages(Ljava/util/List;)Z
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List",
            "<",
            "Ljava/lang/String;",
            ">;)Z"
        }
    .end annotation

    .prologue
    const/4 v1, 0x1

    .line 237
    invoke-interface {p0}, Ljava/util/List;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_0

    move v0, v1

    .line 241
    :goto_0
    return v0

    .line 238
    :cond_0
    invoke-interface {p0}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v2

    :cond_1
    invoke-interface {v2}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    if-eqz v0, :cond_3

    invoke-interface {v2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    .line 239
    const-string v3, "image/*"

    invoke-virtual {v0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-nez v3, :cond_2

    const-string v3, "image/jpeg"

    invoke-virtual {v0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-nez v3, :cond_2

    const-string v3, "image/jpg"

    invoke-virtual {v0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1

    :cond_2
    move v0, v1

    goto :goto_0

    .line 241
    :cond_3
    const/4 v0, 0x0

    goto :goto_0
.end method

.method static assetPathForUrlPath(Ljava/lang/String;)Ljava/lang/String;
    .locals 8

    .prologue
    const/4 v0, 0x0

    const/4 v3, 0x0

    .line 191
    if-eqz p0, :cond_0

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    if-eqz v1, :cond_0

    const-string v1, "/"

    invoke-virtual {p0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_2

    :cond_0
    const-string v0, "www/index.html"

    .line 201
    :cond_1
    :goto_0
    return-object v0

    .line 192
    :cond_2
    const-string v1, "/"

    invoke-virtual {p0, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v1

    if-nez v1, :cond_3

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "/"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    .line 193
    :cond_3
    const-string v1, "/"

    invoke-virtual {p0, v1}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_4

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "index.html"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    .line 194
    :cond_4
    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v1

    .line 195
    const-string v2, "www/"

    invoke-virtual {v1, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_1

    .line 196
    const-string v2, "/"

    const/4 v4, -0x1

    invoke-virtual {v1, v2, v4}, Ljava/lang/String;->split(Ljava/lang/String;I)[Ljava/lang/String;

    move-result-object v4

    .line 197
    array-length v5, v4

    move v2, v3

    :goto_1
    if-ge v2, v5, :cond_5

    aget-object v6, v4, v2

    .line 198
    invoke-virtual {v6}, Ljava/lang/String;->length()I

    move-result v7

    if-eqz v7, :cond_1

    const-string v7, "."

    invoke-virtual {v6, v7}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v7

    if-nez v7, :cond_1

    const-string v7, ".."

    invoke-virtual {v6, v7}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v7

    if-nez v7, :cond_1

    const/16 v7, 0x5c

    invoke-virtual {v6, v7}, Ljava/lang/String;->indexOf(I)I

    move-result v7

    if-gez v7, :cond_1

    .line 199
    invoke-virtual {v6, v3}, Ljava/lang/String;->indexOf(I)I

    move-result v6

    if-gez v6, :cond_1

    .line 197
    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_5
    move-object v0, v1

    .line 201
    goto :goto_0
.end method

.method static compareVersions(Ljava/lang/String;Ljava/lang/String;)I
    .locals 7

    .prologue
    const/4 v1, 0x0

    .line 251
    if-nez p0, :cond_0

    const-string v0, ""

    :goto_0
    const-string v2, "\\."

    invoke-virtual {v0, v2}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v4

    .line 252
    if-nez p1, :cond_1

    const-string v0, ""

    :goto_1
    const-string v2, "\\."

    invoke-virtual {v0, v2}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v5

    .line 253
    array-length v0, v4

    array-length v2, v5

    invoke-static {v0, v2}, Ljava/lang/Math;->max(II)I

    move-result v6

    move v3, v1

    .line 254
    :goto_2
    if-ge v3, v6, :cond_6

    .line 255
    array-length v0, v4

    if-ge v3, v0, :cond_2

    aget-object v0, v4, v3

    invoke-static {v0}, Lcom/bereket/alacakverecek/Util;->num(Ljava/lang/String;)I

    move-result v0

    .line 256
    :goto_3
    array-length v2, v5

    if-ge v3, v2, :cond_3

    aget-object v2, v5, v3

    invoke-static {v2}, Lcom/bereket/alacakverecek/Util;->num(Ljava/lang/String;)I

    move-result v2

    .line 257
    :goto_4
    if-eq v0, v2, :cond_5

    if-ge v0, v2, :cond_4

    const/4 v0, -0x1

    .line 259
    :goto_5
    return v0

    .line 251
    :cond_0
    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    goto :goto_0

    .line 252
    :cond_1
    invoke-virtual {p1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    goto :goto_1

    :cond_2
    move v0, v1

    .line 255
    goto :goto_3

    :cond_3
    move v2, v1

    .line 256
    goto :goto_4

    .line 257
    :cond_4
    const/4 v0, 0x1

    goto :goto_5

    .line 254
    :cond_5
    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_2

    :cond_6
    move v0, v1

    .line 259
    goto :goto_5
.end method

.method static effectiveMime(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 3

    .prologue
    .line 101
    if-eqz p0, :cond_1

    .line 102
    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    .line 103
    const/16 v1, 0x3b

    invoke-virtual {v0, v1}, Ljava/lang/String;->indexOf(I)I

    move-result v1

    .line 104
    if-ltz v1, :cond_0

    const/4 v2, 0x0

    invoke-virtual {v0, v2, v1}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    .line 105
    :cond_0
    sget-object v1, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v0, v1}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v0

    .line 106
    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v1

    if-lez v1, :cond_1

    const/16 v1, 0x2f

    invoke-virtual {v0, v1}, Ljava/lang/String;->indexOf(I)I

    move-result v1

    if-lez v1, :cond_1

    .line 108
    :goto_0
    return-object v0

    :cond_1
    const-string v0, "application/octet-stream"

    invoke-static {p1, v0}, Lcom/bereket/alacakverecek/Util;->mimeForNameOr(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method

.method static extension(Ljava/lang/String;)Ljava/lang/String;
    .locals 2

    .prologue
    const/4 v1, 0x0

    .line 71
    if-nez p0, :cond_0

    const-string v0, ""

    .line 80
    :goto_0
    return-object v0

    .line 72
    :cond_0
    const/16 v0, 0x3f

    invoke-virtual {p0, v0}, Ljava/lang/String;->indexOf(I)I

    move-result v0

    .line 73
    if-ltz v0, :cond_1

    invoke-virtual {p0, v1, v0}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object p0

    .line 74
    :cond_1
    const/16 v0, 0x23

    invoke-virtual {p0, v0}, Ljava/lang/String;->indexOf(I)I

    move-result v0

    .line 75
    if-ltz v0, :cond_2

    invoke-virtual {p0, v1, v0}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object p0

    .line 76
    :cond_2
    const/16 v0, 0x2f

    invoke-virtual {p0, v0}, Ljava/lang/String;->lastIndexOf(I)I

    move-result v0

    .line 77
    if-ltz v0, :cond_3

    add-int/lit8 v0, v0, 0x1

    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p0

    .line 78
    :cond_3
    const/16 v0, 0x2e

    invoke-virtual {p0, v0}, Ljava/lang/String;->lastIndexOf(I)I

    move-result v0

    .line 79
    if-ltz v0, :cond_4

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    add-int/lit8 v1, v1, -0x1

    if-ne v0, v1, :cond_5

    :cond_4
    const-string v0, ""

    goto :goto_0

    .line 80
    :cond_5
    add-int/lit8 v0, v0, 0x1

    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v0

    sget-object v1, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {v0, v1}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method

.method static isSafeVersion(Ljava/lang/String;)Z
    .locals 1

    .prologue
    .line 246
    if-eqz p0, :cond_0

    const-string v0, "[0-9]{1,4}(\\.[0-9]{1,4}){0,3}"

    invoke-virtual {p0, v0}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method static isTextMime(Ljava/lang/String;)Z
    .locals 2

    .prologue
    const/4 v0, 0x0

    .line 94
    if-nez p0, :cond_1

    .line 95
    :cond_0
    :goto_0
    return v0

    :cond_1
    const-string v1, "text/"

    invoke-virtual {p0, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v1

    if-nez v1, :cond_2

    const-string v1, "application/json"

    invoke-virtual {p0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_2

    const-string v1, "application/xml"

    invoke-virtual {p0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_2

    const-string v1, "application/manifest+json"

    .line 96
    invoke-virtual {p0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_2

    const-string v1, "image/svg+xml"

    invoke-virtual {p0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_0

    :cond_2
    const/4 v0, 0x1

    goto :goto_0
.end method

.method static isUrlSafeBase64(Ljava/lang/String;)Z
    .locals 1

    .prologue
    .line 158
    const/16 v0, 0x2d

    invoke-virtual {p0, v0}, Ljava/lang/String;->indexOf(I)I

    move-result v0

    if-gez v0, :cond_0

    const/16 v0, 0x5f

    invoke-virtual {p0, v0}, Ljava/lang/String;->indexOf(I)I

    move-result v0

    if-ltz v0, :cond_1

    :cond_0
    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_1
    const/4 v0, 0x0

    goto :goto_0
.end method

.method static jsString(Ljava/lang/String;)Ljava/lang/String;
    .locals 8

    .prologue
    const/16 v7, 0x22

    const/4 v1, 0x0

    .line 163
    if-nez p0, :cond_0

    const-string v0, "null"

    .line 183
    :goto_0
    return-object v0

    .line 164
    :cond_0
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v0

    add-int/lit8 v0, v0, 0x2

    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(I)V

    .line 165
    invoke-virtual {v2, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move v0, v1

    .line 166
    :goto_1
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    if-ge v0, v3, :cond_3

    .line 167
    invoke-virtual {p0, v0}, Ljava/lang/String;->charAt(I)C

    move-result v3

    .line 168
    sparse-switch v3, :sswitch_data_0

    .line 175
    const/16 v4, 0x20

    if-lt v3, v4, :cond_1

    const/16 v4, 0x2028

    if-eq v3, v4, :cond_1

    const/16 v4, 0x2029

    if-eq v3, v4, :cond_1

    const/16 v4, 0x3c

    if-eq v3, v4, :cond_1

    const/16 v4, 0x3e

    if-ne v3, v4, :cond_2

    .line 176
    :cond_1
    sget-object v4, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    const-string v5, "\\u%04x"

    const/4 v6, 0x1

    new-array v6, v6, [Ljava/lang/Object;

    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    aput-object v3, v6, v1

    invoke-static {v4, v5, v6}, Ljava/lang/String;->format(Ljava/util/Locale;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 166
    :goto_2
    add-int/lit8 v0, v0, 0x1

    goto :goto_1

    .line 169
    :sswitch_0
    const-string v3, "\\\""

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 170
    :sswitch_1
    const-string v3, "\\\\"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 171
    :sswitch_2
    const-string v3, "\\n"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 172
    :sswitch_3
    const-string v3, "\\r"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 173
    :sswitch_4
    const-string v3, "\\t"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 178
    :cond_2
    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 182
    :cond_3
    invoke-virtual {v2, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 183
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    goto :goto_0

    .line 168
    nop

    :sswitch_data_0
    .sparse-switch
        0x9 -> :sswitch_4
        0xa -> :sswitch_2
        0xd -> :sswitch_3
        0x22 -> :sswitch_0
        0x5c -> :sswitch_1
    .end sparse-switch
.end method

.method private static m(Ljava/lang/String;Ljava/lang/String;Z)V
    .locals 1

    .prologue
    .line 22
    sget-object v0, Lcom/bereket/alacakverecek/Util;->EXT2MIME:Ljava/util/Map;

    invoke-interface {v0, p0, p1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 23
    if-nez p2, :cond_0

    sget-object v0, Lcom/bereket/alacakverecek/Util;->MIME2EXT:Ljava/util/Map;

    invoke-interface {v0, p1}, Ljava/util/Map;->containsKey(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    :cond_0
    sget-object v0, Lcom/bereket/alacakverecek/Util;->MIME2EXT:Ljava/util/Map;

    invoke-interface {v0, p1, p0}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 24
    :cond_1
    return-void
.end method

.method static mimeForName(Ljava/lang/String;)Ljava/lang/String;
    .locals 2

    .prologue
    .line 85
    sget-object v0, Lcom/bereket/alacakverecek/Util;->EXT2MIME:Ljava/util/Map;

    invoke-static {p0}, Lcom/bereket/alacakverecek/Util;->extension(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    invoke-interface {v0, v1}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    return-object v0
.end method

.method static mimeForNameOr(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 1

    .prologue
    .line 89
    invoke-static {p0}, Lcom/bereket/alacakverecek/Util;->mimeForName(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 90
    if-eqz v0, :cond_0

    move-object p1, v0

    :cond_0
    return-object p1
.end method

.method private static num(Ljava/lang/String;)I
    .locals 8

    .prologue
    const/4 v0, 0x0

    .line 263
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    .line 264
    invoke-virtual {p0}, Ljava/lang/String;->toCharArray()[C

    move-result-object v3

    array-length v4, v3

    move v1, v0

    :goto_0
    if-ge v1, v4, :cond_1

    aget-char v5, v3, v1

    const/16 v6, 0x30

    if-lt v5, v6, :cond_0

    const/16 v6, 0x39

    if-gt v5, v6, :cond_0

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->length()I

    move-result v6

    const/16 v7, 0x9

    if-ge v6, v7, :cond_0

    invoke-virtual {v2, v5}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    :cond_0
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 265
    :cond_1
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->length()I

    move-result v1

    if-nez v1, :cond_2

    :goto_1
    return v0

    :cond_2
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    goto :goto_1
.end method

.method static safeFileName(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 5

    .prologue
    const/4 v1, 0x0

    .line 113
    if-nez p0, :cond_0

    const-string p0, ""

    .line 114
    :cond_0
    const/16 v0, 0x2f

    invoke-virtual {p0, v0}, Ljava/lang/String;->lastIndexOf(I)I

    move-result v0

    const/16 v2, 0x5c

    invoke-virtual {p0, v2}, Ljava/lang/String;->lastIndexOf(I)I

    move-result v2

    invoke-static {v0, v2}, Ljava/lang/Math;->max(II)I

    move-result v0

    .line 115
    if-ltz v0, :cond_1

    add-int/lit8 v0, v0, 0x1

    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p0

    .line 116
    :cond_1
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v0

    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(I)V

    move v0, v1

    .line 117
    :goto_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    if-ge v0, v3, :cond_4

    .line 118
    invoke-virtual {p0, v0}, Ljava/lang/String;->charAt(I)C

    move-result v3

    .line 119
    const/16 v4, 0x20

    if-lt v3, v4, :cond_2

    const/16 v4, 0x7f

    if-eq v3, v4, :cond_2

    const-string v4, "/\\:*?\"<>|"

    invoke-virtual {v4, v3}, Ljava/lang/String;->indexOf(I)I

    move-result v4

    if-ltz v4, :cond_3

    :cond_2
    const/16 v3, 0x5f

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 117
    :goto_1
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    .line 120
    :cond_3
    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    goto :goto_1

    .line 122
    :cond_4
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    .line 123
    :goto_2
    const-string v2, "."

    invoke-virtual {v0, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_5

    const/4 v2, 0x1

    invoke-virtual {v0, v2}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v0

    goto :goto_2

    .line 124
    :cond_5
    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v2

    if-nez v2, :cond_6

    const-string v0, "dosya"

    .line 125
    :cond_6
    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v2

    const/16 v3, 0x78

    if-le v2, v3, :cond_a

    .line 126
    invoke-static {v0}, Lcom/bereket/alacakverecek/Util;->extension(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    .line 127
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v2

    if-lez v2, :cond_8

    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v2

    add-int/lit8 v2, v2, 0x1

    :goto_3
    rsub-int/lit8 v2, v2, 0x78

    invoke-virtual {v0, v1, v2}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v0

    if-lez v0, :cond_9

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "."

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    :goto_4
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    move-object v1, v0

    .line 129
    :goto_5
    invoke-static {v1}, Lcom/bereket/alacakverecek/Util;->extension(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v0

    if-nez v0, :cond_7

    if-eqz p1, :cond_7

    .line 130
    sget-object v0, Lcom/bereket/alacakverecek/Util;->MIME2EXT:Ljava/util/Map;

    sget-object v2, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {p1, v2}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v2

    invoke-interface {v0, v2}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    .line 131
    if-eqz v0, :cond_7

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "."

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    .line 133
    :cond_7
    return-object v1

    :cond_8
    move v2, v1

    .line 127
    goto :goto_3

    :cond_9
    const-string v0, ""

    goto :goto_4

    :cond_a
    move-object v1, v0

    goto :goto_5
.end method

.method static stripDataUrl(Ljava/lang/String;)Ljava/lang/String;
    .locals 5

    .prologue
    .line 138
    if-nez p0, :cond_0

    const-string v0, ""

    .line 153
    :goto_0
    return-object v0

    .line 139
    :cond_0
    const/4 v0, 0x0

    .line 140
    const-string v1, "data:"

    invoke-virtual {p0, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_1

    .line 141
    const/16 v0, 0x2c

    invoke-virtual {p0, v0}, Ljava/lang/String;->indexOf(I)I

    move-result v0

    .line 142
    if-ltz v0, :cond_4

    add-int/lit8 v0, v0, 0x1

    .line 144
    :cond_1
    :goto_1
    const/4 v1, 0x0

    move v2, v0

    .line 145
    :goto_2
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    if-ge v2, v3, :cond_6

    .line 146
    invoke-virtual {p0, v2}, Ljava/lang/String;->charAt(I)C

    move-result v3

    .line 147
    const/16 v4, 0x20

    if-eq v3, v4, :cond_2

    const/16 v4, 0xa

    if-eq v3, v4, :cond_2

    const/16 v4, 0xd

    if-eq v3, v4, :cond_2

    const/16 v4, 0x9

    if-ne v3, v4, :cond_5

    .line 148
    :cond_2
    if-nez v1, :cond_3

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    invoke-direct {v1, v3}, Ljava/lang/StringBuilder;-><init>(I)V

    invoke-virtual {v1, p0, v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/CharSequence;II)Ljava/lang/StringBuilder;

    .line 145
    :cond_3
    :goto_3
    add-int/lit8 v2, v2, 0x1

    goto :goto_2

    .line 142
    :cond_4
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v0

    goto :goto_1

    .line 149
    :cond_5
    if-eqz v1, :cond_3

    .line 150
    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    goto :goto_3

    .line 153
    :cond_6
    if-eqz v1, :cond_7

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    goto :goto_0

    :cond_7
    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method
