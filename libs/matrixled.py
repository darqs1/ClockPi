from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT, TINY_FONT

from time import sleep
from datetime import datetime

import multiprocessing

class MatrixLed:
    LCD_FONT[49] = [0x40, 0x42, 0x7f, 0x40, 0x40, 0x00, 0x00, 0x00]  # '1'
    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, width=64, height=8, block_orientation=-90)
        self.device.contrast(10)
        self.virtual = viewport(self.device, width=64, height=8)
        self.clockProcess = None

    def showMessage(self, message, delay=0.04):
        show_message(self.device, message, fill="white", font=proportional(LCD_FONT), scroll_delay=delay)

    def clockLoop(self):
        step = 10
        step_now = 1

        point = True
        move_right = True
        margin = 0
        second = datetime.now().strftime('%S')
        while True:
            with canvas(self.virtual) as draw:
                second_now = datetime.now().strftime('%S')
                if second!=second_now:
                    point = not point
                    second=second_now

                text(draw, (0+margin, 1 if move_right else 0), datetime.now().strftime('%H'), fill="white", font=proportional(LCD_FONT))
                text(draw, (12+margin, 1 if move_right else 0), ':' if point else ' ', fill="white", font=proportional(TINY_FONT))
                text(draw, (14+margin, 1 if move_right else 0), datetime.now().strftime('%M'), fill="white", font=proportional(LCD_FONT))
                text(draw, (26+margin, 1 if move_right else 0), ' ' if point else ':', fill="white", font=proportional(TINY_FONT))
                text(draw, (28+margin, 1 if move_right else 0), datetime.now().strftime('%S'), fill="white", font=proportional(LCD_FONT))
                if margin < 8:
                    text(draw, (47, 1 if move_right else 0), datetime.now().strftime('%d.%m'), fill="white", font=proportional(TINY_FONT))
                if margin > 17:
                    text(draw, (0, 1 if move_right else 0), datetime.now().strftime('%d.%m'), fill="white", font=proportional(TINY_FONT))

                if margin >=8 and margin <=17:
                    text(draw, (0, 1 if move_right else 0), datetime.now().strftime('%d'), fill="white", font=proportional(TINY_FONT))
                    text(draw, (57, 1 if move_right else 0), datetime.now().strftime('%m'), fill="white", font=proportional(TINY_FONT))

                if step_now == step:
                    step_now = 1

                    if move_right:
                        margin += 1
                    else:
                        margin -= 1

                    if margin > 24 or margin == 0:
                        move_right = not move_right
                else:
                    step_now += 1


                sleep(0.1)
                # self.showText(margin)

    def showText(self, showText):
        with canvas(self.virtual) as draw:
            text(draw, (0, 1), showText, fill="white", font=proportional(LCD_FONT))

    def clockStart(self):
        self.clockProcess = multiprocessing.Process(target=self.clockLoop)
        self.clockProcess.start()

    def clockStop(self):
        self.clockProcess.terminate()
