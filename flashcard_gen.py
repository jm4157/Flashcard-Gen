"""Takes a number of words in English, does something to them in Chinese, and 
generates a pdf of flashcards of those words.

@author Judah Munoz
"""
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch


MRGN_HORZ = int(1 * inch)
MRGN_VERT = int(0.75 * inch)    # MRGN is the length of the page margin
SPC_HORZ  = int(1 * inch)
SPC_VERT  = int(1 * inch)       # SPC is the space between the cards
CARD_WDTH = int(4 * inch)
CARD_HGHT = int(3 * inch)
# The program asumes that 2MRGN_HORZ + 2CARD_WIDTH + SPC_HORZ = 11 inches and
# 2MRGN_VERT + 2CARD_HGHT + SPC_VERT = 8.5 inches to fit US letter paper

OFFSETS_FRONT = [
    (MRGN_HORZ,                        MRGN_VERT), 
    (MRGN_HORZ,                        MRGN_VERT + CARD_HGHT + SPC_VERT),
    (MRGN_HORZ + CARD_WDTH + SPC_HORZ, MRGN_VERT), 
    (MRGN_HORZ + CARD_WDTH + SPC_HORZ, MRGN_VERT + CARD_HGHT + SPC_VERT)
    ]
"""A list of offsets used to place the front of each card onto the canvas."""
OFFSETS_BACK = [
    (MRGN_HORZ + CARD_WDTH + SPC_HORZ, MRGN_VERT), 
    (MRGN_HORZ + CARD_WDTH + SPC_HORZ, MRGN_VERT + CARD_HGHT + SPC_VERT),
    (MRGN_HORZ,                        MRGN_VERT),
    (MRGN_HORZ,                        MRGN_VERT + CARD_HGHT + SPC_VERT)
                ]
"""A list of offsets used to place the back of each card onto the canvas."""


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
        data = cards[i].front
        (offset_x, offset_y) = OFFSETS_FRONT[i]

        draw_card_front(data, canvas, offset_x, offset_y)

    canvas.showPage()

    for i in range(0, 4): # Draw the back of each card
        data = cards[i].back
        (offset_x, offset_y) = OFFSETS_BACK[i]

        draw_card_back(data, canvas, offset_x, offset_y)


def draw_card_front(data, canvas: Canvas, offset_x: int, offset_y: int):
    """Draws a single card front onto a canvas.

    @param data: the information on the card's front
    @param canvas: the canvas to draw onto
    @param offset_x: the offset along the x axis
    @param offset_y: the offset along the y axis
    """
    canvas.rect(offset_x, offset_y, CARD_WDTH, CARD_HGHT, fill=False, stroke=True)
    
    canvas.drawString(1 * inch + offset_x, 1 * inch + offset_y, data)


def draw_card_back(data, canvas: Canvas, offset_x: int, offset_y: int):
    """Draws a single card back onto a canvas.

    @param data: the information on the card's front
    @param canvas: the canvas to draw onto
    @param offset_x: the offset along the x axis
    @param offset_y: the offset along the y axis
    """
    canvas.rect(offset_x, offset_y, CARD_WDTH, CARD_HGHT, fill=False, stroke=True)
    
    canvas.drawString(1 * inch + offset_x, 1 * inch + offset_y, data)


if __name__ == "__main__":
    canvas = Canvas("flashcards.pdf", pagesize=landscape(letter))
    cards = [CardInfo("Front1", "Back1"),
             CardInfo("Front2", "Back2"),
             CardInfo("Front3", "Back3"),
             CardInfo("Front4", "Back4"),]

    draw_cardset(cards, canvas)

    canvas.save()