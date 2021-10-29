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
        point = True
        while True:
            with canvas(self.virtual) as draw:
                point = not point
                text(draw, (0, 1), datetime.now().strftime('%H'), fill="white", font=proportional(LCD_FONT))
                text(draw, (12, 1), ':' if point else ' ', fill="white", font=proportional(TINY_FONT))
                text(draw, (14, 1), datetime.now().strftime('%M'), fill="white", font=proportional(LCD_FONT))
                text(draw, (26, 1), ' ' if point else ':', fill="white", font=proportional(TINY_FONT))
                text(draw, (28, 1), datetime.now().strftime('%S'), fill="white", font=proportional(LCD_FONT))
                text(draw, (46, 1), datetime.now().strftime('%d.%m'), fill="white", font=proportional(TINY_FONT))
                sleep(1)

    def showText(self, showText):
        with canvas(self.virtual) as draw:
            text(draw, (0, 1), showText, fill="white", font=proportional(LCD_FONT))

    def clockStart(self):
        self.clockProcess = multiprocessing.Process(target=self.clockLoop)
        self.clockProcess.start()

    def clockStop(self):
        self.clockProcess.terminate()
