; Rokudenashi Blues English patch. Applied by tools/build.py to a 2 MB copy (banks $B0+ are free, 0xFF).
lorom

; ---------------------------------------------------------------------------------------------------------------
; VWF for the dialogue renderer. The original draws each 16x16 glyph as 2 columns (4 tiles, 0x40 bytes) at VRAM
; word $1E12 (+0x20 per glyph). A line is a linear strip of 8px columns (2 tiles each), so we render glyphs at any
; pixel x into a 2-column 1bpp buffer, colourise it with the game's own routines and DMA those 2 columns.
; Codes >= $0300 are English (ascii - $20 + $0300); lower codes keep the original fixed-cell path.
; State lives at $7E:FF00 (unused WRAM). A new line/page/message is detected by $1E12 no longer holding the
; value we left there (we leave an odd value the game never produces).
; ---------------------------------------------------------------------------------------------------------------
!LAST  = $FF00
!BASE  = $FF02
!XPOS  = $FF04
!SHIFT = $FF06
!WID   = $FF08
!TMP   = $FF0A
!BUF   = $FF10          ; column 0 rows 0-15, then column 1 rows 0-15

org $88A1B4
vwf_ret:
org $88A1A4             ; was: JSL A545 (load glyph), A5AB + A652 (colourise), A584 (DMA, $1E12 += $20)
    jsl vwf_draw
    bra vwf_ret

; ---------------------------------------------------------------------------------------------------------------
; Runtime word wrap + {page}. Box widths differ per scene (narration 15 cells, portrait box 13; last line of a
; page 13 / 11), so the build can't wrap. The main text loop reads each word via JSL $88A168 at $88:A0CE; we
; return FFFE (newline: the game's own handler consumes the code and pages when the box is full) instead of
; a space whose next word won't fit, and handle FFE0 = {page}: newline without consuming until the last row.
; Limit in px = cells * 16 - 16 (cells = $0F98 & $1F, or $0F99 & $0F on the last row $0F99 & $F0).
; ---------------------------------------------------------------------------------------------------------------
!SUM   = $FF0C
!SPACE = $0300
!PAGE  = $FFE0

org $88A0CE
    jsl wrap_read

org $88A0B8             ; typing speed: a glyph every 2 frames instead of 4 (English has ~2.5x the glyphs)
    and #$01

org $B08000
wrap_read:
    php
    phb
    phx
    phy
    rep #$30
    pea $7E7E
    plb
    plb
.again:
    jsl $88A168         ; A = word, DP $10-$12 = text pointer
    rep #$30
    cmp #!PAGE
    bne .notpage
    lda $1E0D
    and #$00FF
    bne +
    inc $1E0A           ; nothing on the page yet: drop the code
    bra .again
+   and #$00E0
    sta !SUM
    lda $0F99
    and #$00F0
    cmp !SUM
    beq .newline        ; last row: a plain newline waits for a key and starts the next page
    dec $1E0A           ; else newline, and the handler's increment leaves us on {page} again
    bra .newline
.notpage:
    cmp #!SPACE
    bne .ret
    lda $1E12           ; x = current pixel position if a line is in progress
    cmp !LAST
    bne .ret            ; leading space: keep
    lda !XPOS
    beq .ret
    clc
    adc.l en_widths
    and #$00FF          ; (x + space width; x < 256)
    sta !SUM
    lda $1E0A
    inc
    asl
    tay
-   lda [$10],y         ; add the widths of the following word
    cmp #!SPACE+1
    bcc +
    cmp #$0400
    bcs +
    sec
    sbc #!SPACE
    tax
    lda.l en_widths,x
    and #$00FF
    clc
    adc !SUM
    sta !SUM
    iny
    iny
    bra -
+   lda $1E0D           ; limit: last row of the page or a normal row
    and #$00E0
    sta !TMP
    lda $0F99
    and #$00F0
    cmp !TMP
    bne +
    lda $0F99
    and #$000F
    bra ++
+   lda $0F98
    and #$001F
++  asl
    asl
    asl
    asl
    sec
    sbc #$0010          ; = build.py MARGIN: the box shows one cell less than $0F98
    cmp !SUM
    bcs .space          ; limit >= x + word: fits
.newline:
    lda #$FFFE
    bra .ret
.space:
    lda #!SPACE
.ret:
    ply
    plx
    plb
    plp
    rep #$20
    rtl

vwf_draw:              ; in: A16 X16, DP $00 = code * 32
    lda $00
    cmp #$6000
    bcs +
    jsl $88A545         ; Japanese glyph: the original fixed-cell path (other screens use other layouts)
    jsl $88A5AB
    jsl $88A652
    jsl $88A584
    rtl
+   php
    phb
    rep #$30
    pea $7E7E
    plb
    plb
    lda $1E12
    cmp !LAST
    beq .same
    clc
    adc #$0020
    sta !BASE
    stz !XPOS
    ldx #$001E
-   stz !BUF,x
    dex
    dex
    bpl -
.same:
    lda $00
    lsr
    lsr
    lsr
    lsr
    lsr
    sec
    sbc #$0300
    tax
    lda.l en_widths,x
    and #$00FF
    sta !WID
    txa
    asl
    asl
    asl
    asl
    clc
    adc.w #en_font&$FFFF
    sta $02
    sep #$20
    lda.b #en_font>>16
    sta $04
    rep #$20
    jsr render
    lda !XPOS
    and #$FFF8
    asl
    clc
    adc !BASE
    inc
    sta $1E12
    sta !LAST
    sep #$20            ; column count 0 (the caller increments it to 1): never triggers auto-wrap or page end,
    lda $1E0D           ; but stays non-zero so a newline is not taken for a leading one
    and #$E0
    sta $1E0D
    plb
    plp
    rtl

render:                 ; OR glyph ($02-$04, 16 rows, width !WID) in at !XPOS, upload, advance
    lda !XPOS
    and #$0007
    sta !SHIFT
    ldy #$0000
.row:
    lda [$02],y
    and #$00FF
    xba
    ldx !SHIFT
    beq +
-   lsr
    dex
    bne -
+   sta !TMP
    sep #$20
    lda !TMP+1
    ora !BUF,y
    sta !BUF,y
    lda !TMP
    ora !BUF+16,y
    sta !BUF+16,y
    rep #$20
    iny
    cpy #$0010
    bne .row
    jsr upload
    lda !XPOS
    clc
    adc !WID
    sta !TMP
    eor !XPOS
    and #$FFF8
    beq +
    ldx #$000E          ; moved into the next column: shift the buffer left one column
-   lda !BUF+16,x
    sta !BUF,x
    stz !BUF+16,x
    dex
    dex
    bpl -
+   lda !TMP
    sta !XPOS
    rts

upload:                 ; buffer -> $1E15 words (low byte = 1bpp row), colourise, queue a 0x40-byte DMA
    ldx #$0000
    ldy #$0000
-   lda !BUF,x
    and #$00FF
    sta $1E15,y
    inx
    iny
    iny
    cpx #$0020
    bne -
    jsl $88A5AB
    jsl $88A652
    rep #$30
    sep #$20
    stz $87
    rep #$20
    lda #$1E15
    sta $85
    lda #$0040
    sta $8A
    lda !XPOS
    and #$FFF8
    asl
    clc
    adc !BASE
    sta $88
    lda #$1000
    tsb $57
    rts

en_font:
    incbin "../build/en_font.bin"
en_widths:
    incbin "../build/en_widths.bin"
