"""Takes a number of words in English, does something to them in Chinese, and 
generates a pdf of flashcards of those words.

@author Judah Munoz
"""
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth, getFont, registerFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont


MRGN_HORZ = int(0.75 * inch)
MRGN_VERT = int(1 * inch)       # MRGN is the length of the page margin
SPC_HORZ  = int(1 * inch)
SPC_VERT  = int(1 * inch)       # SPC is the space between the cards
CARD_WDTH = int(3 * inch)
CARD_HGHT = int(4 * inch)
# The program asumes that 2MRGN_HORZ + 2CARD_WIDTH + SPC_HORZ = 11 inches and
# 2MRGN_VERT + 2CARD_HGHT + SPC_VERT = 8.5 inches to fit US letter paper

SPC_SML = 14
SPC_LG = 28
HGHT_IMG = 72
HGHT_TXT = 15

OFFSETS = [
    (MRGN_HORZ,                        MRGN_VERT), 
    (MRGN_HORZ,                        MRGN_VERT + CARD_HGHT + SPC_VERT),
    (MRGN_HORZ + CARD_WDTH + SPC_HORZ, MRGN_VERT), 
    (MRGN_HORZ + CARD_WDTH + SPC_HORZ, MRGN_VERT + CARD_HGHT + SPC_VERT)
    ]
"""A list of offsets used to place the front of each card onto the canvas."""


class CardInfo:
    """Holds all the information for a single flashcard.
    """
    def __init__(self, img, wrd_chn, wrd_eng, phon, xmpl_chn, xmpl_eng, qr):
        self.img      = img
        self.wrd_chn  = wrd_chn
        self.wrd_eng  = wrd_eng
        self.phon     = phon
        self.xmpl_chn = xmpl_chn
        self.xmpl_eng = xmpl_eng
        self.qr       = qr


def draw_cardset(cards: list[CardInfo], canvas: Canvas):
    """Takes a list of 4 flashcard infos and draws them onto the pdf.

    @param cards: a list of CardInfo
    @param canvas: the canvas to draw onto
    """
    for i in range(0, 4): # Draw the front of each card
        data = cards[i]
        (offset_x, offset_y) = OFFSETS[i]

        draw_card(data, canvas, offset_x, offset_y)


def draw_card(data: CardInfo, canvas: Canvas, offset_x: int, offset_y: int):
    """Draws a single card front onto a canvas.

    @param data: the information on the card's front
    @param canvas: the canvas to draw onto
    @param offset_x: the offset along the x axis
    @param offset_y: the offset along the y axis
    """
    canvas.rect(offset_x, offset_y, CARD_WDTH, CARD_HGHT, fill=False, stroke=True)

    canvas.setFont('NotoSans', 11)
    x = offset_x + int(CARD_WDTH / 2) - int(stringWidth(data.xmpl_eng, 'NotoSans', 11) / 2)
    y = offset_y + SPC_LG + HGHT_TXT
    canvas.drawString(x, y, data.xmpl_eng)

    canvas.setFont('NotoSansSC', 11)
    x = offset_x + int(CARD_WDTH / 2) - int(stringWidth(data.xmpl_chn, 'NotoSansSC', 11) / 2)
    y += 2 * HGHT_TXT + SPC_SML
    canvas.drawString(x, y, data.xmpl_chn)

    canvas.setFont('NotoSans', 14)
    ln = data.wrd_eng + " - " + data.phon
    x = offset_x + int(CARD_WDTH / 2) - int(stringWidth(ln, 'NotoSans', 14) / 2)
    y += 2 * HGHT_TXT + SPC_LG
    canvas.drawString(x, y, ln)

    canvas.setFont('NotoSansSC', 14)
    x = offset_x + int(CARD_WDTH / 2) - int(stringWidth(data.wrd_chn, 'NotoSansSC', 14) / 2)
    y += HGHT_TXT + SPC_SML
    canvas.drawString(x, y, data.wrd_chn)

    y += HGHT_TXT + SPC_LG
    canvas.drawString(offset_x, y, data.img)


if __name__ == "__main__":
    canvas = Canvas("flashcards.pdf", pagesize=LETTER)
    registerFont(UnicodeCIDFont('STSong-Light'))
    registerFont(TTFont('NotoSans', 'NotoSans-Regular.ttf'))
    registerFont(TTFont('NotoSansSC', 'NotoSansSC-Regular.ttf'))

    cards = [CardInfo("Picture", "椅子", "Chair", "Yǐzǐ", "椅子很舒服。", "The chair is cozy.", "QR code"),
             CardInfo("Picture", "桌子", "Table", "Zhuōzǐ", "我的盘子在桌子上。", "My plate is on the table.", "QR code"),
             CardInfo("Picture", "床", "Bed", "Chuáng", "我喜欢晚上睡在我的床上。", "I like to sleep in my bed at night.", "QR code"),
             CardInfo("Picture", "梳妆台", "Dresser", "Shūzhuāng tái", "梳妆台里面有衣服。", "The dresser has clothes inside.", "QR code")]

    draw_cardset(cards, canvas)

    canvas.save()

    # face = getFont('NotoSans').face
    # string_height = (face.ascent - face.descent) / 1000 * 11

    # print(string_height)